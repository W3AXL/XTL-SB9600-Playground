#!/bin/env python3
# GM1200 Controller class
# Copyright (C) 2014 Paul Banks (http://paulbanks.org)
# 
# This file is part of GM1200Controller
#
# GM1200Controller is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GM1200Controller is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GM1200Controller.  If not, see <http://www.gnu.org/licenses/>.
#

from time import sleep
from binascii import hexlify, unhexlify
import sb9600

# Addressable modules
MODULE_BCAST =      0
MODULE_RADIO =      1
MODULE_FRONTPANEL = 5

# Lamp mappings
lamps_map = {
    "L1": 0x0D, "L2RED": 0x0B, "L2GREEN": 0x0C, "L3": 0x01, "L4": 0x02, "L5":
    0x04, "L5B": 0x05, "L6": 0x10, "L7": 0x07, "L8": 0x11, "L9": 0x12, "L10":
    0x13, "L11": 0x0E, "L12": 0x0F, "L13": 0x14, "L14": 0x15, "L15": 0x16,
    "L16": 0x17, "L17": 0x18, "L18": 0x19,
}

# Lamp attributes
LAMP_OFF =    0
LAMP_ON =     1
LAMP_FLASH =  2

# Illumination addresses
ILLUM_MIC =     1 #TODO: A guess - I didn't have a mic attached to verify it!
ILLUM_DISPLAY = 2
ILLUM_BUTTONS = 3

# Control values
BUTTON_DOWN = 1
BUTTON_UP = 0

class XTL:
  """XTL5000 Controller"""

  def __init__(self, bus):
    self.bus = bus

  def CSQ(self):
    """Enter CSQ mode"""
    self.bus.sb9600_send(MODULE_RADIO, 0x02, 0, 0x40)

  def Reset(self):
    self.bus.sb9600_send(MODULE_BCAST, 0x00, 0x01, 0x08)

  def SBEP(self, module):
    """Enter SBEP mode"""
    self.bus.sb9600_send(MODULE_BCAST, 0x12, module, 0x06)
    self.bus.sbep_enter()

  def Display(self, text, offset=0):
    """Send text to display"""

    if len(text) > 14:
      raise ValueError("Text too long!")

    # Build display message
    msg = bytes((0x80, 0x00, len(text), 0x00, offset))
    msg += bytes(text, "ASCII")
    msg += b"\x00" * len(text) # Character attributes

    # Send it
    self.SBEP(MODULE_FRONTPANEL)
    self.bus.sbep_send(0x01, msg)
    self.bus.sbep_leave()

  def Lamp(self, lamp, function):
    """Switch on/off/flash lamp"""
    # If lamp is not an integer, use it as key to look up lampID in map
    if not isinstance(lamp, int):
      lamp = lamps_map[lamp]
    self.SBEP(MODULE_FRONTPANEL)
    self.bus.sbep_send(0x21, bytes((0x01, lamp, function)))
    self.bus.sbep_leave()

  def Illumination(self, illum, level):
    """Change level of illumination"""
    self.bus.sb9600_send(MODULE_FRONTPANEL, illum, level, 0x58)

  def Control(self, controlid, value):
    """Indicate a control use"""
    self.bus.sb9600_send(MODULE_FRONTPANEL, controlid, value & 0xFF, 0x57)

  def ReadEEPROM(self, module, startaddr, endaddr, callback=None):
    """Read EEPROM data. Note: you'll need to reset the radio after this!"""
    self.CSQ()
    bus.wait_for_quiet()
    
    # Select device? (TODO: What is this?)
    # You'll need to reset the radio after this command
    self.bus.sb9600_send(MODULE_BCAST, module, 0x01, 0x08)

    # Must wait some time before entering SBEP mode
    sleep(0.5)
    self.SBEP(MODULE_RADIO)

    # Read the data
    eedata = b''
    chunklen = 0x40
    for addr in range(startaddr, endaddr, chunklen):
      msg = bytes(
          (chunklen, (addr >> 16) & 0xFF, (addr >> 8) & 0xFF, addr & 0xFF))
      self.bus.sbep_send(0x11, msg) 
      op, data = self.bus.sbep_recv()
      if op==0x80: # Reply is EEPROM data
        addr_rx = data[0]<<16 | data[1]<<8 | data[2]
        if addr_rx != addr:
          raise RuntimeError("Unexpected address in reply addr=0x%x" % addr_rx )
        if len(data[3:]) != chunklen:
          raise RuntimeError("Unexpected data length!")
        eedata += data[3:]
      else:
        raise RuntimeError("Unexpected reply op=%d" % op)

      # Notify of progress
      if callback:
        callback(addr)

    # Done with SBEP mode
    self.bus.sbep_leave()

    return eedata

  def Audio(self, enable):
    enable = 1 if enable else 0
    self.bus.sb9600_send(MODULE_RADIO, 0x00, enable, 0x1D)

  def SetRXFrequency(self, frequency):
    """Set the receiver frequency"""
    ch = int( (frequency*1E6 / 6250) - 60000 )
    self.bus.sb9600_send(0x03, (ch>>8) & 0xFF, ch & 0xFF, 0x3F)

  def SetTXFrequency(self, frequency):
    """Set the transmitter frequency"""
    ch = int( (frequency*1E6 / 6250) - 60000 )
    self.bus.sb9600_send(0x02, (ch>>8) & 0xFF, ch & 0xFF, 0x3F)

if __name__=="__main__":
  print("GM1200 controller tester")

  bus = sb9600.Serial("/dev/ttyUSB0")
  gm1200 = GM1200(bus)

  #eedata = gm1200.ReadEEPROM(1, 0, 0x800)
  #f = open("EEDUMP.bin", "wb")
  #f.write(eedata)
  #f.close()

  #gm1200.Reset()
  #bus.wait_for_quiet()

  gm1200.CSQ()
  bus.wait_for_quiet()

  gm1200.SetRXFrequency(433.5) # MHz
  gm1200.SetTXFrequency(433.5) # MHz
  gm1200.Audio(1)

  gm1200.Lamp("L2RED", LAMP_FLASH)
  gm1200.Lamp("L8", LAMP_ON)
  gm1200.Illumination(ILLUM_DISPLAY, 0xd4)
  gm1200.Illumination(ILLUM_BUTTONS, 0xd4)

  msg = "HELLO WORLD   "
  try:
    lamps = [[0x14,0x19],[0x15,0x18],[0x16,0x17]] 
    pos = 0
    while True:
      gm1200.Display(msg[pos:]+msg[0:pos])
      pos+=1
      pos%=14
      for lg in lamps:
        for l in lg:
          gm1200.Lamp(l, LAMP_ON)
        sleep(0.1)
        for l in lg:
          gm1200.Lamp(l, LAMP_OFF)
  except KeyboardInterrupt:
    gm1200.Reset()

