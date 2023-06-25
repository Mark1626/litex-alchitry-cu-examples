#

**Steps:**
* cd soc
* python base.py
* iceprog build/gateware/top.v
* cd test # Must be within the folder of csv.csv
* python test_leds.py
* litex_term /dev/ttyUSBX --kernel firmware/firmware.bin --csr-csv test/csv.csv
