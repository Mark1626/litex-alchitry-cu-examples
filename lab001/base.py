#!/usr/bin/env python3

# Port of lab002/blinker from FPGA 101 for the Alchitry Cu

from migen import *

from litex_boards.platforms import alchitry_cu

# Create a led blinker module
class Blink(Module):
    def __init__(self, led):
        counter = Signal(26)
        # combinatorial assignment
        self.comb += led.eq(counter[25])

        # synchronous assignement
        self.sync += counter.eq(counter + 1)

platform = alchitry_cu.Platform()

# Get led signal from our platform
led = platform.request("user_led", 0)

# Create our main module
module = Blink(led)

# Build the design
platform.build(module)
