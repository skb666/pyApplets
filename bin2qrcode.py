from PIL import Image
import re
x = 25
y = 25
im = Image.new("RGB",(x,y))
data = open('qrcode.txt').read()
for i in range(0,x):
    for j in range(0,y):
        line = data[i*x+j]
        if line == '1':
            im.putpixel((i,j),(0,0,0))
        else:
            im.putpixel((i,j),(255,255,255))
im.show()
