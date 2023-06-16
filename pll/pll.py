#!/usr/bin/env python3

from migen import *

from litex.build.generic_platform import *
from litex_boards.platforms import alchitry_cu

# CRG ----------------------------------------------------------------------------------------------

class _CRG(LiteXModule):
    def __init__(self, platform, sys_clk_freq=25e6):
        self.rst    = Signal()
        self.cd_sys = ClockDomain()

        # # #

        # Clk/Rst
        clk100 = platform.request("clk100")
        rst_n = platform.request("cpu_reset")

        # Clock generated from PLL
        self.cd_sys = ClockDomain()

        # PLL
        self.pll = pll = iCE40PLL(primitive="SB_PLL40_CORE")
        self.comb += pll.reset.eq(~rst_n)
        pll.register_clkin(clk100, 100e6)
        pll.create_clkout(self.cd_sys, sys_clk_freq, with_reset=False)


