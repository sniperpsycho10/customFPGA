from lut import LUT
from routing import Routing
from fabric import Fabric


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


# Create LUT objects
lut1 = LUT("LUT1", memory1)
lut2 = LUT("LUT2", memory2)
lut3 = LUT("LUT3", memory3)


# Create FPGA fabric
fabric = Fabric()


# Add LUTs into fabric
fabric.add_lut(lut1)
fabric.add_lut(lut2)
fabric.add_lut(lut3)


# Display LUTs
print("FPGA Fabric LUTs:")
fabric.show_luts()


# Create routing fabric
routing = Routing()


# Add routes
routing.add_route("LUT1_OUT", ("LUT2", 0))
routing.add_route("LUT1_OUT", ("LUT3", 2))


# Display routes
print("\nRouting Table:")
routing.show_routes()


# User inputs
a = int(input("\nEnter A: "))
b = int(input("Enter B: "))
c = int(input("Enter C: "))
d = int(input("Enter D: "))


# Send inputs into LUT1
fabric.luts["LUT1"].set_inputs([a,b,c,d])


# Initialize other LUTs
fabric.luts["LUT2"].set_inputs([0,1,0,1])
fabric.luts["LUT3"].set_inputs([1,0,0,1])


# Compute LUT1
x = fabric.luts["LUT1"].compute()

print("\nLUT1 Output =", x)


# Route signal automatically
routing.route_signal("LUT1_OUT", x, fabric.luts)


# Compute LUT2
y = fabric.luts["LUT2"].compute()

print("LUT2 Output =", y)


# Compute LUT3
z = fabric.luts["LUT3"].compute()

print("LUT3 Output =", z)