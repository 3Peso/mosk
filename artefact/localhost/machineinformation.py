"""
mosk localhost module for classes collecting machine information.
"""

__version__ = '0.0.4'
__author__ = '3Peso'
__all__ = ['MachineName']

import logging
import socket

from baseclasses.artefact import ArtefactBase


class MachineName(ArtefactBase):
    """
    Retrieves the name of the machine running this script.
    """
    _logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)

    def _collect(self):
        self.data = socket.gethostname()
        if self.data is not None:
            MachineName._logger.debug(f"Machine name '{self.data.collecteddata}' has been collected.")
        else:
            MachineName._logger.info("Could not colelct machine name.")
