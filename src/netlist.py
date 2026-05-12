class Netlist:

    def __init__(self):

        self.nodes = []

        self.connections = []


    # -------------------------
    # ADD NODE
    # -------------------------
    def add_node(
        self,
        lut_name,
        logic_type,
        inputs
    ):

        self.nodes.append({

            "lut": lut_name,

            "logic": logic_type,

            "inputs": inputs
        })


    # -------------------------
    # BUILD CONNECTIONS
    # -------------------------
    def build_connections(self):

        self.connections = []


        lut_names = [

            node["lut"]

            for node in self.nodes
        ]


        for node in self.nodes:

            current_lut = node["lut"]


            for input_signal in node["inputs"]:

                if input_signal in lut_names:

                    self.connections.append(

                        (
                            input_signal,
                            current_lut
                        )
                    )


    # -------------------------
    # SHOW NETLIST
    # -------------------------
    def show_netlist(self):

        print(
            "\nFPGA HDL Netlist:\n"
        )


        for node in self.nodes:

            print(

                node["lut"],
                "=",
                node["logic"],
                "(",
                ",".join(node["inputs"]),
                ")"
            )


        print(
            "\nNetlist Connections:\n"
        )


        for connection in self.connections:

            print(
                connection[0],
                "->",
                connection[1]
            )