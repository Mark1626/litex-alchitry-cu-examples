#!/usr/bin/env python3

# Port of lab003 from FPGA 101 for the Alchitry Cu board

from migen import *

from litex.build.generic_platform import *
from litex_boards.platforms import alchitry_cu

from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores.uart import UARTWishboneBridge

from litex.soc.cores import gpio

# GPIO -------------------------------------------------------------------------------------------

class Led(gpio.GPIOOut):
    pass

# Design -------------------------------------------------------------------------------------------

# Create our platform (fpga interface)


platform = alchitry_cu.Platform()

# Create our soc (fpga description)
class BaseSoC(SoCMini):
    def __init__(self, platform, **kwargs):
        sys_clk_freq = int(100e6)

        # SoCMini (No CPU, we are controlling the SoC over UART)
        SoCMini.__init__(self, platform, sys_clk_freq, csr_data_width=32,
            ident="My first LiteX System On Chip on Alchitry Cu", ident_version=True)

        # Clock Reset Generation
        self.submodules.crg = CRG(platform.request("clk100"), ~platform.request("cpu_reset"))

        # No CPU, use Serial to control Wishbone bus
        self.submodules.serial_bridge = UARTWishboneBridge(platform.request("serial"), sys_clk_freq)
        self.add_wb_master(self.serial_bridge.wishbone)

        # Led
        user_leds = Cat(*[platform.request("user_led", i) for i in range(8)])
        self.submodules.leds = Led(user_leds)
        self.add_csr("leds")

soc = BaseSoC(platform)

# Build --------------------------------------------------------------------------------------------

builder = Builder(soc, output_dir="build", csr_csv="test/csr.csv")
builder.build(build_name="top")
