class InstructionWrapper:
    # TODO parentinstrcution currently is not used anywhere. Is it really needed?
    def __init__(self, instruction, parentinstrutction, instructionid: 'int > 0', placeholdername: str = ''):
        self._instruction = instruction
        self._parentinstruction = parentinstrutction
        self._instructionid = int(instructionid)
        self._instructionchildren = []
        # The placeholder name will be used in the placeholder cache to store the results of the
        # collection of the instruction in the objects of the wrapper class. The results should be
        # scalar results, but this is currently not enfored.s
        self._placeholdername = placeholdername

    def __str__(self):
        return "{}:{}".format(self.instructionname, self._instructionid)

    @property
    def instruction(self):
        return self._instruction

    @property
    def instructionname(self):
        return type(self._instruction).__name__

    @property
    def instructionid(self):
        return self._instructionid

    @property
    def instructionchildren(self):
        return self._instructionchildren

    @property
    def placeholdername(self):
        return self._placeholdername

    def addchild(self, child):
        self._instructionchildren.append(child)
