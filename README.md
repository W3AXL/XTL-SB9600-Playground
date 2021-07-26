# XTL-SB9600-Playground
experiments with SB9600 on the XTL series

### Connecting to the SB9600 Bus
You'll need a RIB of some flavor. Either genuine or aftermarket. RIBless cables are probably doable but I'll figure that out later.
```
RIB DB25 Pin    XTL J2 Pin
--------------------------
BUS+ (15/24)    BUS+ (2)
BUS- (11/13)    BUS- (3)
/BUSY (6)       BUSY (9)
```

This is what I used to connect my RIB to the XTL. Seems to work fine. Not sure if the SB9600 RESET line is necessary. The DSM says it's only used for collision mitigation.

### Using the Python Scripts

You'll need a python 3 installation and pyserial installed via pip.

The ```listener.py``` script will print out any SB9600 or SBEP messages, and decode them if they're recognized. Simply change the COM port in the script and run it. Exit with Ctrl+C

```console
  Btn/Knob >>: ptt pressed
Chan State >>: Transmit ON
   Unknown >>: Unknown message for radio module (0x01): func 0x1a, params 0x0 0x0
   Channel >>: Idle state
  Btn/Knob >>: hub released
   Unknown >>: Unknown message for radio module (0x01): func 0x19, params 0x0 0x1
 SBEP Icon >>: led_red (0x10) icon on
   Unknown >>: Unknown message for radio module (0x01): func 0x3c, params 0xb 0x1
   Unknown >>: Unknown message for radio module (0x01): func 0x3c, params 0xa 0x0
     Audio >>: Unmuted
Chan State >>: Monitor OFF
     Audio >>: Muted
  Btn/Knob >>: ptt released
Chan State >>: Transmit OFF
  Btn/Knob >>: hub pressed
Chan State >>: Monitor ON
   Unknown >>: Unknown message for radio module (0x01): func 0x19, params 0x0 0x0
   Unknown >>: Unknown message for radio module (0x01): func 0x3c, params 0xb 0x0
 SBEP Icon >>: led_red (0x10) icon off
```

The other included py files are the support libraries for SB9600. They were originally pulled from https://paulbanks.org/projects/sb9600/. 
