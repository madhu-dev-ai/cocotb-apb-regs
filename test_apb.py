import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


async def reset(dut):
    dut.psel.value = 0
    dut.penable.value = 0
    dut.pwrite.value = 0
    dut.paddr.value = 0
    dut.pwdata.value = 0
    dut.presetn.value = 0
    for _ in range(3):
        await RisingEdge(dut.pclk)
    dut.presetn.value = 1
    await RisingEdge(dut.pclk)


async def apb_write(dut, addr, value):
    # Setup phase
    dut.psel.value = 1
    dut.penable.value = 0
    dut.pwrite.value = 1
    dut.paddr.value = addr
    dut.pwdata.value = value
    await RisingEdge(dut.pclk)
    # Access phase
    dut.penable.value = 1
    await RisingEdge(dut.pclk)
    err = int(dut.pslverr.value)
    # Back to idle
    dut.psel.value = 0
    dut.penable.value = 0
    dut.pwrite.value = 0
    return err


async def apb_read(dut, addr):
    # Setup phase
    dut.psel.value = 1
    dut.penable.value = 0
    dut.pwrite.value = 0
    dut.paddr.value = addr
    await RisingEdge(dut.pclk)
    # Access phase
    dut.penable.value = 1
    await RisingEdge(dut.pclk)
    data = int(dut.prdata.value)
    err = int(dut.pslverr.value)
    # Back to idle
    dut.psel.value = 0
    dut.penable.value = 0
    return data, err


@cocotb.test()
async def test_write_read_ctrl(dut):
    cocotb.start_soon(Clock(dut.pclk, 10, unit="ns").start())
    await reset(dut)

    err = await apb_write(dut, 0x0, 0x12345678)
    assert err == 0, "write to CTRL should not give an error"

    data, err = await apb_read(dut, 0x0)
    assert err == 0, "read of CTRL should not give an error"
    assert data == 0x12345678, f"CTRL read {data:#x}, expected 0x12345678"

import random


@cocotb.test()
async def test_random_vs_model(dut):
    cocotb.start_soon(Clock(dut.pclk, 10, unit="ns").start())
    await reset(dut)

    # Python model: what the chip should hold
    model = {0x0: 0, 0x4: 0, 0xC: 0}
    writable = [0x0, 0x4, 0xC]

    for i in range(500):
        addr = random.randint(0, 15)

        if random.random() < 0.5:
            # WRITE
            value = random.getrandbits(32)
            err = await apb_write(dut, addr, value)
            if addr in writable:
                model[addr] = value
                assert err == 0, f"op {i}: write to {addr:#x} gave an unexpected error"
            else:
                assert err == 1, f"op {i}: write to {addr:#x} should give an error"
        else:
            # READ
            data, err = await apb_read(dut, addr)
            if addr in writable:
                expected, expected_err = model[addr], 0
            elif addr == 0x8:
                expected, expected_err = 0xA5, 0
            else:
                expected, expected_err = 0, 1
            assert data == expected, f"op {i}: read {addr:#x} got {data:#x}, expected {expected:#x}"
            assert err == expected_err, f"op {i}: read {addr:#x} error {err}, expected {expected_err}"