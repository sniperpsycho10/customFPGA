from lut import LUT
from routing import Routing
from fabric import Fabric
from switchbox import SwitchBox
from signal_engine import SignalEngine
from configurator import Configurator
from netlist import Netlist

import time


# -------------------------
# HDL DESCRIPTION
# -------------------------

hdl_program = [

    "LUT1 = XOR(A,B)",

    "LUT2 = AND(LUT1,C)",

    "LUT3 = OR(LUT1,D)",

    "LUT4 = XOR(LUT2,LUT3)"
]


# -------------------------
# CONFIGURATION
# -------------------------

configurator = Configurator()

parsed_nodes = configurator.parse_hdl(
    hdl_program
)


# -------------------------
# NETLIST
# -------------------------

netlist = Netlist()


for node in parsed_nodes:

    netlist.add_node(

        node["lut"],

        node["logic"],

        node["inputs"]
    )


netlist.build_connections()

netlist.show_netlist()


# -------------------------
# FABRIC
# -------------------------

fabric = Fabric()

routing = Routing()

switchbox = SwitchBox()


# -------------------------
# CREATE LUTS
# -------------------------

layer = 0
row = 0
column = 0


for node in parsed_nodes:

    lut_name = node["lut"]

    logic_type = node["logic"]


    memory = configurator.logic_to_memory(
        logic_type
    )


    lut = LUT(
        lut_name,
        memory
    )


    fabric.add_lut(
        lut,
        layer,
        row,
        column
    )


    layer = (layer + 1) % 3

    row += 1

    column = (column + 1) % 3


fabric.show_grid()


# -------------------------
# BUILD ROUTING GRAPH
# -------------------------

for source, destination in netlist.connections:

    routing.add_connection(
        source,
        destination
    )


routing.show_graph()


# -------------------------
# AUTO ROUTING
# -------------------------

for source, destination in netlist.connections:

    routing.auto_route(
        source,
        destination
    )


# -------------------------
# ENABLE SWITCHES
# -------------------------

for source, destination in netlist.connections:

    switch_name = (

        source +
        "_OUT->" +
        destination
    )


    switchbox.add_switch(
        switch_name,
        True
    )


# -------------------------
# SIGNAL ENGINE
# -------------------------

engine = SignalEngine(
    visual_mode="3D"
)


# -------------------------
# LUT LABELS
# -------------------------

lut_labels = {}


for node in parsed_nodes:

    lut_labels[
        node["lut"]
    ] = node["logic"]


# -------------------------
# INPUTS
# -------------------------

a = int(input("\nEnter A: "))
b = int(input("Enter B: "))
c = int(input("Enter C: "))
d = int(input("Enter D: "))


input_map = {

    "A": a,

    "B": b,

    "C": c,

    "D": d
}


# -------------------------
# INITIALIZE LUT INPUTS
# -------------------------

for node in parsed_nodes:

    lut_name = node["lut"]

    input_values = []


    for signal_name in node["inputs"]:

        if signal_name in input_map:

            input_values.append(
                input_map[signal_name]
            )

        else:

            input_values.append(0)


    while len(input_values) < 4:

        input_values.append(0)


    fabric.luts[
        lut_name
    ].set_inputs(
        input_values
    )


# -------------------------
# EXECUTION
# -------------------------

routing.reset_congestion()

routing.show_timing_report()

cycle = 1


# -------------------------
# MAIN EXECUTION LOOP
# -------------------------

for node in parsed_nodes:

    engine.run_cycle(
        cycle
    )


    lut_name = node["lut"]


    # -------------------------
    # LUT ACTIVATION ANIMATION
    # -------------------------
    engine.animate_lut_activation(
        fabric,
        routing,
        switchbox,
        lut_name,
        lut_labels
    )


    # -------------------------
    # COMPUTE LUT OUTPUT
    # -------------------------
    output = fabric.luts[
        lut_name
    ].compute()


    print(
        lut_name,
        "Output =",
        output
    )


    # -------------------------
    # INJECT SIGNAL PACKETS
    # -------------------------
    routing.inject_signal(
        lut_name + "_OUT",
        output,
        cycle
    )


    # -------------------------
    # ADVANCE SIGNALS
    # -------------------------
    for step in range(5):

        routing.advance_signals(
            fabric,
            switchbox,
            cycle
        )


        engine.draw_fpga(
            fabric,
            routing,
            switchbox,
            lut_labels,
            active_lut=lut_name
        )


        time.sleep(0.2)


    routing.show_congestion()

    cycle += 1


# -------------------------
# FINAL TIMING FLUSH
# -------------------------

print(
    "\n=========="
)

print(
    "Final Timing Flush"
)

print(
    "=========="
)


while len(routing.signal_queue) > 0:

    engine.run_cycle(
        cycle
    )


    routing.advance_signals(
        fabric,
        switchbox,
        cycle
    )


    engine.draw_fpga(
        fabric,
        routing,
        switchbox,
        lut_labels
    )


    routing.show_congestion()


    time.sleep(0.5)


    cycle += 1


# -------------------------
# FINISHED
# -------------------------

print(
    "\nFPGA Timing Simulation Complete."
)


input(
    "\nPress Enter to close visualization..."
)