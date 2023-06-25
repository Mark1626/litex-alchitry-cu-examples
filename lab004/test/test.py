#!/usr/bin/env python3

import time
import random

from litex import RemoteClient

wb = RemoteClient()
wb.open()

# Test led
print("Testing Led...")
for i in range(64):
    print(wb.regs.leds_out.read())
    time.sleep(0.2)

wb.close()
