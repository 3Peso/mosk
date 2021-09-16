"""
mosk localhost module for classes collecting machine information.
"""

__author__ = '3Peso'
__all__ = ['MachineName']

import logging
import socket
from logging import Logger

from baseclasses.artefact import ArtefactBase


class MachineName(ArtefactBase):
    """
    Retrieves the name of the machine running this script.
    """
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        self.data = socket.gethostname()
        if self.data is not None:
            MachineName._logger.debug(f"Machine name '{self.data[-1].collecteddata}' has been collected.")
        else:
            MachineName._logger.info("Could not colelct machine name.")
