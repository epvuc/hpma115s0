# hpma115s0
Parse the serial data stream from Honeywell HPMA115S0 series particulate detectors

This is a halfassed implementation in python for reading the datastream of this sensor.
This is for the non-"Compact" version only, the "Compact" version's data format is
trivially different. 

The device takes 5VDC power and communicates by async serial at 9600 bps. It has a
few commands you can send it, none of which I've implemented, because by default on
power-up it just starts streaming 32 byte data packets once per second which is all
I care about. 

Bytes 0 and 1 are the start-of-packet identifier, 0x42 0x4D. Bytes 30 and 31 are the
packet checksum which should be the sum of all the other bytes (including the start
bytes) mod 65536. 

Bytes 6 and 7 are the pm2.5 value in uG/m^3, big-end first, and bytes 8 and 9 are pm10.
