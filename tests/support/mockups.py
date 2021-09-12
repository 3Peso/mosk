from baseclasses.artefact import ArtefactBase


class ExceptionArtefactMockup(ArtefactBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._supportedplatform = "MamboJamboPlatform"

    def _collect(self):
        raise ValueError("There is something wrong with your values.")


class SimpleArtefactMockup(ArtefactBase):
    def _collect(self):
        return None
