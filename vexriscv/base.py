#!/usr/bin/env python3

# Port of lab003 from FPGA 101 for the Alchitry Cu board

from migen import *

from litex.build.generic_platform import *
from litex_boards.platforms import alchitry_cu

from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores.uart import UARTWishboneBridge

from litex.soc.cores import gpio

kB = 1024
mB = 1024*kB

# GPIO -------------------------------------------------------------------------------------------

class Led(gpio.GPIOOut):
    pass

# Design -------------------------------------------------------------------------------------------

# Create our platform (fpga interface)


platform = alchitry_cu.Platform()

# Create our soc (fpga description)
class BaseSoC(SoCCore):
    def __init__(self, platform):
        sys_clk_freq = int(100e6)

        # SoC with CPU
        SoCCore.__init__(self, platform,
            cpu_type                 = "serv",
            clk_freq                 = 100e6,
            ident                    = "LiteX CPU Test SoC", ident_version=True,
            integrated_rom_size      = 0,
            integrated_sram_size     = 2*kB)

        # Clock Reset Generation
        self.submodules.crg = CRG(platform.request("clk100"), ~platform.request("cpu_reset"))

        # Led
        # self.leds = LedChaser(pads=platform.request_all("user_led"), sys_clk_freq=sys_clk_freq)
        user_leds = Cat(*[platform.request("user_led", i) for i in range(8)])
        self.submodules.leds = Led(user_leds)
        self.add_csr("leds")

soc = BaseSoC(platform)

# Build --------------------------------------------------------------------------------------------

builder = Builder(soc, output_dir="build", csr_csv="test/csr.csv")
builder.build(build_name="top")
