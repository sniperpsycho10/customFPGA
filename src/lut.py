class LUT:

    def __init__(self, name, memory):
        self.name = name
        self.memory = memory
        self.inputs = []
        self.output = None

    def set_inputs(self, inputs):
        self.inputs = inputs

    def compute(self):

        # Convert input bits into binary string
        binary_address = ""

        for bit in self.inputs:
            binary_address += str(bit)

        # Convert binary string to decimal
        address = int(binary_address, 2)

        # Read LUT memory
        self.output = self.memory[address]

        return self.output