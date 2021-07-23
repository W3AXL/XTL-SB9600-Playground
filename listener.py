#
#   This script listens for any SB9600/SBEP messages, and tries to decode them
#    
#   the xtl.processMsg() function is where the main handling of messages is done
#

import sb9600
import xtl5000

bus = sb9600.Serial("COM2")
xtl = xtl5000.XTL(bus)

bus.ser.flush()

lastBusy = 0

try:
    while True:
        # Decode serial message
        if bus.ser.in_waiting > 0:
            msg = bus.read(bus.ser.in_waiting)
            xtl.processMsg(msg)
except KeyboardInterrupt:
    exit(0)