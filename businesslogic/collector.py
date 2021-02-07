from instructionparsers.xmlparser import XmlParser

from businesslogic.log import mosk_logger
from instructionparsers.wrapper import InstructionWrapper
from baseclasses.artefact import ArtefactBase
from baseclasses.protocol import ProtocolBase
from businesslogic.placeholders import PlaceholderReplacer
from protocol.logfileprotocol import LogFileProtocol


class Collector:
    def __init__(self, parser: XmlParser, protocol: ProtocolBase):
        self._parser = parser
        self._protocol = protocol

    @staticmethod
    def get_collector(instructionsfile: str, examiner: str = ''):
        protocol = LogFileProtocol(examiner)
        xmlparser = XmlParser(instructionsfile, protocol)
        collector = Collector(parser=xmlparser, protocol=protocol)
        return collector

    def collect(self):
        # TODO This currently is only a hack. Needs to be refactored.
        PlaceholderReplacer.set_collect_phase()
        self._document_metadata()
        self._collect_from_instrcutions(self._parser.instructions)

    def _document_metadata(self):
        for metafield in self._parser.metadatafields:
            self._protocol.writer_protocol_entry(entryheader='',
                                                 entrydata="{}: {}"
                                                 .format(metafield, self._parser.get_metadata(metafield)))

    def _collect_from_instrcutions(self, current_instruction: InstructionWrapper, callpath: str = ''):
        if callpath == '':
            callpath = str(current_instruction)
        else:
            callpath = "{}->{}".format(callpath, str(current_instruction))

        # travel down to the leaf elements of the instruction tree
        # which are artefacts
        for child in current_instruction.instructionchildren:
            self._collect_from_instrcutions(child, callpath)

        if isinstance(current_instruction.instruction, ArtefactBase):
            self._collect_and_document(current_instruction.instruction, callpath=callpath)

            if current_instruction.placeholdername != '':
                PlaceholderReplacer.update_placeholder(current_instruction.placeholdername,
                                                       current_instruction.instruction.data)
                mosk_logger.info("Stored artefact data '{}' as placeholder '{}'."
                                 .format(current_instruction.instruction.data,
                                         current_instruction.placeholdername))
        else:
            mosk_logger.debug(callpath)

    def _collect_and_document(self, artefact: ArtefactBase, callpath: str):
        # The following implicitly calls ArtefactBase.collect() because
        # ArtefactBase implements __call__.
        artefact()
        mosk_logger.debug("{} - collected data".format(callpath))
        self._protocol.writer_protocol_entry(entrydata=artefact.getdocumentation(),
                                             entryheader=callpath)
        self._protocol.writer_protocol_entry(entryheader='', entrydata=' ')
        self._protocol.writer_protocol_entry(entrydata=str(artefact), entryheader='')
        self._protocol.writer_protocol_entry(entryheader='', entrydata=' ')

    # TODO document start date
    # TODO document start time
    # TODO document end date
    # TODO document end time
