import re,time,os
try:
    import psutil
except ModuleNotFoundError:
    os.system('"%s\\python.exe" -m pip install psutil --user'%os.path.dirname(sys.executable))
    import psutil
    
try:
    from PIL import ImageGrab
except ModuleNotFoundError:
    os.system(r'"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\python.exe" -m pip install pillow --user')
    from PIL import ImageGrab

def process(x):
    p=psutil.process_iter()
    for item in p:
        r=str(item)
        if re.search(x,r):
            return 1
    else:
        return 0
i=0
Max=1000
pro='explorer'
location='d:/截获/屏幕/'
try:
    os.makedirs(location)
except:
    pass
while 1:
    a=process(pro)
    print(a)
    if a==1:
        i=len(os.listdir(location))
        if i>=int(Max):
            while 1:
                os.remove('%s%s'%(location,min(os.listdir(location))))
                i=len(os.listdir(location))
                if i==Max-1:break
        print(pro+"已开启")
        im=ImageGrab.grab((0,0,1920,1080))
        tim=time.localtime()
        name='%02d_%02d_%02d_%02d_%02d.jpg'%(tim.tm_mon,tim.tm_mday,tim.tm_hour,tim.tm_min,tim.tm_sec)
        im.save(location+name,'JPEG')
        print(time.ctime()+"图片保存")
        time.sleep(5)
        
    else:
        print(pro+"关闭")
        time.sleep(20)
