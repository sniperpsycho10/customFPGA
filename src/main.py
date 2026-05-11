from lut import LUT
from routing import Routing
from fabric import Fabric
from switchbox import SwitchBox
from signal_engine import SignalEngine
from configurator import Configurator


# -------------------------
# CONFIGURATION
# -------------------------

configurator = Configurator()

config = configurator.load_fpga_config(
    "../configs/fpga_config.json"
)


# -------------------------
# LUT MEMORIES
# -------------------------

memory1 = configurator.generate_memory(
    config["LUTS"]["LUT1"]
)

memory2 = configurator.generate_memory(
    config["LUTS"]["LUT2"]
)

memory3 = configurator.generate_memory(
    config["LUTS"]["LUT3"]
)

memory4 = configurator.generate_memory(
    config["LUTS"]["LUT4"]
)

memory5 = configurator.generate_memory(
    config["LUTS"]["LUT5"]
)

memory6 = configurator.generate_memory(
    config["LUTS"]["LUT6"]
)


print("\nGenerated LUT Memories:\n")

print("LUT1 =", memory1)
print("LUT2 =", memory2)
print("LUT3 =", memory3)
print("LUT4 =", memory4)
print("LUT5 =", memory5)
print("LUT6 =", memory6)


# -------------------------
# CREATE LUTS
# -------------------------

lut1 = LUT("LUT1", memory1)
lut2 = LUT("LUT2", memory2)
lut3 = LUT("LUT3", memory3)
lut4 = LUT("LUT4", memory4)
lut5 = LUT("LUT5", memory5)
lut6 = LUT("LUT6", memory6)


# -------------------------
# CREATE FABRIC
# -------------------------

fabric = Fabric()


# -------------------------
# LAYERED FPGA PLACEMENT
# -------------------------

fabric.add_lut(
    lut1,
    0,
    0,
    0
)

fabric.add_lut(
    lut2,
    1,
    0,
    1
)

fabric.add_lut(
    lut3,
    2,
    1,
    0
)

fabric.add_lut(
    lut4,
    0,
    1,
    1
)

fabric.add_lut(
    lut5,
    1,
    1,
    2
)

fabric.add_lut(
    lut6,
    2,
    2,
    1
)


fabric.show_grid()


# -------------------------
# CREATE ROUTING
# -------------------------

routing = Routing()


# FPGA Routing Graph
routing.add_connection(
    "LUT1",
    "LUT2"
)

routing.add_connection(
    "LUT1",
    "LUT3"
)

routing.add_connection(
    "LUT2",
    "LUT3"
)

routing.add_connection(
    "LUT3",
    "LUT4"
)

routing.add_connection(
    "LUT4",
    "LUT5"
)

routing.add_connection(
    "LUT5",
    "LUT6"
)


routing.show_graph()


# -------------------------
# AUTO ROUTING
# -------------------------

routing.auto_route(
    "LUT1",
    "LUT2"
)

routing.auto_route(
    "LUT1",
    "LUT3"
)

routing.auto_route(
    "LUT1",
    "LUT4"
)

routing.auto_route(
    "LUT1",
    "LUT5"
)

routing.auto_route(
    "LUT3",
    "LUT4"
)

routing.auto_route(
    "LUT4",
    "LUT5"
)

routing.auto_route(
    "LUT5",
    "LUT6"
)

# -------------------------
# SWITCHBOX
# -------------------------

switchbox = SwitchBox()

for switch_name, switch_state in config[
    "SWITCHES"
].items():

    switchbox.add_switch(
        switch_name,
        switch_state
    )


# -------------------------
# SIGNAL ENGINE
# -------------------------

engine = SignalEngine(
    visual_mode="3D"
)


# -------------------------
# LABELS
# -------------------------

lut_labels = {

    "LUT1": config["LUTS"]["LUT1"],

    "LUT2": config["LUTS"]["LUT2"],

    "LUT3": config["LUTS"]["LUT3"],

    "LUT4": config["LUTS"]["LUT4"],

    "LUT5": config["LUTS"]["LUT5"],

    "LUT6": config["LUTS"]["LUT6"]
}


# -------------------------
# INPUTS
# -------------------------

a = int(input("\nEnter A: "))
b = int(input("Enter B: "))
c = int(input("Enter C: "))
d = int(input("Enter D: "))


# -------------------------
# INITIALIZE LUTS
# -------------------------

fabric.luts["LUT1"].set_inputs(
    [a,b,c,d]
)

fabric.luts["LUT2"].set_inputs(
    [0,1,0,1]
)

fabric.luts["LUT3"].set_inputs(
    [1,0,0,1]
)

fabric.luts["LUT4"].set_inputs(
    [0,0,0,0]
)

fabric.luts["LUT5"].set_inputs(
    [0,0,0,0]
)

fabric.luts["LUT6"].set_inputs(
    [0,0,0,0]
)


# -------------------------
# CYCLE 1
# -------------------------

routing.reset_congestion()

engine.run_cycle(1)

x = fabric.luts["LUT1"].compute()

print("LUT1 Output =", x)


engine.draw_fpga(
    fabric,
    routing,
    switchbox,
    lut_labels,
    active_lut="LUT1"
)


# -------------------------
# CYCLE 2
# -------------------------

engine.run_cycle(2)

print("Signal Propagation Started")


# Animate signals
engine.animate_signal(
    fabric,
    routing,
    switchbox,
    "LUT1",
    "LUT2",
    lut_labels
)

engine.animate_signal(
    fabric,
    routing,
    switchbox,
    "LUT1",
    "LUT3",
    lut_labels
)

engine.animate_signal(
    fabric,
    routing,
    switchbox,
    "LUT3",
    "LUT4",
    lut_labels
)

engine.animate_signal(
    fabric,
    routing,
    switchbox,
    "LUT4",
    "LUT5",
    lut_labels
)

engine.animate_signal(
    fabric,
    routing,
    switchbox,
    "LUT5",
    "LUT6",
    lut_labels
)


active_routes = [

    "LUT1_OUT->LUT2",

    "LUT1_OUT->LUT3",

    "LUT1_OUT->LUT4",

    "LUT1_OUT->LUT5",

    "LUT1_OUT->LUT6"
]


# Route signals
routing.route_signal(
    "LUT1_OUT",
    x,
    fabric,
    switchbox
)


engine.draw_fpga(
    fabric,
    routing,
    switchbox,
    lut_labels,
    active_routes=active_routes
)


routing.show_congestion()


# -------------------------
# CYCLE 3
# -------------------------

engine.run_cycle(3)


engine.animate_lut_activation(
    fabric,
    routing,
    switchbox,
    "LUT2",
    lut_labels
)

engine.animate_lut_activation(
    fabric,
    routing,
    switchbox,
    "LUT3",
    lut_labels
)

engine.animate_lut_activation(
    fabric,
    routing,
    switchbox,
    "LUT4",
    lut_labels
)

engine.animate_lut_activation(
    fabric,
    routing,
    switchbox,
    "LUT5",
    lut_labels
)

engine.animate_lut_activation(
    fabric,
    routing,
    switchbox,
    "LUT6",
    lut_labels
)


# Compute outputs
y = fabric.luts["LUT2"].compute()
z = fabric.luts["LUT3"].compute()

u = fabric.luts["LUT4"].compute()
v = fabric.luts["LUT5"].compute()
w = fabric.luts["LUT6"].compute()


print("LUT2 Output =", y)
print("LUT3 Output =", z)
print("LUT4 Output =", u)
print("LUT5 Output =", v)
print("LUT6 Output =", w)


engine.draw_fpga(
    fabric,
    routing,
    switchbox,
    lut_labels,
    active_lut="LUT2"
)


# -------------------------
# CYCLE 4
# -------------------------

engine.run_cycle(4)

print("\n=== Runtime FPGA Reconfiguration ===")

print("Reprogramming LUT2 to OR")


new_memory = configurator.generate_memory(
    "OR"
)


fabric.luts["LUT2"].memory = new_memory

lut_labels["LUT2"] = "OR"


engine.animate_lut_activation(
    fabric,
    routing,
    switchbox,
    "LUT2",
    lut_labels
)


new_output = fabric.luts["LUT2"].compute()

print("Reconfigured LUT2 Output =", new_output)


engine.draw_fpga(
    fabric,
    routing,
    switchbox,
    lut_labels,
    active_lut="LUT2"
)


routing.show_congestion()


input("\nPress Enter to close visualization...")