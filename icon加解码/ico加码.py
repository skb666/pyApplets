import base64,os.path
while 1:
    a=input('图像路径:')
    if a!='q':
        open_icon = open(a,"rb")
        b64str = base64.b64encode(open_icon.read())
        open_icon.close()
        write_data = "%s=%s\n" % (os.path.basename(a).split('.')[0],b64str)
        f = open("icon.py","a")
        f.write(write_data)
        f.close()
    else:
        break
