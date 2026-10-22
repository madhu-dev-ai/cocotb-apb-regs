[![tests](https://github.com/madhu-dev-ai/cocotb-apb-regs/actions/workflows/test.yml/badge.svg)](https://github.com/madhu-dev-ai/cocotb-apb-regs/actions/workflows/test.yml)

# cocotb-apb-regs

A small APB register block (SystemVerilog) verified with cocotb and Python.

## The design

`apb_regs.sv` has 4 registers on an APB slave interface:

| Address | Name    | Access                  |
|---------|---------|-------------------------|
| 0x0     | CTRL    | read/write              |
| 0x4     | DATA    | read/write              |
| 0x8     | STATUS  | read only (always 0xA5) |
| 0xC     | SCRATCH | read/write              |

A bad address, or a write to STATUS, sets `pslverr`.

## The tests

`test_apb.py` has 5 tests:

- test_write_read_ctrl: write a value, read it back
- test_status_read_only: STATUS reads 0xA5 and cannot be changed
- test_bad_address: bad addresses give an error
- test_random_vs_model: 500 random reads and writes checked against a Python model (scoreboard)
- test_coverage_report: counts which (read or write, address) cases were tried, 32 in total, and fails if any case was missed

## Bug story

Bug 1: I changed the DATA write so it went into SCRATCH instead.
test_random_vs_model failed because the DATA read did not match the model.
I fixed the line and all 5 tests passed again.

Bug 2: I made a write to SCRATCH also overwrite CTRL.
The directed tests did not notice, because they never read CTRL after writing SCRATCH.
test_random_vs_model caught it because it mixes reads and writes on every address and compares against the Python model.
test_coverage_report also failed, because the random test stopped early and left some cases untried.
I fixed the line and all 5 tests passed again.

## How to run

```
make
```

Needs: cocotb, Icarus Verilog, make.