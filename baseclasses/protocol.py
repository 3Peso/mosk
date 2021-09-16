"""
mosk protocol base class module
"""

__author__ = '3Peso'

from abc import abstractmethod
from baseclasses.artefact import ArtefactBase


class ProtocolBase:
    def __init__(self, examiner: str = '', taskid: str = '', artifactid: str = ''):
        self._examiner: str = str(examiner)
        self._taskid: str = str(taskid)
        self._artifactid: str = str(artifactid)
        self._collection_start: str = None
        self._collection_end: str = None

    @abstractmethod
    def store_artefact(self, artefact: ArtefactBase, callpath: str):
        pass

    @abstractmethod
    def set_task_metadata(self, metadata):
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

    @property
    @abstractmethod
    def collection_start(self):
        pass

    @collection_start.setter
    @abstractmethod
    def collection_start(self, value):
        pass

    @property
    @abstractmethod
    def collection_end(self):
        pass

    @collection_end.setter
    @abstractmethod
    def collection_end(self, value):
        pass
