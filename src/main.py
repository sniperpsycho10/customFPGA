from lut import LUT
from register import Register
from routing import Routing
from fabric import Fabric
from switchbox import SwitchBox
from signal_engine import SignalEngine
from configurator import Configurator
from netlist import Netlist

import time


# =========================================================
# HDL PROGRAM
# =========================================================

hdl_program = [

    "LUT1 = XOR(A,B)",

    "LUT2 = AND(LUT1,C)",

    "LUT3 = OR(LUT2,D)",

    "LUT4 = XOR(LUT3,A)"
]


# =========================================================
# CONFIGURATOR
# =========================================================

configurator = Configurator()

parsed_nodes = configurator.parse_hdl(
    hdl_program
)


# =========================================================
# FPGA OBJECTS
# =========================================================

fabric = Fabric()

routing = Routing()

switchbox = SwitchBox()

netlist = Netlist()

engine = SignalEngine()


# =========================================================
# BUILD NETLIST
# =========================================================

for node in parsed_nodes:

    netlist.add_node(

        node["lut"],

        node["logic"],

        node["inputs"]
    )


netlist.build_connections()


# =========================================================
# CREATE LUTS + REGISTERS
# =========================================================

register_count = 1


for node in parsed_nodes:

    lut_name = node["lut"]

    logic_type = node["logic"]


    # -----------------------------------------------------
    # CREATE LUT MEMORY
    # -----------------------------------------------------

    memory = configurator.logic_to_memory(
        logic_type
    )


    # -----------------------------------------------------
    # CREATE LUT
    # -----------------------------------------------------

    lut = LUT(
        lut_name,
        memory
    )


    fabric.add_lut(
        lut
    )


    # -----------------------------------------------------
    # CREATE REGISTER
    # -----------------------------------------------------

    reg_name = (
        "REG" +
        str(register_count)
    )


    register = Register(
        reg_name,
        pipeline_stage=register_count
    )


    # -----------------------------------------------------
    # PLACE REGISTER NEAR LUT
    # -----------------------------------------------------

    fabric.add_register(

        register,

        parent_lut_name=lut_name
    )


    register_count += 1


# =========================================================
# FORCE-DIRECTED PLACEMENT
# =========================================================

fabric.optimize_placement(
    netlist
)

fabric.snap_to_grid()


# =========================================================
# SHOW NETLIST
# =========================================================

netlist.show_netlist()


# =========================================================
# SHOW FLOORPLAN
# =========================================================

fabric.show_grid()

fabric.show_utilization()


# =========================================================
# BUILD ROUTING GRAPH
# =========================================================

for source, destination in netlist.connections:

    routing.add_connection(
        source,
        destination
    )


routing.show_graph()


# =========================================================
# AUTO ROUTING
# =========================================================

for source, destination in netlist.connections:

    routing.auto_route(
        source,
        destination
    )


# =========================================================
# TIMING REPORT
# =========================================================

routing.show_timing_report()

routing.show_critical_path()


# =========================================================
# SWITCHBOXES
# =========================================================

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


# =========================================================
# LABELS
# =========================================================

lut_labels = {}


for node in parsed_nodes:

    lut_labels[
        node["lut"]
    ] = node["logic"]


for reg_name in fabric.registers:

    lut_labels[
        reg_name
    ] = "PIPE"


# =========================================================
# USER INPUTS
# =========================================================

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


# =========================================================
# INITIALIZE LUT INPUTS
# =========================================================

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


# =========================================================
# PIPELINE EXECUTION
# =========================================================

cycle = 1

pipeline_stage = 1


for node in parsed_nodes:

    engine.run_cycle(
        cycle
    )


    engine.show_pipeline_barrier(
        pipeline_stage
    )


    lut_name = node["lut"]


    # -----------------------------------------------------
    # DRAW FPGA
    # -----------------------------------------------------

    engine.draw_fpga(

        fabric,
        routing,
        switchbox,
        lut_labels,

        active_component=lut_name
    )


    # -----------------------------------------------------
    # COMPUTE LUT
    # -----------------------------------------------------

    output = fabric.luts[
        lut_name
    ].compute()


    print(
        lut_name,
        "Output =",
        output
    )


    # -----------------------------------------------------
    # PIPELINE REGISTER
    # -----------------------------------------------------

    reg_name = (
        "REG" +
        str(pipeline_stage)
    )


    register = fabric.registers[
        reg_name
    ]


    register.load_input(
        output
    )


    print(
        reg_name,
        "Pipeline Loaded =",
        output
    )


    time.sleep(0.5)


    # -----------------------------------------------------
    # CLOCK WAVE
    # -----------------------------------------------------

    engine.animate_clock_wave(

        fabric,
        routing,
        switchbox,
        lut_labels
    )


    # -----------------------------------------------------
    # CLOCK EDGE
    # -----------------------------------------------------

    register.clock_tick()


    print(
        reg_name,
        "Pipeline Output =",
        register.get_output()
    )


    # -----------------------------------------------------
    # INJECT SIGNAL
    # -----------------------------------------------------

    routing.inject_signal(

        lut_name + "_OUT",

        register.get_output(),

        cycle
    )


    # -----------------------------------------------------
    # ADVANCE SIGNALS
    # -----------------------------------------------------

    for step in range(10):

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

            active_component=reg_name
        )


        time.sleep(0.04)


    # -----------------------------------------------------
    # SHOW CONGESTION
    # -----------------------------------------------------

    routing.show_congestion()


    cycle += 1

    pipeline_stage += 1


# =========================================================
# FINAL TIMING FLUSH
# =========================================================

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


    time.sleep(0.08)

    cycle += 1


# =========================================================
# DONE
# =========================================================

print(
    "\nFPGA Floorplanning + Timing Closure Simulation Complete."
)


input(
    "\nPress Enter to close visualization..."
)