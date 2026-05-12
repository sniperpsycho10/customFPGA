# Custom FPGA Architecture Simulator
# Full FPGA CAD + Timing + Routing + 3D Visualization Framework

---

# Introduction

This project is a complete custom FPGA architecture simulator written entirely in Python.

The simulator evolved phase-by-phase from a simple LUT-based logic simulator into a miniature FPGA CAD environment capable of:

- HDL parsing
- Netlist generation
- Logic simulation
- Routing
- Timing analysis
- Congestion analysis
- Pipelining
- Floorplanning
- Placement optimization
- Interactive 3D visualization

The project models many concepts used in real FPGA CAD tools such as:

- Xilinx Vivado
- Intel Quartus
- VPR (Versatile Place and Route)
- academic FPGA research frameworks

The simulator is designed for:
- FPGA architecture learning
- CAD algorithm experimentation
- visualization of digital systems
- educational hardware design exploration

---

# Final Capabilities

By the end of Phase 10, the simulator supports:

---

## Logic Features

- 4-input LUT architecture
- programmable truth tables
- dynamic LUT memory generation
- runtime reconfiguration
- multiple logic gate support

Supported logic:

- AND
- OR
- XOR
- NAND
- NOR
- XNOR
- RANDOM LUT generation

---

## FPGA Fabric Features

- configurable FPGA grid
- LUT placement
- register placement
- floorplanning
- tile-based architecture

---

## Routing Features

- routing graph generation
- automatic routing
- Manhattan routing
- congestion tracking
- routing delay simulation
- routing visualization

---

## Timing Features

- timing-aware routing
- route delays
- critical path analysis
- estimated max clock frequency
- timing closure simulation

---

## Pipeline Features

- pipeline registers
- clocked execution
- synchronous behavior
- clock wave propagation
- stage-by-stage execution

---

## HDL Features

Custom HDL-like syntax:

```text
LUT1 = XOR(A,B)
LUT2 = AND(LUT1,C)
LUT3 = OR(LUT2,D)