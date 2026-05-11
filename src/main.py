from lut import LUT


# LUT1 memory
memory1 = [
    0,1,0,1,
    1,0,1,0,
    0,1,1,0,
    1,0,1,1
]


# LUT2 memory
memory2 = [
    1,0,1,0,
    0,1,0,1,
    1,1,0,0,
    0,1,1,0
]


# Create LUT objects
lut1 = LUT("LUT1", memory1)
lut2 = LUT("LUT2", memory2)


# User inputs for LUT1
a = int(input("Enter A: "))
b = int(input("Enter B: "))
c = int(input("Enter C: "))
d = int(input("Enter D: "))


# Send inputs to LUT1
lut1.set_inputs([a,b,c,d])


# Compute LUT1 output
x = lut1.compute()

print("LUT1 Output =", x)


# Send LUT1 output into LUT2
lut2.set_inputs([x,1,0,1])


# Compute LUT2 output
y = lut2.compute()

print("LUT2 Output =", y)