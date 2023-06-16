#!/usr/bin/env python3

import time
import random

from litex import RemoteClient

wb = RemoteClient()
wb.open()

for i in range(10):
  wb.regs.plusone_in.write(i)
  plusone = wb.regs.plusone_out.read()
  print(f"{i} + 1 = {plusone}")
  time.sleep(0.1)

wb.close()
