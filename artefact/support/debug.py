from baseclasses.artefact import ArtefactBase
from businesslogic.placeholders import Placeholder


class DebugPlaceholder(ArtefactBase):
    def _collect(self) -> None:
        try:
            self.data = Placeholder.get_placeholder(self._placeholder)
        except KeyError:
            self.data = f"The placeholder '{self._placeholder}' has not been initialized yet."

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._placeholder: str = self.get_parameter('placeholder')