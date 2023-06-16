#!/usr/bin/env python3

import time
import random

from litex import RemoteClient

wb = RemoteClient()
wb.open()

# # #

print("CSR Registers")
for k, v in wb.regs.d.items():
  print(k, v)

print("Memory Regions")
for k, v in wb.mems.d.items():
  print(k, v)

wb.close()
