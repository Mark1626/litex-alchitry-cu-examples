#!/usr/bin/env python3

import time
import random

from litex import RemoteClient

wb = RemoteClient()
wb.open()

# # #

for k, v in wb.regs.d.items():
  print(k, v)

length = 32
r = wb.read(0x00000000, length=length, burst="fixed")
for v in r:
    os.write("test.txt", bytes(v.encode("utf-8")))

wb.close()
