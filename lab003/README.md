# Lab003

**Status:** Tested on board

Adding a custom core as a MMIO peripheral in the SoC

## Instructions

1. We are going to create a custom core and add it as a MMIO peripheral. For this example we are not going to be using a CPU

2. The PlusOne core is added as a submodule to the SoC

3. Build the bitstream with `python base.py`

4. litex_server --uart --uart-port=/dev/<USB-port>

5. cd test # Must be within the folder of csv.csv

6. Let's test the leds peripherals in the SoC
  - python test_plusone.py
