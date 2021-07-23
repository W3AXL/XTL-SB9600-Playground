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
RECVD<: knob_chan clicks: 255
RECVD<: Entering SBEP mode to PANEL at 9600 baud
RECVD<: Set text_channel to NOAA Cedar Rpd
RECVD<: Goto CH 18
RECVD<: CH change 18 ACK
RECVD<: Entering SBEP mode to PANEL at 9600 baud
RECVD<: Set text_softkeys to ^ZONE^NUIS^PWR ^SCAN^PROG
RECVD<: Entering SBEP mode to PANEL at 9600 baud
RECVD<: monitor icon on
RECVD<: b'01 00 03 1e 3a'
RECVD<: Entering SBEP mode to PANEL at 9600 baud
RECVD<: None icon on
RECVD<: Audio unmuted
RECVD<: knob_chan clicks: 255
RECVD<: Entering SBEP mode to PANEL at 9600 baud
RECVD<: Set text_channel to 2m Calling
RECVD<: b'01 00 00 1a 44'
RECVD<: b'01 00 00 1e 81'
RECVD<: Audio muted
RECVD<: Entering SBEP mode to PANEL at 9600 baud
RECVD<: None icon off
RECVD<: Goto CH 17
RECVD<: CH change 17 ACK
RECVD<: Entering SBEP mode to PANEL at 9600 baud
RECVD<: Set text_softkeys to ^ZONE^NUIS^PWR ^SCAN^CALL
RECVD<: Entering SBEP mode to PANEL at 9600 baud
RECVD<: low_power icon on
RECVD<: Entering SBEP mode to PANEL at 9600 baud
RECVD<: direct icon on
```

The other included py files are the support libraries for SB9600. They were originally pulled from https://paulbanks.org/projects/sb9600/. 
