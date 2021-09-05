"""
mosk localhost module for classes collecting file information.
"""

__author__ = '3Peso'
__all__ = ['FileExistence', 'FileContent', 'ShellHistoryOfAllUsers']

import logging
import os
import shutil
import datetime
from collections import namedtuple
from os import path
from pathlib import Path
from shutil import copyfile

from baseclasses.artefact import ArtefactBase, MacArtefact
from source.localhost import expandfilepath
from businesslogic.support import get_userfolders, md5

TermianlHistory = namedtuple('TerminalHistory', ['Path', 'Content'])


class FileExistence(ArtefactBase):
    """
    Tests if a file exsists under the provided path and returns True or False accordingly.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        filepath = expandfilepath(self.filepath)
        if path.exists(filepath):
            self.data = f"File '{filepath}' exists."
            self.data[-1].sourcepath = filepath
        else:
            self.data = f"File '{filepath}' does not exist."


class FileContent(ArtefactBase):
    """
    Retrieves the file content of a file provided by path. It does NOT copy the file itself. The
    content is stored inside the log created during the collection session.
    """
    _max_file_size = 1024*1024*10 # by default at max 10 MiBs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        filepath = expandfilepath(self.filepath)
        if path.exists(filepath):
            with open(filepath, "r") as filetoload:
                self._read_file(filetoload, filepath)
            self.data[-1].sourcepath = filepath
        else:
            self.data = f"File '{self.filepath}' does not exist."

    def _read_file(self, filetoload, filepath):
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
    _logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        userfolders = set(get_userfolders())
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


class FileCopy(MacArtefact):
    """
    Tries to copy the file in a live session provided by 'filepath'.
    The file copy is stored alongside the collection log. The collection log points to the copied file, but
    does not hold it.
    """
    _destination_directory = '.'

    def __init__(self, *args, **kwargs):
        # Will be filled in super with the property setter filepath.
        self._filepath = ""
        super().__init__(*args, **kwargs)

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        logger = logging.getLogger(__name__)
        if not os.path.exists(value):
            logger.warning(f"File path '{value}' does not exist.")

        self._filepath = expandfilepath(value)

    def _collect(self):
        file_copy_destination = os.path.join(self._ensure_target_directory(), os.path.basename(self.filepath))
        if path.exists(self.filepath):
            copyfile(self.filepath, file_copy_destination)
            self.data = f"Copied file '{self.filepath}' to '{file_copy_destination}'."
            self.data[-1].sourcehash = md5(fpath=self.filepath)
            self.data[-1].sourcepath = self.filepath
        else:
            self.data = f"The file '{self.filepath}' does not exist."
            shutil.rmtree(path.dirname(file_copy_destination), True)

    def _ensure_target_directory(self):
        if not path.exists(self._destination_directory):
            os.mkdir(self._destination_directory)

        unique_dir_name = self._get_unique_directory_name(self._destination_directory, datetime.datetime.now())
        new_unique_directory = os.path.join(self._destination_directory, unique_dir_name)
        os.mkdir(new_unique_directory)

        return new_unique_directory

    def _get_unique_directory_name(self, target_directory, datetime):
        logger = logging.getLogger(__name__)
        # Assume, target directory exists.
        # REMARKS: This only works correct on macOS and Linux.
        filename = path.basename(self.filepath)
        timestamp = f"{datetime.year}{str(datetime.month).zfill(2)}{str(datetime.day).zfill(2)}" \
                    f"{str(datetime.hour).zfill(2)}{str(datetime.minute).zfill(2)}{str(datetime.second).zfill(2)}"

        unique_name = f"{filename}_{timestamp}{str(1).zfill(2)}"
        max_counter = 99
        for counter in range(2,max_counter+1):
            if not path.exists(path.join(target_directory, unique_name)):
                break
            else:
                unique_name = f"{filename}_{timestamp}{str(counter).zfill(2)}"

            if counter == max_counter:
                logger.warning("Max counter reached.")
                raise OverflowError("Max counter reached. Consider less calling 'FileCopy' collectors.")

        return unique_name


class FileMetadata(MacArtefact):
    """
    Tries to collect as much metadata to a target file, as possible.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        pass