from lut import LUT
from routing import Routing
from fabric import Fabric
from switchbox import SwitchBox
from signal_engine import SignalEngine
from configurator import Configurator

import matplotlib.pyplot as plt


# Create configurator
configurator = Configurator()


# Load FPGA config
config = configurator.load_fpga_config(
    "../configs/fpga_config.json"
)


# Generate LUT memories
memory1 = configurator.generate_memory(
    config["LUTS"]["LUT1"]
)

memory2 = configurator.generate_memory(
    config["LUTS"]["LUT2"]
)

memory3 = configurator.generate_memory(
    config["LUTS"]["LUT3"]
)


# Display memories
print("\nGenerated LUT Memories:\n")

print("LUT1 =", memory1)
print("LUT2 =", memory2)
print("LUT3 =", memory3)


# Create LUTs
lut1 = LUT("LUT1", memory1)
lut2 = LUT("LUT2", memory2)
lut3 = LUT("LUT3", memory3)


# Create FPGA fabric
fabric = Fabric()

fabric.add_lut(lut1, 0, 0)
fabric.add_lut(lut2, 0, 1)
fabric.add_lut(lut3, 1, 0)


# Create routing
routing = Routing()

for route in config["ROUTES"]:

    source = route[0]
    destination_lut = route[1]
    destination_index = route[2]

    routing.add_route(
        source,
        (
            destination_lut,
            destination_index
        )
    )


# Create switchbox
switchbox = SwitchBox()

for switch_name, switch_state in config[
    "SWITCHES"
].items():

    switchbox.add_switch(
        switch_name,
        switch_state
    )


# Create signal engine
engine = SignalEngine()


# FPGA logic labels
lut_labels = {

    "LUT1": config["LUTS"]["LUT1"],

    "LUT2": config["LUTS"]["LUT2"],

    "LUT3": config["LUTS"]["LUT3"]
}


# Enable plotting
plt.ion()


# FPGA inputs
a = int(input("\nEnter A: "))
b = int(input("Enter B: "))
c = int(input("Enter C: "))
d = int(input("Enter D: "))


# Initialize LUTs
fabric.luts["LUT1"].set_inputs(
    [a,b,c,d]
)

fabric.luts["LUT2"].set_inputs(
    [0,1,0,1]
)

fabric.luts["LUT3"].set_inputs(
    [1,0,0,1]
)


# -------------------
# Cycle 1
# -------------------
engine.run_cycle(1)

x = fabric.luts["LUT1"].compute()

print("LUT1 Output =", x)

engine.draw_fpga(
    fabric,
    lut_labels
)

plt.pause(1)


# -------------------
# Cycle 2
# -------------------
engine.run_cycle(2)

print("Signal Propagation Started")


# Animate signals
engine.animate_signal(
    fabric,
    "LUT1",
    "LUT2",
    lut_labels
)

engine.animate_signal(
    fabric,
    "LUT1",
    "LUT3",
    lut_labels
)


# Route signals
routing.route_signal(
    "LUT1_OUT",
    x,
    fabric,
    switchbox
)


# -------------------
# Cycle 3
# -------------------
engine.run_cycle(3)


# Animate activations
engine.animate_lut_activation(
    fabric,
    "LUT2",
    lut_labels
)

engine.animate_lut_activation(
    fabric,
    "LUT3",
    lut_labels
)


# Compute outputs
y = fabric.luts["LUT2"].compute()

print("LUT2 Output =", y)

z = fabric.luts["LUT3"].compute()

print("LUT3 Output =", z)


engine.draw_fpga(
    fabric,
    lut_labels
)

plt.pause(1)


# -------------------
# Cycle 4
# -------------------
engine.run_cycle(4)

print("\n=== Runtime FPGA Reconfiguration ===")

print("Reprogramming LUT2 from current logic to OR")


# Generate new memory
new_memory = configurator.generate_memory(
    "OR"
)


# Reconfigure LUT2
fabric.luts["LUT2"].memory = new_memory


# Update displayed logic label
lut_labels["LUT2"] = "OR"


print("New LUT2 Memory =")
print(new_memory)


# Animate reconfiguration
engine.animate_lut_activation(
    fabric,
    "LUT2",
    lut_labels
)


# Recompute LUT2
new_output = fabric.luts["LUT2"].compute()

print("Reconfigured LUT2 Output =", new_output)


# Final FPGA view
engine.draw_fpga(
    fabric,
    lut_labels
)

plt.ioff()

plt.show()