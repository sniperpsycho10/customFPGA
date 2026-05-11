# CustomFPGA

A software-based FPGA architecture simulator built completely in Python.

This project simulates the internal architecture of an FPGA including:

- LUT (Look-Up Table) logic blocks
- Programmable routing fabric
- Signal propagation
- FPGA fabric topology
- Dynamic interconnect architecture

The goal of this project is to understand FPGA internals from an architecture-level perspective rather than only using HDL tools.

---

# Project Goals

This project aims to simulate how real FPGA hardware works internally.

Instead of only writing Verilog/VHDL, this simulator focuses on:

- FPGA logic fabric
- LUT-based computation
- Routing architecture
- Programmable interconnects
- Scalable FPGA topology
- Hardware-style signal propagation

---

# Current Progress

## Phase 1 — LUT Architecture ✅

Implemented:

- 4-input programmable LUTs
- LUT object-oriented architecture
- LUT signal computation
- Binary-address-based LUT evaluation
- Multiple connected LUT objects
- Inter-LUT signal propagation

### Features

- Reusable LUT class
- Dynamic LUT inputs
- Dynamic LUT outputs
- Scalable LUT objects

---

## Phase 2 — Routing Architecture ✅

Implemented:

- Programmable routing tables
- Dynamic signal routing
- Automatic routing engine
- FPGA-style interconnect propagation
- Multi-destination routing (fanout)
- FPGA fabric manager

### Features

- Routing class
- Automatic signal movement
- Multi-LUT routing
- FPGA fabric container
- Scalable routing architecture

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