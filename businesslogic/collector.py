"""
Collector Module
"""

__author__ = '3Peso'
__all__ = ['Collector']

import logging
from datetime import datetime
from instructionparsers.xmlparser import XmlParser
from contextlib import suppress

from instructionparsers.wrapper import InstructionWrapper
from baseclasses.artefact import ArtefactBase
from businesslogic.placeholders import Placeholder
from protocol.logfileprotocol import LogFileProtocol


# TODO There should be a way to provide comments for the protocol by defining them in the instructions file
class Collector:
    """
    The Collector class is the actual part where all the logic of the protocol instance, the instruction parser
    and the collector artefacts is been instantiated and invoked.
    """
    _logger = logging.getLogger(__name__)

    def __init__(self, parser: XmlParser, protocol):
        self._parser = parser
        self._protocol = protocol
        self._collectionstart = None
        self._collectionend = None
        self._logger.debug("Collector object initialized.")

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

    @property
    def protocol(self):
        return self._protocol

    def _collect_from_instrcutions(self, current_instruction: InstructionWrapper, callpath: str = ''):
        if callpath == '':
            callpath = str(current_instruction)
        else:
            callpath = f"{callpath}->{current_instruction}"

        # travel down to the leaf elements of the instruction tree
        # which are artefacts
        for child in current_instruction.instructionchildren:
            self._collect_from_instrcutions(child, callpath)

        # Artefacts do implement the method '_collect'.
        if '_collect' in dir(current_instruction.instruction):
            self._collect_and_document(current_instruction.instruction, callpath=callpath)

            # if the current instruction contains a "placeholdername" attribute this means
            # there is a placeholder for the global placeholder dictionary which needs to be
            # filled with the result of the current collector, so that following collectors
            # can use this information for their own collection process, like for example the
            # machine name.
            if current_instruction.placeholdername != '':
                Placeholder.update_placeholder(current_instruction.placeholdername,
                                               current_instruction.instruction.data[0].collecteddata)
                Collector._logger.info(
                    f"Stored artefact data '{current_instruction.instruction.data}' as placeholder "
                    f"'{current_instruction.placeholdername}'.")
        else:
            Collector._logger.debug(callpath)

    def _collect_and_document(self, artefact: ArtefactBase, callpath: str):
        # The following implicitly calls ArtefactBase.collect() because
        # ArtefactBase implements __call__.
        # Supress exeptions during collect because we never know what may go wrong.
        # If something goes wrong, there will be nothing collected, but it will be logged
        # that the collection for the collector was not able to collect the data.
        with suppress(BaseException):
            artefact()
            Collector._logger.debug(f"{callpath} - collected data")

        self._protocol.store_artefact(artefact, callpath)
