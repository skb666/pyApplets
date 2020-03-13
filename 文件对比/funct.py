import os,time,datetime,json
from tkinter import *

#遍历路径
def iterbrowse(path):
    for home, dirs, files in os.walk(path):
        for filename in files:
            yield os.path.join(home, filename)

#把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

#获取文件的大小,结果保留两位小数，单位为MB
def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)

#获取文件的访问时间
def get_FileAccessTime(filePath):
    t = os.path.getatime(filePath)
    return TimeStampToTime(t)

#获取文件的创建时间
def get_FileCreateTime(filePath):
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)

#获取文件的修改时间
def get_FileModifyTime(filePath):
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)

#遍历得到新字典
def get_Newzd(filename):
    lb_ll=0
    lb_z=''
    zd={}
    for filePath in iterbrowse(filename):
        lb=filePath.split('\\')
        lb_l=len(lb)
        if lb_l!=lb_ll or lb_z!=lb[-2]:
            lb_ll=lb_l
            lb_z=lb[-2]
            zfc=''
            for i in range(lb_l-1):
                zfc+=lb[i]+'\\'
            zd[zfc]=[]
        zd[zfc].append(lb[-1])
    return zd