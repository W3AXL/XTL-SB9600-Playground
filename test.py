#!/bin/env python3

import sb9600
import xtl5000

import time

bus = sb9600.Serial("COM2")
xtl = xtl5000.XTL(bus)

bus.ser.flush()

# command backlight button
xtl.sendButton(xtl.button_map_o5['btn_light'], 0x01)
time.sleep(0.01)
xtl.sendButton(xtl.button_map_o5['btn_light'], 0x00)