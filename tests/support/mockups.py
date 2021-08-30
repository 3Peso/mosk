from baseclasses.artefact import ArtefactBase


class ExceptionArtefactMockup(ArtefactBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._supportedsystem = "MamboJamboPlatform"

    def _collect(self):
        raise ValueError("There is something wrong with your values.")
