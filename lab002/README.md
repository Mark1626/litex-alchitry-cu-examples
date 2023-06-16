# Lab 002

SoC example based on Lab003 in FPGA 101 ported for Alchitry Cu

**Status:** Tested on board

## Instructions

1. python base.py

2. iceprog build/gateware/top.v

3. litex_server --uart --uart-port=/dev/<USB-port>

4. cd test # Must be within the folder of csv.csv

5. Let's test the leds peripherals in the SoC 
  - python test_leds.py

6. We can also access the CSR from the litex_cli's GUI interface
  - litex_cli --gui

7. Let's try reading from the the SPI Flash.
  - litex_cli --read 0x10000000 --length 128
  - iceprog -o 0x30000 <somehex.dat>
  - litex_cli --read 0x10030000 --length 128
