"""
mosk protocol base class module
"""

__version__ = '0.0.1'
__author__ = '3Peso'

from abc import abstractmethod


class ProtocolBase:
    def __init__(self, examiner='', taskid='', artifactid=''):
        self._examiner = str(examiner)
        self._taskid = str(taskid)
        self._artifactid = str(artifactid)

    @abstractmethod
    def writer_protocol_entry(self, entryheader: str, entrydata: str):
        pass

    @property
    def examiner(self):
        return self._examiner

    @property
    def artifact_id(self):
        return self._artifactid

    @property
    def task_id(self):
        return self._taskid
