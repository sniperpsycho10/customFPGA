# CustomFPGA

A software-based FPGA architecture simulator built completely in Python.

This project recreates the internal architecture of an FPGA including:

- LUT (Look-Up Table) logic blocks
- Routing fabric
- Switch box architecture
- FPGA grid topology
- Signal propagation engine
- Animated signal visualization
- Runtime FPGA reconfiguration

The goal of this project is to deeply understand how real FPGA hardware works internally.

---

# Project Goals

This simulator focuses on FPGA architecture rather than only HDL programming.

The project models:

- FPGA logic computation
- Programmable interconnects
- Switch matrices
- Grid topology
- Propagation timing
- Hardware-style execution cycles
- Signal movement visualization

---

# Current Progress

---

# Phase 1 — LUT Architecture ✅

Implemented:

- 4-input programmable LUTs
- LUT object-oriented architecture
- Binary-address LUT evaluation
- Multi-LUT signal flow
- Inter-LUT communication

### Features

- Reusable LUT blocks
- Dynamic LUT inputs/outputs
- Modular logic-cell architecture

---

# Phase 2 — Routing Architecture ✅

Implemented:

- Programmable routing tables
- Automatic routing engine
- FPGA-style signal propagation
- Multi-destination routing
- FPGA fabric manager

### Features

- Dynamic routing
- Fanout architecture
- Scalable FPGA fabric
- Automatic signal movement

---

# Phase 3 — Switch Box Architecture ✅

Implemented:

- Programmable switch matrices
- Runtime route enable/disable
- Dynamic reconfiguration
- Selective fanout control

### Features

- SwitchBox class
- Runtime routing control
- Programmable interconnect switching

---

# Phase 4 — FPGA Grid Architecture ✅

Implemented:

- 2D FPGA topology
- LUT physical placement
- Neighbor-aware architecture
- Grid-based routing
- Basic FPGA visualization

### Features

- Spatial LUT organization
- Physical FPGA coordinates
- Neighbor detection
- Topology-aware routing
- Matplotlib FPGA visualization

---

# Phase 5 — Signal Propagation Engine ✅

Implemented:

- Simulation cycles
- Delayed signal routing
- Signal event queue
- Hardware-style propagation
- Animated signal movement
- LUT activation animation

### Features

- Propagation timing engine
- Cycle-based FPGA execution
- Live signal animation
- Route traversal visualization
- Dynamic LUT activation
- Real-time FPGA updates

---

# Project Structure

```text
CustomFPGA/
│
├── assets/
├── configs/
├── docs/
├── fpga_env/
├── src/
│   ├── fabric.py
│   ├── lut.py
│   ├── main.py
│   ├── routing.py
│   ├── signal_engine.py
│   └── switchbox.py
│
├── tests/
├── README.md
└── requirements.txt