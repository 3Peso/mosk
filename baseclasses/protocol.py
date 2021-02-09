from abc import abstractmethod, ABCMeta


class Protocol(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'write_protocol_entry') and
                callable(subclass.write_protocol_entry) and
                hasattr(subclass, 'task_id') and
                callable(subclass.task_id) and
                hasattr(subclass, 'artifactid') and
                callable(subclass.artifactid) and
                hasattr(subclass, 'examiner') and
                callable(subclass.examiner))


class ProtocolBase(Protocol):
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
