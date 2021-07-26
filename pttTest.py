#
#   This script keys the radio for 3 seconds. Proof of concept.
#
#   Good for checking that you're able to send basic SB9600 commands to the radio
#

import sb9600
import xtl5000

import time

bus = sb9600.Serial("COM2")
xtl = xtl5000.XTL(bus)

bus.ser.flush()

# try PTT
xtl.sendButton(xtl.button_map_o5['ptt'],0x01)
time.sleep(3)
xtl.sendButton(xtl.button_map_o5['ptt'],0x00)