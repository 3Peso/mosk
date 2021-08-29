from baseclasses.artefact import ArtefactBase


class ExceptionArtefactMockup(ArtefactBase):
    def _collect(self):
        raise ValueError("There is something wrong with your values.")
