class InstructionWrapper:
    def __init__(self, instruction, parentinstrutction, instructionid: 'int > 0', placeholdername: str = ''):
        self._instruction = instruction
        self._parentinstruction = parentinstrutction
        self._instructionid = instructionid
        self._instructionchildren = []
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
