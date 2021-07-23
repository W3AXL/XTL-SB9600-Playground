#
#   This script emulates a press of the backlight button on the O5 control head
#
#   Good for checking that you're able to send basic SB9600 commands to the radio
#

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