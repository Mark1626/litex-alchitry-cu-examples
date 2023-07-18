# Lab 004

**Status:** Tested on board

Building a SoC with a RISC-V VexRiscv CPU

## Instructions

1. Lattice ICE40 HX8K does not have integrated ROM, so we need to be making some adjustments to the design
  * **ROM** We will be using part of the SPIFlash as ROM. We need to offset the start of the rom as the SPIFlash also contains the FPGA bitstream.
  * **SRAM:** HX8K has 4k BRAM blocks so we set the integrated SRAM as 4kB
  * **CPU:** The default variant of VexRiscv did not fit in the ICE40, so a VexRiscv lite was chosen, see https://github.com/SpinalHDL/VexRiscv#area-usage-and-maximal-frequency
  * **Clock Speed:** Since we are using the lite variant our clock frequency also has to be reduced, synthesis was found to pass at 50Mhz.

2. Build the bitstream with `python base.py`

3. Upload the bitstream with `iceprog build/gateware/top.bin`

4. Since the ROM region of the SoC is within the SPIFlash we need to load the bios into the board with `iceprog`
  * `iceprog -o 0x50000 build/software/bios/bios.bin`

5. We can load any bare metal RISC-V application in the same location `0x50000`
  * Build the litex demo with `litex_bare_metal_demo --build-path build --mem rom`
  * `iceprog -o 0x50000 demo.bin`
  * When you connect to the terminal the demo application will start instead of the BIOS as 
  it is at the CPU reset address

**Timing information from different synthesis runs:**

```
# Attempt with sys_clk_freq at 200Mhz
Info: Max frequency for clock '__main___crg_clkout': 60.31 MHz (FAIL at 200.00 MHz)

# Attempt with sys_clk_freq at 100Mhz
Info: Max frequency for clock '__main___crg_clkout': 57.43 MHz (FAIL at 100.00 MHz)

# Attempt with sys_clk_freq at 50Mhz
Info: Max frequency for clock '__main___crg_clkout': 55.76 MHz (PASS at 50.00 MHz)
```
