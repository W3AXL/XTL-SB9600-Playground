#!/bin/env python3

import sb9600
from gm1200 import *

import time

bus = sb9600.Serial("COM2")
gm1200 = GM1200(bus)

#gm1200.CSQ()

try:
    while True:
        if bus.ser.in_waiting > 0:
            bus.read(bus.ser.in_waiting)
except KeyboardInterrupt:
    #gm1200.Reset()
    exit(0)

#gm1200.Lamp("L2RED", LAMP_FLASH)
#gm1200.Lamp("L8", LAMP_ON)

#gm1200.Illumination(ILLUM_DISPLAY, 0xd4)
#gm1200.Illumination(ILLUM_BUTTONS, 0xd4)



#gm1200.SetRXFrequency(433.5) # MHz
#gm1200.SetTXFrequency(433.5) # MHz