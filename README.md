\[!\[tests](https://github.com/madhu-dev-ai/cocotb-apb-regs/actions/workflows/test.yml/badge.svg)](https://github.com/madhu-dev-ai/cocotb-apb-regs/actions/workflows/test.yml)



\# cocotb-apb-regs



A small APB register block (SystemVerilog) verified with cocotb and Python.



\## The design

`apb\_regs.sv` has 4 registers on an APB slave interface:



| Address | Name    | Access     |

|---------|---------|------------|

| 0x0     | CTRL    | read/write |

| 0x4     | DATA    | read/write |

| 0x8     | STATUS  | read only (always 0xA5) |

| 0xC     | SCRATCH | read/write |



A bad address, or a write to STATUS, sets `pslverr`.



\## The tests

`test\_apb.py` has 5 tests:

\- test\_write\_read\_ctrl: write a value, read it back

\- test\_status\_read\_only: STATUS reads 0xA5 and cannot be changed

\- test\_bad\_address: bad addresses give an error

\- test\_random\_vs\_model: 500 random reads and writes checked against a Python model (scoreboard)

\- test\_coverage\_report: counts which (read or write, address) cases were tried, 32 in total, and fails if any case was missed



\## Bug story

Bug 1: I changed the DATA write so it went into SCRATCH instead.

test\_random\_vs\_model failed because the DATA read did not match the model.

I fixed the line and all 5 tests passed again.



\## How to run

&#x20;   make



Needs: cocotb, Icarus Verilog, make.

