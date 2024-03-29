"""
mosk localhost module for classes collecting file information.
"""

__author__ = '3Peso'

import logging
import os
import platform
import shutil
import datetime
import re
from logging import Logger
from collections import namedtuple
from os import path
from pathlib import Path
from shutil import copyfile

from baseclasses.artefact import ArtefactBase, MacArtefact, LinuxArtefact, FileClass
from businesslogic.support import get_userfolders, md5, run_terminal_command
from businesslogic.errors import MaxDirectoriesReachedError, TreePathError, CollectorParameterError


TermianlHistory = namedtuple('TerminalHistory', ['Path', 'Content'])


class FileExistence(ArtefactBase, FileClass):
    """
    Tests if a file exsists under the provided path and returns True or False accordingly.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        if path.exists(self.source_path):
            self.data = f"File '{self.source_path}' exists."
            self.data[-1].sourcepath = self.source_path
        else:
            self.data = f"File '{self.source_path}' does not exist."


class FileContent(ArtefactBase, FileClass):
    """
    Retrieves the file content of a file provided by path. It does NOT copy the file itself. The
    content is stored inside the log created during the collection session.
    """
    _max_file_size: int = 1024*1024*10 # by default at max 10 MiBs

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        if path.exists(self.source_path):
            with open(self.source_path, "r") as filetoload:
                self._read_file(filetoload, self.source_path)
            self.data[-1].sourcepath = self.source_path
        else:
            self.data = f"File '{self.source_path}' does not exist."

    def _read_file(self, filetoload, filepath) -> None:
        if Path(filepath).stat().st_size > self._max_file_size:
            self.data = f"File '{filepath}' is bigger than {self._max_file_size / 1024 / 1024} MiBs. " \
                        f"File Content Collector max file size is {self._max_file_size / 1024 / 1024} MiBs."
        else:
            self.data = filetoload.read()


class ShellHistoryOfAllUsers(MacArtefact):
    """
    Tries to access all user folders of a macOS installation and then it iterates over the possible shell history
    files (.bash_history and .zhs_history).
    """
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        userfolders: set = set(get_userfolders())
        for history in ShellHistoryOfAllUsers._collect_bash_history(userfolders):
            self.data = history.Content
            self.data[-1].sourcepath = history.Path

    @staticmethod
    def _collect_bash_history(userfolders):
        historyfilepaths = (path.join(folder, history) for folder in userfolders
                            for history in ['.bash_history', '.zsh_history'])
        for historyfile in historyfilepaths:
            if path.exists(historyfile):
                ShellHistoryOfAllUsers._logger.debug("Found terminal history file '{}'.".format(historyfile))
                with open(historyfile, encoding='unicode_escape') as hf:
                    yield TermianlHistory(Path=historyfile, Content=hf.read())


class FileHash(ArtefactBase, FileClass):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        if not re.compile(r'^[a-f0-9]{32}$').match(self.filehash):
            self.data = f"MD5 hash '{self.filehash}' is invalid."

        if not os.path.exists(self.source_path):
            self.data = f"The file '{self.source_path}' does not exist."
        else:
            file_hash = md5(self.source_path)
            if file_hash != self.filehash:
                self.data = f"The hash '{file_hash}' of file '{self.source_path}' does not match the provided " \
                            f"hash '{self.filehash}'."
            else:
                self.data = f"The hash '{file_hash}' of file '{self.source_path}' matches the provided " \
                            f"hash '{self.filehash}'."


class FileCopy(MacArtefact, LinuxArtefact, FileClass):
    """
    Tries to copy the file in a live session provided by 'filepath'.
    The file copy is stored alongside the collection log. The collection log points to the copied file, but
    does not hold it.
    """
    _destination_directory = '.'
    _FILE_PATH_SEPERATOR = '\n'
    _WILDCARD:str = '*'
    _OS_PATH_SEPERATOR = '/' if platform.system() != 'Windows' else '\\'

    def __init__(self, *args, **kwargs) -> None:
        # Will be filled in super with the property setter filepath.
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        for file_path in self.source_path.split(self._FILE_PATH_SEPERATOR):
            if path.isfile(file_path):
                self._collect_single(file_path=file_path)
            else:
                tree_paths:list = self._expand_path(input_path=file_path)
                for path_ in tree_paths:
                    if not path.exists(path_):
                        self.data = f"The path '{path_}' does not exist."
                    else:
                        self._collect_tree(tree_path=path_)

    def _collect_single(self, file_path: str = '') -> None:
        is_file = path.isfile(file_path)
        source_exists: bool = os.path.exists(file_path)
        enough_space: bool = True

        try:
            if source_exists and is_file:
                target_path: str = self._ensure_target_directory()
                file_copy_destination: str = os.path.join(target_path, os.path.basename(file_path))
                enough_space = self._enough_space_on_target(target_path=target_path, source_path=file_path)
                target_path_length_valid: bool = self._validate_target_path_length(file_copy_destination)

                if not enough_space:
                    self.data = f"File '{file_path}' could not be copied, " \
                                f"because there is not enough space on target '{target_path}'."
                if not target_path_length_valid:
                    self.data = f"File '{file_path}' could not be copied, because the target path " \
                                f"length of '{target_path}' is too long for the underlying system."

                else:
                    copyfile(file_path, file_copy_destination)
                    self.data = f"Copied file '{file_path}' to '{file_copy_destination}'."
                    self.data[-1].sourcepath = file_path

            if not is_file:
                self.data = f"The provided filepath '{file_path}' is not a file."

            if not source_exists:
                self.data = f"The file '{file_path}' does not exist."
        finally:
            if not enough_space:
                shutil.rmtree(path.dirname(file_copy_destination), True)

    def _collect_tree(self, tree_path:str) -> None:
        # TODO: validate length of destination path
        for file_ in [f for f in os.listdir(tree_path) if path.isfile(path.join(tree_path, f))]:
            try:
                self.data = f"Copied file '{path.join(tree_path, file_)}'."
                self.data[-1].sourcepath = path.join(tree_path, file_)
            except PermissionError:
                self.data = f"Could not collect data of file '{path.join(tree_path, file_)}'. Permission denied."

            if self._enough_space_on_target(self.destination_directory, tree_path):
                target_path:str = self._ensure_target_directory()
                shutil.copytree(tree_path, os.path.join(target_path, 'tree'))

    def _ensure_target_directory(self) -> str:
        if not path.exists(self.destination_directory):
            os.mkdir(self.destination_directory)

        unique_dir_name = self._get_unique_directory_name(self.destination_directory, datetime.datetime.now())
        new_unique_directory: bytes = os.path.join(self.destination_directory, unique_dir_name)
        os.mkdir(new_unique_directory)

        return new_unique_directory

    def _get_unique_directory_name(self, target_directory, dt: datetime.datetime) -> str:
        logger: Logger = logging.getLogger(__name__)
        # Assume, target directory exists.
        # REMARKS: This only works correct on macOS and Linux.
        filename: str = path.basename(self.source_path)
        timestamp: str = f"{dt.year}{str(dt.month).zfill(2)}{str(dt.day).zfill(2)}" \
                         f"{str(dt.hour).zfill(2)}{str(dt.minute).zfill(2)}{str(dt.second).zfill(2)}"

        unique_name: str = f"{filename}_{timestamp}{str(1).zfill(2)}"
        max_counter: int = 99
        for counter in range(2, max_counter+1):
            if not path.exists(path.join(target_directory, unique_name)):
                break
            else:
                unique_name = f"{filename}_{timestamp}{str(counter).zfill(2)}"

            if counter == max_counter:
                logger.warning("Max counter reached.")
                raise MaxDirectoriesReachedError("Max counter reached. Consider less calling 'FileCopy' collectors.")

        return unique_name

    @staticmethod
    def _enough_space_on_target(target_path, source_path) -> bool:
        if not os.path.exists(target_path):
            return False

        if not os.path.exists(source_path):
            return False

        freespace = shutil.disk_usage(target_path).free
        size_of_file_to_copy = Path(source_path).stat().st_size
        if freespace > size_of_file_to_copy:
            return True
        else:
            return False

    @staticmethod
    def _validate_target_path_length(targert_path) -> bool:
        if platform.system() != "Windows":
            return True

        max_windows_path_length = 260
        is_valid = len(targert_path) <= max_windows_path_length

        return is_valid

    @property
    def destination_directory(self):
        return self._destination_directory

    @destination_directory.setter
    def destination_directory(self, value):
        if not os.path.exists(value):
            raise FileNotFoundError(f"The destination directory '{value}' does not exist.")

        if os.path.isfile(value):
            raise CollectorParameterError(f"The provided destination directory '{value}' is a file.")

        self._destination_directory = value

    def _expand_path(self, input_path:str) -> list:
        try:
            if input_path.index(self._WILDCARD) < input_path.rindex(self._OS_PATH_SEPERATOR):
                raise TreePathError('Wildcards are only supported in leaf nodes.')
        except ValueError:
            pass

        if self._WILDCARD not in input_path:
            return [input_path]

        # TODO: Support wildcards in parent dir names
        path_regex = re.compile(input_path)
        return [f.path for f in os.scandir(input_path.replace(
            input_path[input_path.rindex(self._OS_PATH_SEPERATOR):], ''))
                if f.is_dir() and path_regex.match(f.path)]


class FileMetadata(ArtefactBase, FileClass):
    """
    Tries to collect as much metadata to a target file, as possible.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._metadata: dict = {}

    def _collect(self) -> None:
        file_exists: bool = os.path.exists(self.source_path)
        if not file_exists:
            self.data = f"File '{self.source_path}' does not exist."

        if file_exists:
            self._collect_timestamps()
            self._collect_sizes()
            self._collect_other()
            self._collect_extended_attributes()
            self.data = self._metadata
            self.data[-1].sourcehash = md5(fpath=self.source_path)
            self.data[-1].sourcepath = self.source_path

    def _collect_extended_attributes(self):
        if platform.system() != "Darwin":
            self.data = f"Collection of extended attributes on platform '{platform.system()}' is not supported."
            return

        extended_attributes = run_terminal_command(['xattr', self.source_path])

        if extended_attributes is not None and extended_attributes != "":
            self.data = f"Extended Attributes: {extended_attributes}"

    def _collect_sizes(self) -> None:
        stats = Path(self.source_path).stat()
        self._metadata['Size in Bytes'] = stats.st_size
        self._metadata['Used Blocks'] = stats.st_blocks
        self._metadata['Block Size'] = stats.st_blksize

    def _collect_other(self) -> None:
        stats = Path(self.source_path).stat()
        self._metadata['INode Number'] = stats.st_ino
        self._metadata['Owner ID'] = stats.st_uid
        self._metadata['Group ID'] = stats.st_gid
        self._metadata['File Type and Permissions'] = stats.st_mode

    def _collect_timestamps(self) -> None:
        modified_datetime = os.path.getmtime(self.source_path)
        self._metadata['Modified'] = datetime.datetime.utcfromtimestamp(modified_datetime)\
            .strftime("%Y-%m-%d %H:%M:%S UTC")

        created_datetime = os.path.getctime(self.source_path)
        self._metadata['Created'] = datetime.datetime.utcfromtimestamp(created_datetime)\
            .strftime("%Y-%m-%d %H:%M:%S UTC")

        accessd_datetime = os.path.getatime(self.source_path)
        self._metadata['Accessed'] = datetime.datetime.utcfromtimestamp(accessd_datetime)\
            .strftime("%Y-%m-%d %H:%M:%S UTC")

        if platform.system() != "Windows":
            birth_datetime = Path(self.source_path).stat().st_birthtime
            self._metadata['Birth'] = datetime.datetime.utcfromtimestamp(birth_datetime).\
                strftime("%Y-%m-%d %H:%M:%S UTC")
        else:
            logger: Logger = logging.getLogger(__name__)
            logger.info(f"The platform '{platform.system()}' does not support st_birthtime.")


class FileDirectoryPath(MacArtefact):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        # result = run_terminal_command(['mdfind', self._get_mdfind_parameter(filename)])
        pass
