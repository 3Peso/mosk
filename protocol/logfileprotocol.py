import logging
import re
from datetime import date
from glob import glob

from baseclasses.protocol import ProtocolBase


class LogFileProtocol(ProtocolBase):
    _protocolfilename = ''
    _date = None
    _artefactlogger: logging.Logger = logging.getLogger('LogFile Protocol Artefact')
    _messagelogger: logging.Logger = logging.getLogger('LogFile Protocol Message')
    _protocolfiletype = 'txt'

    def __init__(self, examiner, artifactid='', filedate=date.today(), taskid=''):
        super().__init__(artifactid=artifactid, examiner=examiner, taskid=taskid)
        self._date = filedate
        self._protocolfilename = self.protocol_filename

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

    def writer_protocol_entry(self, entryheader, entrydata):
        if entryheader is not None and entryheader != '':
            self._messagelogger.info('*' * len(entryheader))
            self._messagelogger.info(entryheader)
            self._messagelogger.info('*' * len(entryheader))
        if entrydata is not None and entrydata != '':
            self._artefactlogger.info(entrydata)
        return

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
