#! /usr/bin/env python3
# Parse serial data stream from Honeywell HPMA115S0 particulates detector

import serial, sys
serialdev = "/dev/ttyUSB0"
try:
    ser = serial.Serial(serialdev, 9600, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False)
except:
    print("failed to open serial device %s" % (serialdev))
    sys.exit()

# HPMA115S0 sends 32 byte packets starting with 0x42,0x4D so just shift in incoming
# characters from the end until the first two are 0x42 and 0x4D, then pick the pm2.5
# and pm10 values out. They're represented as two bytes each but range is only 0-1000
# according to the datasheet. 
# Checksum is sum of all bytes except checksum chars (last two) mod 65536

buf = [0] * 32
while True: 
    try:
        buf = buf[1:32] # chop off the first position
        buf.append(ord(ser.read())) # add new value to the end
        if (buf[0] == 0x42) and (buf[1] == 0x4d):
            csum = sum(buf[0:30]) % 65536      # sum of bytes
            csumread = buf[30] * 256 + buf[31] # expected checksum
            pm25  = buf[6] * 256 + buf[7]
            pm10 = buf[8] * 256 + buf[9]
            if csum == csumread:
                print("pm2.5 = %d , pm10 = %d , checksum %04x ok" % (pm25, pm10, csum))
            else:
                print("checksum fail %04x != %04x" % (csum, csumread))
    except:
        raise
