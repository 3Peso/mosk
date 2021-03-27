__version__ = '0.0.3'
__author__ = '3Peso'
__all__ = ['LogFileProtocol']

import logging
import re
from datetime import date
from glob import glob
from contextlib import suppress

from baseclasses.protocol import ProtocolBase
from baseclasses.artefact import ArtefactBase
from businesslogic.data import CollectionMetaData


class LogFileProtocol(ProtocolBase):
    """
    Class to write a text protocol of the colleted data.
    """

    def __init__(self, examiner, artifactid='', filedate=date.today(), taskid=''):
        super().__init__(artifactid=artifactid, examiner=examiner, taskid=taskid)
        self._date = filedate
        self._protocolfilename = ''
        self._protocolfiletype = 'txt'
        self._protocolfilename = self.protocol_filename

        self._artefactlogger = logging.getLogger('LogFile Protocol Artefact')
        self._messagelogger = logging.getLogger('LogFile Protocol Message')

        self._setup_protocol_logging(self._artefactlogger, self._protocolfilename, formatstring='')
        self._setup_protocol_logging(self._messagelogger, self._protocolfilename, formatstring='')
        return

    @staticmethod
    def _setup_protocol_logging(currlogger: logging.Logger, protocolfilepath,
                                formatstring='%(asctime)s : %(message)s'):
        currlogger.setLevel(logging.INFO)
        currlogger.propagate = False
        filehandler = logging.FileHandler(protocolfilepath)
        filehandler.setLevel(logging.INFO)

        if formatstring != '':
            formatter = logging.Formatter(formatstring)
            filehandler.setFormatter(formatter)

        currlogger.addHandler(filehandler)

    def _get_current_file_counter(self):
        nextcounter = 1
        searchpattern = "*_{}_{}-{:0>2d}-{:0>2d}.{}".format(self._examiner, self._date.year, self._date.month,
                                                            self._date.day, self._protocolfiletype)
        protocols = glob(searchpattern)
        protocols.sort()
        if len(protocols) > 0:
            if m := re.match(r"(\d{5})_\w+_\d{4}-\d{2}-\d{2}\.\w+", protocols[-1]):
                nextcounter = int(m[1])+1
                if nextcounter >= 100000:
                    raise ValueError('You reached the limit of 99999 protocols. Delete old protocols.')
        return nextcounter

    # TODO Refactor. The call currently is horrible
    def _write_protocol_entry(self, entryheader, entrydata):
        if entryheader is not None and entryheader != '':
            self._messagelogger.info('*' * len(entryheader))
            self._messagelogger.info(entryheader)
            self._messagelogger.info('*' * len(entryheader))
        if entrydata is not None and entrydata != '':
            self._artefactlogger.info(entrydata)
        return

    # TODO Think about adding a newline functions
    @property
    def protocol_filename(self):
        if self._protocolfilename == '':
            if self._artifactid:
                name = f"{self._artifactid}_{self._examiner}_{self._date}.{self._protocolfiletype}"
            else:
                name = "{:0>5d}_{}_{}.{}"\
                    .format(self._get_current_file_counter(), self._examiner, self._date, self._protocolfiletype)
        else:
            name = self._protocolfilename

        return name

    def set_task_metadata(self, metadata: CollectionMetaData):
        for metafield in metadata.metadata_fields:
            self._write_protocol_entry(entryheader='',
                                       entrydata="{}: {}"
                                       .format(metafield, metadata.get_metadata(metafield)))

    def store_artefact(self, artefact: ArtefactBase, callpath: str):
        self._write_protocol_entry(entrydata=artefact.getdocumentation(),
                                   entryheader=callpath)
        self._write_protocol_entry(entryheader='', entrydata=' ')

        if artefact.data is None:
            self._write_protocol_entry(entrydata="Could not collect data for artefact '{}'\n"
                                                 "due to unhandled exception."
                                                 .format(str(type(artefact))),
                                                 entryheader='')
        else:
            with suppress(TypeError):
                self._write_protocol_entry(entrydata=str(artefact), entryheader='')

        self._write_protocol_entry(entryheader='', entrydata=' ')

    @property
    def collection_start(self):
        return self._collection_start

    @collection_start.setter
    def collection_start(self, value):
        self._collection_start = value
        self._write_protocol_entry(entryheader='Collection Start', entrydata=value)

    @property
    def collection_end(self):
        return self._collection_end

    @collection_end.setter
    def collection_end(self, value):
        self._collection_end = value
        self._write_protocol_entry(entryheader='Collection End', entrydata=value)

# Protocol Example

# Examiner: amr
# Examination Date: 01.01.2020 MEZ
# Examination Start: 01:01
# Examination End: 02:02
# Task-ID: 21-123456/210-001
# Task Desription: Standarddaten des Asservats feststellen.
#
#########################
# LocalHost->AllUsernames
#########################
# user1
# user2
############################
# LocalHost->CurrentUsername
############################
# Der_Benutzer
# .....
#
#
# Modules and Libraries
#
# Python
# Python 3.8
# glob Version 1.1
# datetime 0.2
# .....
