"""Protcol write to write collected data to a tinydb db"""

__author__ = "3Peso"
__all__ = ['TinyDBProtocol']

import tinydb

from baseclasses.artefact import ArtefactBase
from baseclasses.protocol import ProtocolBase


class TinyDBProtocol(ProtocolBase):
    """
    Class to store collected data in a tinyDB db.
    """

    def __init__(self, examiner, artifactid='', taskid=''):
        super().__init__(artifactid=artifactid, examiner=examiner, taskid=taskid)

    def set_task_metadata(self, metadata):
        pass

    def store_artefact(self, artefact: ArtefactBase, callpath: str):
        pass
