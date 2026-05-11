# CustomFPGA

A software-based FPGA architecture simulator built completely in Python.

This project recreates internal FPGA architecture concepts including:

- LUT logic fabric
- Routing fabric
- Switch box architecture
- FPGA grid topology
- Signal propagation engine
- Runtime FPGA reconfiguration
- Interactive FPGA visualization
- Pseudo-3D FPGA rendering

The goal of this project is to deeply understand how FPGA hardware works internally.

---

# Project Goals

This simulator focuses on FPGA architecture rather than only HDL programming.

The project models:

- FPGA logic computation
- Programmable interconnects
- Switch matrices
- FPGA topology
- Propagation timing
- Runtime FPGA programming
- Signal visualization
- Interactive FPGA rendering

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
- FPGA visualization

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

# Phase 6 — FPGA Configuration System ✅

Implemented:

- Logic abstraction layer
- Runtime FPGA reconfiguration
- JSON FPGA configuration files
- Automatic LUT memory generation
- Runtime LUT programming
- Configurable FPGA architecture

### Supported Configuration Modes

| Mode | Example |
|---|---|
| Logic abstraction | XOR |
| Raw LUT memory | 0,1,1,0 |
| Random LUT generation | RANDOM |

### Features

- JSON FPGA config loader
- Runtime FPGA logic updates
- Dynamic LUT memory replacement
- Live FPGA reprogramming
- Visual FPGA logic labels
- Automatic LUT synthesis behavior

---

# Phase 7 — Advanced Visualization System ✅

Implemented:

- Advanced route visualization
- Interactive FPGA rendering
- Real-time FPGA updates
- Active route highlighting
- Switch-state visualization
- Pseudo-3D FPGA rendering
- Visualization mode switching

### Visualization Features

| Visualization Feature | Status |
|---|---|
| Active route coloring | ✅ |
| Signal propagation animation | ✅ |
| LUT activation pulses | ✅ |
| Runtime reconfiguration visualization | ✅ |
| Interactive rendering | ✅ |
| Pseudo-3D FPGA rendering | ✅ |
| FPGA logic labels | ✅ |

### Supported Visualization Modes

| Mode | Description |
|---|---|
| 2D | Standard FPGA topology |
| 3D | Pseudo-3D FPGA rendering |

---

# Project Structure

```text
CustomFPGA/
│
├── assets/
│
├── configs/
│   └── fpga_config.json
│
├── docs/
├── fpga_env/
│
├── src/
│   ├── configurator.py
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