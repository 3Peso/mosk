"""Protcol write to write collected data to a tinydb db"""

import tinydb

from baseclasses.protocol import ProtocolBase


class TinyDBProtocol(ProtocolBase):
    """
    Class to store collected data in a tinyDB db.
    """

    def __init__(self, examiner, artifactid='', taskid=''):
        super().__init__(artifactid=artifactid, examiner=examiner, taskid=taskid)

    # TODO
    def set_task_metadata(self, metadata):
        return

    # TODO
    def store_artefact(self, artefact: ArtefactBase, callpath: str):
        return