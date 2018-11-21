import time,os
try:
    from pynput import mouse
except ModuleNotFoundError:
    os.system('"%s\\python.exe" -m pip install pynput --user'%os.path.dirname(sys.executable))
    from pynput import mouse

location='d:/截获/鼠标键盘/'
try:
    os.makedirs(location)
except:
    pass

def move(x,y):
    tim=time.localtime()
    name='%02d_%02d_%02d_%02d_%02d'%(tim.tm_mon,tim.tm_mday,tim.tm_hour,tim.tm_min,tim.tm_sec)
    with open('%s鼠标.txt'%location,'a') as f_obj:
        f_obj.write(f'{name}\t鼠标位置:{(x,y)}\n')

def click(x,y,button,pressed):
    tim=time.localtime()
    name='%02d_%02d_%02d_%02d_%02d'%(tim.tm_mon,tim.tm_mday,tim.tm_hour,tim.tm_min,tim.tm_sec)
    with open('%s鼠标.txt'%location,'a') as f_obj:
        f_obj.write(f"{name}\t{'按下' if pressed else '释放'}{str(button).split('.')[1]}:{(x,y)}\n")

def scroll(x,y,dx,dy):
    tim=time.localtime()
    name='%02d_%02d_%02d_%02d_%02d'%(tim.tm_mon,tim.tm_mday,tim.tm_hour,tim.tm_min,tim.tm_sec)
    with open('%s鼠标.txt'%location,'a') as f_obj:
        f_obj.write(f"{name}\t鼠标滚轮:{'向下' if dy<0 else '向上'}{(x,y)}\n")

with mouse.Listener(
        on_move=move,
        on_click=click,
        on_scroll=scroll) as listener:
    listener.join()
