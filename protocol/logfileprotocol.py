__author__ = '3Peso'
__all__ = ['LogFileProtocol']

import logging
import re
from datetime import date
from glob import glob
from contextlib import suppress
from logging import Logger

from baseclasses.protocol import ProtocolBase
from baseclasses.artefact import ArtefactBase
from businesslogic.data import CollectionMetaData



class LogFileProtocol(ProtocolBase):
    log_file_name_pattern = r"(\d{5})_\w+_\d{4}-\d{2}-\d{2}\.\w+"

    """
    Class to write a text protocol of the colleted data.
    """

    def __init__(self, examiner: str, artifactid: str = '', filedate: date = date.today(), taskid: str = '',
                 own_protocol_filename: str = ''):
        logger: Logger = logging.getLogger(__name__)
        super().__init__(artifactid=artifactid, examiner=examiner, taskid=taskid)
        self._date = filedate
        self._protocolfilename = ''
        self._protocolfiletype = 'txt'
        self._search_pattern = "*_{}_{}-{:0>2d}-{:0>2d}.{}".format(self._examiner, self._date.year, self._date.month,
                                                                   self._date.day, self._protocolfiletype)

        if own_protocol_filename is not None and own_protocol_filename != '':
            logger.debug(f"Using custom protocol log file '{own_protocol_filename}'.")
            self._protocolfilename = own_protocol_filename
        else:
            self._protocolfilename = self.protocol_filename

        self._artefactlogger: Logger = logging.getLogger('LogFile Protocol Artefact')
        self._messagelogger: Logger = logging.getLogger('LogFile Protocol Message')

        self._setup_protocol_logging(self._artefactlogger, self._protocolfilename, formatstring='')
        self._setup_protocol_logging(self._messagelogger, self._protocolfilename, formatstring='')
        return

    @staticmethod
    def _setup_protocol_logging(currlogger: logging.Logger, protocolfilepath: str,
                                formatstring: str ='%(asctime)s : %(message)s'):
        currlogger.setLevel(logging.INFO)
        currlogger.propagate = False
        filehandler = logging.FileHandler(protocolfilepath)
        filehandler.setLevel(logging.INFO)

        if formatstring != '':
            formatter = logging.Formatter(formatstring)
            filehandler.setFormatter(formatter)

        currlogger.addHandler(filehandler)

    @classmethod
    def _get_current_file_counter(cls, searchpattern: str):
        nextcounter: int = 1

        protocols = glob(searchpattern)
        protocols.sort()
        if len(protocols) > 0:
            if m := re.match(cls.log_file_name_pattern, protocols[-1]):
                nextcounter = int(m[1])+1
                if nextcounter >= 100000:
                    raise ValueError('You reached the limit of 99999 protocols. Delete old protocols.')
        return nextcounter

    def _write_protocol_entry(self, entryheader: str, entrydata: str):
        entry = LogFileProtocol._prepare_protocol_entry(entryheader=entryheader, entrydata=entrydata)
        self._write(entry)
        return

    def _write(self, data: str):
        self._messagelogger.info(self._sanitize_data(data))
        return

    @staticmethod
    def _sanitize_data(data: str):
        data = data.lstrip("\r\n").rstrip("\r\n")
        return f"{data}"

    @classmethod
    def _prepare_protocol_entry(cls, entryheader: str, entrydata: str):
        entry: str = ""
        if entryheader is not None and entryheader != '':
            entry = \
                f"{LogFileProtocol._get_header_seperator(entryheader)}\r\n" \
                f"{entryheader}\r\n" \
                f"{LogFileProtocol._get_header_seperator(entryheader)}\r\n"
        if entrydata is not None and entrydata != '':
            entry += f"{entrydata}\r\n"
        return entry

    @classmethod
    def _get_header_seperator(cls, header: str):
        return '*' * len(header)

    @property
    def protocol_filename(self):
        if self._protocolfilename == '':
            if self._artifactid:
                name = f"{self._artifactid}_{self._examiner}_{self._date}.{self._protocolfiletype}"
            else:
                name = "{:0>5d}_{}_{}.{}"\
                    .format(self._get_current_file_counter(self._search_pattern),
                            self._examiner, self._date, self._protocolfiletype)
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
