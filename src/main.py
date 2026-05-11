from lut import LUT
from routing import Routing
from fabric import Fabric
from switchbox import SwitchBox
from signal_engine import SignalEngine

import matplotlib.pyplot as plt


# LUT memories
memory1 = [
    0,1,0,1,
    1,0,1,0,
    0,1,1,0,
    1,0,1,1
]

memory2 = [
    1,0,1,0,
    0,1,0,1,
    1,1,0,0,
    0,1,1,0
]

memory3 = [
    0,0,1,1,
    1,1,0,0,
    1,0,1,0,
    0,1,0,1
]


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

routing.add_route(
    "LUT1_OUT",
    ("LUT2", 0)
)

routing.add_route(
    "LUT1_OUT",
    ("LUT3", 2)
)


# Create switchbox
switchbox = SwitchBox()

switchbox.add_switch(
    "LUT1_OUT->LUT2",
    True
)

switchbox.add_switch(
    "LUT1_OUT->LUT3",
    True
)


# Create signal engine
engine = SignalEngine()


# Enable interactive plotting
plt.ion()


# User inputs
a = int(input("Enter A: "))
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

engine.draw_fpga(fabric)

plt.pause(1)


# -------------------
# Cycle 2
# -------------------
engine.run_cycle(2)

print("Signal Propagation Started")


# Animate signal to LUT2
engine.animate_signal(
    fabric,
    "LUT1",
    "LUT2"
)


# Animate signal to LUT3
engine.animate_signal(
    fabric,
    "LUT1",
    "LUT3"
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


# Animate LUT2 activation
engine.animate_lut_activation(
    fabric,
    "LUT2"
)


# Animate LUT3 activation
engine.animate_lut_activation(
    fabric,
    "LUT3"
)


# Compute outputs
y = fabric.luts["LUT2"].compute()

print("LUT2 Output =", y)

z = fabric.luts["LUT3"].compute()

print("LUT3 Output =", z)


# Final FPGA view
engine.draw_fpga(fabric)


plt.ioff()

plt.show()