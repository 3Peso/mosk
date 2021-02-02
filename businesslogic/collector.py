from instructionparsers.xmlparser import XmlParser

from businesslogic.log import mosk_logger
from instructionparsers.wrapper import SourceOrArtefactWrapper
from baseclasses.artefact import ArtefactBase
from baseclasses.protocol import ProtocolBase
from businesslogic.placeholders import PlaceholderReplacer


class Collector:
    _parser: XmlParser
    _protocol: ProtocolBase

    def __init__(self, parser: XmlParser, protocol: ProtocolBase):
        self._parser = parser
        self._protocol = protocol

    # This is meant as a callback function for an artefact
    # in case an artefact needs some values from higher up
    # parents
    def call_for_parameter(self, parametername: str):
        # TODO
        return

    def collect(self):
        self._document_metadata()
        self._collect_from_instrcutions(self._parser.instructions)

    def _document_metadata(self):
        for metafield in self._parser.metadatafields:
            self._protocol.writer_protocol_entry(entryheader='',
                                                 entrydata="{}: {}"
                                                 .format(metafield, self._parser.get_metadata(metafield)))

    def _collect_from_instrcutions(self, current_instruction: SourceOrArtefactWrapper, callpath: str = ''):
        if callpath == '':
            callpath = str(current_instruction)
        else:
            callpath = "{}->{}".format(callpath, str(current_instruction))

        # travel down to the leaf elements of the instruction tree
        # which are artefacts
        for child in current_instruction.wrapperchildren:
            self._collect_from_instrcutions(child, callpath)

        if isinstance(current_instruction.soaelement, ArtefactBase):
            self._collect_and_document(current_instruction.soaelement, callpath=callpath)

            if current_instruction.placeholdername != '':
                PlaceholderReplacer.update_placeholder(current_instruction.placeholdername,
                                                       current_instruction.soaelement.data)
                mosk_logger.info("Stored artefact data '{}' as placeholder '{}'."
                                 .format(current_instruction.soaelement.data,
                                         current_instruction.placeholdername))
        else:
            mosk_logger.debug(callpath)

    def _collect_and_document(self, soa: ArtefactBase, callpath: str):
        # The following implicitly calls ArtefactBase.collect() because
        # ArtefactBase implements __call__.
        soa()
        mosk_logger.debug("{} - collected data".format(callpath))
        self._protocol.writer_protocol_entry(entrydata=soa.getdocumentation(),
                                             entryheader=callpath)
        self._protocol.writer_protocol_entry(entryheader='', entrydata=' ')
        self._protocol.writer_protocol_entry(entrydata=soa.data, entryheader='')
        self._protocol.writer_protocol_entry(entryheader='', entrydata=' ')

    # TODO document start date
    # TODO document start time
    # TODO document end date
    # TODO document end time
