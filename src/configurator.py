import random
import json


class Configurator:

    def __init__(self):

        self.logic_library = {

            "AND": [
                0,0,0,1
            ],

            "OR": [
                0,1,1,1
            ],

            "XOR": [
                0,1,1,0
            ],

            "NAND": [
                1,1,1,0
            ],

            "NOR": [
                1,0,0,0
            ],

            "XNOR": [
                1,0,0,1
            ]
        }


    def expand_to_16_bits(
        self,
        base_memory
    ):

        expanded_memory = []

        for i in range(4):

            expanded_memory.extend(
                base_memory
            )

        return expanded_memory


    def generate_memory(
        self,
        config_input
    ):

        config_input = config_input.upper()


        # Logic keyword mode
        if config_input in self.logic_library:

            base_memory = self.logic_library[
                config_input
            ]

            return self.expand_to_16_bits(
                base_memory
            )


        # Random mode
        elif config_input == "RANDOM":

            memory = []

            for i in range(16):

                memory.append(
                    random.randint(0,1)
                )

            return memory


        # Raw LUT memory mode
        else:

            memory = list(
                map(
                    int,
                    config_input.split(",")
                )
            )

            if len(memory) == 4:

                memory = self.expand_to_16_bits(
                    memory
                )

            return memory


    def load_fpga_config(
        self,
        filename
    ):

        with open(filename, "r") as file:

            config_data = json.load(file)

        return config_data