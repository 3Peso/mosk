"""
mosk localhost module for classes collecting information from output of platform specific tools.
"""

__author__ = '3Peso'

import logging
from os import path

from baseclasses.artefact import MacArtefact
from businesslogic.support import run_terminal_command
from businesslogic.support import validate_file_signature


class PLUtil(MacArtefact):
    """Uses the tool 'PLUtil' to collect information from plist files.
    This is a macOS specific tool.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.tool_path = ""
        super.__init__(*args, **kwargs)

    def _collect(self) -> None:
        if path.exists(self.filepath):
            plutil_path = self.tool_path
            self.data = run_terminal_command(['plutil', '-p', self.filepath])
            self.data[-1].sourcepath = self.filepath
        else:
            self.data = f"File '{self.filepath}' does not exist."

    @property
    def tool_path(self):
        logger = logging.getLogger(__name__)
        if path.exists(self.tool_path):
            return self.tool_path
        else:
            logger.warning("Using 'plutil' from artefact.")
            return 'plutil'

    @tool_path.setter
    def tool_path(self, value):
        logger = logging.getLogger(__name__)
        if path.exists(value) and validate_file_signature(value):
            self.tool_path = value
        else:
            logger.warning(f"Provided tool path '{value}' does not exist.")