# Custom FPGA Simulator — Phase 9

## Overview

Phase 9 upgrades the project into a timing-aware HDL-driven FPGA architecture simulator.

The simulator now supports:

- HDL frontend parsing
- Automatic netlist generation
- FPGA routing graph construction
- Segmented signal propagation
- Packet-based routing
- Timing-aware routing delays
- Event-driven timing flush cycles
- Timing visualization
- Congestion tracking
- Animated FPGA routing

The architecture now resembles a simplified FPGA CAD and timing-analysis environment.

---

# Phase 9 Features

---

## 1. HDL Frontend Parser

The simulator now accepts HDL-style FPGA descriptions.

Example:

```python
hdl_program = [

    "LUT1 = XOR(A,B)",

    "LUT2 = AND(LUT1,C)",

    "LUT3 = OR(LUT1,D)",

    "LUT4 = XOR(LUT2,LUT3)"
]