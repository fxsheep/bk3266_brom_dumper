#!/usr/bin/env python3
import sys,serial

MAGIC=b"\x01\xe0\xfc"

if len(sys.argv) < 3:
    print("usage: bk3266_dump_brom.py <serial port> <file>")
    exit()

#open serial port
serialPort = serial.Serial(port = sys.argv[1], baudrate=115200,\
    bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

#send echo handshake
length=1
cmd=0
while True:
    serialPort.write(MAGIC+length.to_bytes(1,byteorder='little')+\
        cmd.to_bytes(1,byteorder='little'))
    if (serialPort.read(8) == b"\x04\x0e\x05\x01\xe0\xfc\x01\x00"):
        break

f = open(sys.argv[2],"wb")

#read memory
length=5
cmd=3

i = 0
while (i < 0x4000):
    serialPort.write(MAGIC+length.to_bytes(1,byteorder='little')+\
        cmd.to_bytes(1,byteorder='little')+i.to_bytes(4,byteorder='little'))
    data = list(serialPort.read(15))
    if (len(data) != 15 or data[0] != 0x04 or data[1] != 0x0e):
        continue
    print(data[11:15])
    f.write(bytes(data[11:15]))
    i = i + 4
f.close()
