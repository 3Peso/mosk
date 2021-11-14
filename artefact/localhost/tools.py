"""
mosk localhost module for classes collecting information from output of platform specific tools.
"""

__author__ = '3Peso'

from os import path

from baseclasses.artefact import MacArtefact
from businesslogic.support import run_terminal_command
from businesslogic.errors import CollectorParameterError
from baseclasses.artefact import FileClass, ToolClass


class PLUtil(MacArtefact, FileClass, ToolClass):
    """Uses the tool 'PLUtil' to collect information from plist files.
    This is a macOS specific tool.
    """

    def __init__(self, *args, **kwargs) -> None:
        self._tool_path = ""
        self._default_tool = "plutil" # The _default_tool attribute is used inside ToolClass
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        try:
            if not path.exists(self.source_path):
                self.data = f"File '{self.source_path}' does not exist."
                return
        except AttributeError:
            raise(CollectorParameterError("No 'filepath' parameter provided."))

        plutil_path = self.tool_path
        self.data = run_terminal_command([plutil_path, '-p', self.source_path])
        self.data[-1].sourcepath = self.source_path
        if plutil_path == 'plutil':
            self.data = \
                "WARNING: No own copy of 'PLUtil' provided. 'PLUtil' of the live artefact has been used."
