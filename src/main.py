from lut import LUT
from routing import Routing
from fabric import Fabric
from switchbox import SwitchBox
from signal_engine import SignalEngine


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


# Show FPGA grid
fabric.show_grid()


# Create routing
routing = Routing()

routing.add_route("LUT1_OUT", ("LUT2", 0))
routing.add_route("LUT1_OUT", ("LUT3", 2))


# Show routes
print("\nRouting Table:")
routing.show_routes()


# Create switchbox
switchbox = SwitchBox()

switchbox.add_switch("LUT1_OUT->LUT2", True)
switchbox.add_switch("LUT1_OUT->LUT3", True)


# User inputs
a = int(input("\nEnter A: "))
b = int(input("Enter B: "))
c = int(input("Enter C: "))
d = int(input("Enter D: "))


# Set LUT1 inputs
fabric.luts["LUT1"].set_inputs([a,b,c,d])


# Initialize LUT2/LUT3
fabric.luts["LUT2"].set_inputs([0,1,0,1])
fabric.luts["LUT3"].set_inputs([1,0,0,1])


# Compute LUT1
x = fabric.luts["LUT1"].compute()

print("\nLUT1 Output =", x)


# Route signals
routing.route_signal(
    "LUT1_OUT",
    x,
    fabric,
    switchbox
)


# Compute LUT2
y = fabric.luts["LUT2"].compute()

print("LUT2 Output =", y)


# Compute LUT3
z = fabric.luts["LUT3"].compute()

print("LUT3 Output =", z)


# Visualize FPGA
engine = SignalEngine()

engine.draw_fpga(fabric, routing)