# Litex on Alchitry Cu

This repo contains examples of using Litex on the Alchitry Cu board. I created this repo when I added support for the board in Litex and as there are very few examples for the Alchitry Cu board. 

Some of the examples are ported from the [FPGA 101 repo](https://github.com/litex-hub/fpga_101.git) from Litex hub. Credits to the authors for making this awesome project.

**Prerequisites**

1. Litex - https://github.com/enjoy-digital/litex/wiki/Installation
2. Project ICEStorm

Support for this board was added in https://github.com/litex-hub/litex-boards/pull/510, if your current Litex installation says the board is not available you may need to pull the latest changes in [litex-boards](https://github.com/litex-hub/litex-boards)

## Examples

1. Lab001 - **Blinky:** Blinky example based on Lab002/blinker in FPGA 101
2. Lab002 - **SoC:** SoC example based on Lab003 in FPGA 101 ported for Alchitry Cu
3. Lab003 - Adding a custom core to the SoC
4. Lab004 - SoC with RISC-V CPU

## TODO

1. Update Blinky example with a PLL
2. 
