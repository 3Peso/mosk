import logging

from baseclasses.artefact import ArtefactBase
from businesslogic.placeholders import Placeholder


class DebugPlaceholder(ArtefactBase):
    def _collect(self):
        try:
            self.data = Placeholder.get_placeholder(self._placeholder)
        except KeyError:
            self.data = f"The placeholder '{self._placeholder}' has not been initialized yet."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._placeholder = self.get_parameter('placeholder')