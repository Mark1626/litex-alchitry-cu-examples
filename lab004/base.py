#!/usr/bin/env python3

# Port of lab003 from FPGA 101 for the Alchitry Cu board

from migen import *

from litex.gen import *

from litex.build.generic_platform import *
from litex_boards.platforms import alchitry_cu

from litex.soc.integration.soc_core import *
from litex.soc.integration.soc import SoCRegion
from litex.soc.integration.builder import *
from litex.soc.cores.uart import UARTWishboneBridge

from litex.soc.cores.clock import iCE40PLL
from litex.soc.cores.led import LedChaser

from migen.genlib.resetsync import AsyncResetSynchronizer

kB = 1024
mB = 1024*kB


# CRG -------------------------------------------------------------------------------------------

class _CRG(LiteXModule):
    def __init__(self, platform, sys_clk_freq):
        self.rst    = Signal()
        self.cd_sys = ClockDomain()
        self.cd_por = ClockDomain()
    
        # Clk/Rst
        clk100  = platform.request("clk100")
        rst_n   = platform.request("cpu_reset")

        # Power On Reset
        por_count = Signal(16, reset=2**16-1)
        por_done  = Signal()
        self.comb += self.cd_por.clk.eq(ClockSignal())
        self.comb += por_done.eq(por_count == 0)
        self.sync.por += If(~por_done, por_count.eq(por_count - 1))

        self.pll = pll = iCE40PLL(primitive="SB_PLL40_CORE")
        self.comb += pll.reset.eq(~rst_n) # FIXME: Add proper iCE40PLL reset support and add back | self.rst.
        pll.register_clkin(clk100, 100e6)
        pll.create_clkout(self.cd_sys, sys_clk_freq, with_reset=False)
        self.specials += AsyncResetSynchronizer(self.cd_sys, ~por_done | ~pll.locked)
        platform.add_period_constraint(self.cd_sys.clk, 1e9/sys_clk_freq)

# Design -------------------------------------------------------------------------------------------


# Create our soc (fpga description)
class BaseSoC(SoCCore):
    # mem_map = {**SoCCore.mem_map, **{"spiflash": 0x20000000}}
    def __init__(self, bios_flash_offset, sys_clk_freq=50e6, **kwargs):
        # Create our platform (fpga interface)
        platform = alchitry_cu.Platform()

        # Disable Integrated ROM since too large for iCE40.
        kwargs["integrated_rom_size"]  = 0
        # kwargs["integrated_sram_size"] = 4*kB

        # Set CPU variant / reset address
        # kwargs["cpu_reset_address"] = self.mem_map["spiflash"] + bios_flash_offset

        # SoC with CPU
        SoCCore.__init__(self, platform, sys_clk_freq,
            cpu_type                 = "vexriscv",
            cpu_variant              = "lite+debug",
            ident                    = "LiteX SoC on Alchitry Cu",
            ident_version            = True,
            **kwargs)

        # CRG
        self.submodules.crg = _CRG(platform, sys_clk_freq)

        # SPI Flash --------------------------------------------------------------------------------
        from litespi.modules import W25Q32
        from litespi.opcodes import SpiNorFlashOpCodes as Codes
        self.add_spi_flash(mode="1x", module=W25Q32(Codes.READ_1_1_1), with_master=False)

        # Add ROM linker region --------------------------------------------------------------------
        self.bus.add_region("rom", SoCRegion(
            origin = self.bus.regions["spiflash"].origin + bios_flash_offset,
            size   = 32*kB,
            linker = True)
        )
        self.cpu.set_reset_address(self.bus.regions["rom"].origin)

        # Led
        self.submodules.leds = LedChaser(pads=platform.request_all("user_led"), sys_clk_freq=sys_clk_freq)

        # Serial bridge
        # self.submodules.uart_bridge = UARTWishboneBridge(platform.request("serial"), sys_clk_freq, baudrate=115200)
        # self.add_wb_master(self.uart_bridge.wishbone)

        # user_leds = Cat(*[platform.request("user_led", i) for i in range(8)])
        # self.submodules.leds = Led(user_leds)
        # self.add_csr("leds")

# bios_flash_offset = 0x021000
bios_flash_offset = 0x50000
soc = BaseSoC(bios_flash_offset)

# Build --------------------------------------------------------------------------------------------

builder = Builder(soc, output_dir="build", csr_csv="test/csr.csv", csr_json="test/csr.json")
builder.build(build_name="top")
