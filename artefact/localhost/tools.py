"""
mosk localhost module for classes collecting information from output of platform specific tools.
"""

__author__ = '3Peso'

import logging
from os import path

from baseclasses.artefact import MacArtefact
from businesslogic.support import run_terminal_command
from businesslogic.support import validate_file_signature
from businesslogic.errors import SignatureMatchError, CollectorParameterError
from baseclasses.artefact import FileClass


class PLUtil(MacArtefact, FileClass):
    """Uses the tool 'PLUtil' to collect information from plist files.
    This is a macOS specific tool.
    """

    def __init__(self, *args, **kwargs) -> None:
        self._tool_path = ""
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        try:
            if not path.exists(self.filepath):
                self.data = f"File '{self.filepath}' does not exist."
                return
        except AttributeError:
            raise(CollectorParameterError("No 'filepath' parameter provided."))

        plutil_path = self.tool_path
        self.data = run_terminal_command([plutil_path, '-p', self.filepath])
        self.data[-1].sourcepath = self.filepath
        if plutil_path == 'plutil':
            self.data = \
                "WARNING: No own copy of 'PLUtil' provided. 'PLUtil' of the live artefact has been used."

    @property
    def tool_path(self):
        logger = logging.getLogger(__name__)
        if path.exists(self._tool_path):
            return self._tool_path
        else:
            logger.warning("Using 'plutil' from artefact.")
            return 'plutil'

    @tool_path.setter
    def tool_path(self, value):
        logger = logging.getLogger(__name__)
        if path.exists(value):
            if validate_file_signature(value):
                self._tool_path = value
            else:
                raise SignatureMatchError(f"The provided PLUtil at '{value}' does not match its signature.")
        else:
            logger.warning(f"Provided tool path '{value}' does not exist.")
