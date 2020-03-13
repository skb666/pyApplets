import struct
import binascii
import os

m = open("flag.png","rb").read()
k=0
for i in range(5000):
    if k==1:
        break
    for j in range(5000):
        c = m[12:16] + struct.pack('>i', i) + struct.pack('>i', j)+m[24:29]
        crc = binascii.crc32(c) & 0xffffffff
        if crc == 0x91918666:
            k = 1
            print(hex(i),hex(j))
            break

