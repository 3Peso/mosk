"""
Collector Module
"""

__version__ = '0.0.4'
__author__ = '3Peso'
__all__ = ['Collector']

import logging
from datetime import datetime
from instructionparsers.xmlparser import XmlParser
from contextlib import suppress

from instructionparsers.wrapper import InstructionWrapper
from baseclasses.artefact import ArtefactBase
from baseclasses.protocol import ProtocolBase
from businesslogic.placeholders import Placeholder
from protocol.logfileprotocol import LogFileProtocol


# TODO There should be a way to provide comments for the protocol by defining them in the instructions file
class Collector:
    """
    The Collector class is the actual part where all the logic of the protocol instance, the instruction parser
    and the collector artefacts is been instantiated and invoked.
    """
    _logger = logging.getLogger(__name__)

    def __init__(self, parser: XmlParser, protocol: ProtocolBase):
        self._parser = parser
        self._protocol = protocol
        self._collectionstart = None
        self._collectionend = None

    @classmethod
    def get_collector(cls, instructionsfile: str, examiner: str = '',
                      placeholderfile: str = Placeholder.get_globalplaceholderfile()):
        Placeholder.set_globalplaceholderfile(placeholderfile)
        protocol = LogFileProtocol(examiner)
        xmlparser = XmlParser(instructionsfile, protocol)
        collector = cls(parser=xmlparser, protocol=protocol)
        return collector

    def collect(self):
        # Log the date and time when collection started.
        self._protocol.collection_start = datetime.now()
        self._protocol.set_task_metadata(self._parser.metadata)
        self._collect_from_instrcutions(self._parser.instructions)
        # Log the date and time when collection ended.
        self._protocol.collection_end = datetime.now()

    def _collect_from_instrcutions(self, current_instruction: InstructionWrapper, callpath: str = ''):
        if callpath == '':
            callpath = str(current_instruction)
        else:
            callpath = "{}->{}".format(callpath, str(current_instruction))

        # travel down to the leaf elements of the instruction tree
        # which are artefacts
        for child in current_instruction.instructionchildren:
            self._collect_from_instrcutions(child, callpath)

        # HACK: This is a rather whaky way of determining if the object is right
        # Another way would be to use 'isinstance' which I try not to use to
        # avoid implementing my own ABC.
        if 'collect' in dir(current_instruction.instruction):
            self._collect_and_document(current_instruction.instruction, callpath=callpath)

            if current_instruction.placeholdername != '':
                Placeholder.update_placeholder(current_instruction.placeholdername,
                                               current_instruction.instruction.data)
                Collector._logger.info("Stored artefact data '{}' as placeholder '{}'.".
                                       format(current_instruction.instruction.data,
                                              current_instruction.placeholdername))
        else:
            Collector._logger.debug(callpath)

    def _collect_and_document(self, artefact: ArtefactBase, callpath: str):
        # The following implicitly calls ArtefactBase.collect() because
        # ArtefactBase implements __call__.
        with suppress(BaseException):
            artefact()
            Collector._logger.debug("{} - collected data".format(callpath))

        self._protocol.writer_protocol_entry(entrydata=artefact.getdocumentation(),
                                             entryheader=callpath)
        self._protocol.writer_protocol_entry(entryheader='', entrydata=' ')

        if artefact.data is None:
            self._protocol.writer_protocol_entry(entrydata="Could not collect data for artefact '{}'\n"
                                                           "due to unhandled exception."
                                                 .format(str(type(artefact))),
                                                 entryheader='')
        else:
            with suppress(TypeError):
                self._protocol.writer_protocol_entry(entrydata=str(artefact), entryheader='')

        self._protocol.writer_protocol_entry(entryheader='', entrydata=' ')
