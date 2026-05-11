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
- Layered FPGA architecture
- Intelligent FPGA routing

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
- Intelligent routing systems
- Layered FPGA architecture

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

---

# Phase 2 — Routing Architecture ✅

Implemented:

- Programmable routing tables
- Automatic routing engine
- FPGA-style signal propagation
- Multi-destination routing
- FPGA fabric manager

---

# Phase 3 — Switch Box Architecture ✅

Implemented:

- Programmable switch matrices
- Runtime route enable/disable
- Dynamic reconfiguration
- Selective fanout control

---

# Phase 4 — FPGA Grid Architecture ✅

Implemented:

- 2D FPGA topology
- LUT physical placement
- Neighbor-aware architecture
- Grid-based routing
- FPGA visualization

---

# Phase 5 — Signal Propagation Engine ✅

Implemented:

- Simulation cycles
- Delayed signal routing
- Signal event queue
- Hardware-style propagation
- Animated signal movement
- LUT activation animation

---

# Phase 6 — FPGA Configuration System ✅

Implemented:

- Logic abstraction layer
- Runtime FPGA reconfiguration
- JSON FPGA configuration files
- Automatic LUT memory generation
- Runtime LUT programming
- Configurable FPGA architecture

### Supported LUT Configuration Modes

| Mode | Example |
|---|---|
| Logic abstraction | XOR |
| Raw LUT memory | 0,1,1,0 |
| Random LUT generation | RANDOM |

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

---

# Phase 8 — Advanced FPGA Architecture ✅

Implemented:

- Layered FPGA topology
- 3D FPGA coordinate system
- Vertical routing visualization
- Inter-layer vias
- Graph-based routing
- BFS pathfinding
- Intelligent auto-routing
- Routing congestion tracking
- Multi-node FPGA topology
- Expanded FPGA visualization

### FPGA Architecture Features

| Feature | Status |
|---|---|
| Layered FPGA architecture | ✅ |
| 3D FPGA coordinates | ✅ |
| Inter-layer routing | ✅ |
| Vertical vias | ✅ |
| Routing graph | ✅ |
| BFS routing | ✅ |
| Congestion tracking | ✅ |
| Multi-hop path discovery | ✅ |

---

# Example FPGA Layered Topology

```text
Layer 0:
LUT1 ---- LUT4

Layer 1:
LUT2 ---- LUT5

Layer 2:
LUT3 ---- LUT6