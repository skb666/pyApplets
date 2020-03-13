from tkinter import *
import json
from re import *
from random import *

__author__='SKB666'
__date__='2018-01-20'

def dclx(ck):
    n=randint(0,len(ck.keys()))
    l=0
    for x in ck.keys():
        if l==n:
            c=x
            y=ck[x]
        l+=1
    s=[str(dfg) for dfg in range(len(c))]
    z=''
    while len(s)>1:
        w=randint(0,len(c)-1)
        if str(w) in s:
            s.remove(str(w))
            z+=c[w]
    z+=c[int(s[0])]
    return c,z,y

def find():
    bz=zw=False
    ah=''
    awc=dclx(ck)
    name =var.get() or 'adfasdfasasdasdfsdfsdfsfsdfsdfssas'
    for key in ck.keys():
        if name==key:
            t.delete(1.0,END)
            t.insert(END,"英-->汉:\n\n")
            t.insert(END,name+'  --'+ck[name][:-1])
            bz=True
            break
    if not bz:
        for key in ck.keys():
            zz=compile(r'[ \.a-zA-Z]'+name+r'[ \.a-zA-Z,:]').findall(ck[key])
            if zz:
                ah+=key+'  --'+ck[key][:-1]+'\n\n'
                zw=True
    if ah!='':
        bz=True
    if zw:
        t.delete(1.0,END)
        t.insert(END,"汉-->英:\n\n")
        t.insert(END,ah)
    if not bz:
        if name=='adfasdfasasdasdfsdfsdfsfsdfsdfssas':
            if t.get(1.0,1.4)!='每日一词':
                t.delete(1.0,END)
                t.insert(END,"每日一词:\n\n")
            t.insert(END,awc[0]+'  --'+awc[2][:-1]+'\n\n')
        else:
            t.delete(1.0,END)
            t.insert(END,'未找到！')

def rightKey1(event=None):
    menubar1.post(event.x_root,event.y_root)
def rightKey2(event=None):
    menubar2.post(event.x_root,event.y_root)
def cut_ent(event=None):
    ent.event_generate("<<Cut>>")
def copy_ent(event=None):
    ent.event_generate("<<Copy>>")
def paste_ent(event=None):
    ent.event_generate('<<Paste>>')
def cut_t(event=None):
    t.event_generate("<<Cut>>")
def copy_t(event=None):
    t.event_generate("<<Copy>>")
def paste_t(event=None):
    t.event_generate("<<Paste>>")

with open('word.json') as f_obj:
    ck=json.load(f_obj)

win = Tk()
win.title('单词查找')
win.geometry('+450+200')
win.resizable(width=False, height=False)

menubar1=Menu(win,tearoff=False)
menubar1.add_command(label='剪切',command=cut_ent)
menubar1.add_command(label='复制',command=copy_ent)
menubar1.add_command(label='粘贴',command=paste_ent)
menubar2=Menu(win,tearoff=False)
menubar2.add_command(label='剪切',command=cut_t)
menubar2.add_command(label='复制',command=copy_t)
menubar2.add_command(label='粘贴',command=paste_t)

l6 = Label(win,text='',bg='#00aaff',font=("幼圆",5),width=3).grid(row=1,column=0,sticky='W'+'N'+'S')

root = Frame(win,bg='#00aaff',borderwidth=2)

l1 = Label(root,text='',bg='#00aaff',font=("幼圆",5),height=1).grid(row=0,column=1,sticky='W'+'N'+'E')

fra = Frame(root,bg='#00aaff',borderwidth=2)

l2 = Label(fra,text='输入要查询的内容:',bg='#00aaff',font=("幼圆",15,"bold"),width=16,height=2).grid(row=0,column=1,sticky='W'+'N')

var = StringVar()
ent=Entry(fra, textvariable = var,width=32,font=("幼圆",13,"bold"),bg='#00ddff', fg="#222222")
ent.grid(row=0,column=2,sticky='W'+'N'+'S'+'E')
ent.bind('<Return>',lambda a:find())
ent.bind("<Button-3>",rightKey1)

fra.grid(row=1,column=1)

l3 = Label(root,text='',bg='#00aaff',font=("幼圆",5),height=1).grid(row=2,column=1,sticky='W'+'N'+'E')

t = Text(root,width=48,height=10,font=("幼圆",13,"bold"),bg='#00ddff',fg="white")
t.grid(row=3,column=1,sticky='W'+'N'+'E')
t.bind("<Button-3>",rightKey2)

l4 = Label(root,text='',bg='#00aaff',font=("幼圆",5),height=1).grid(row=4,column=1,sticky='W'+'N'+'E')

Button(root, text="查   找",height=1,font=("幼圆",15,"bold"),bg='RoyalBlue',command =find).grid(row=5,column=1,sticky='W'+'N'+'E')

l5 = Label(root,text='',bg='#00aaff',font=("幼圆",5),height=1).grid(row=6,column=1,sticky='W'+'N'+'E')

root.grid(row=1,column=1)

l7 = Label(win,text='',bg='#00aaff',font=("幼圆",5),width=3).grid(row=1,column=2,sticky='W'+'N'+'S')

a=dclx(ck)
t.insert(END,"每日一词:\n\n")
t.insert(END,a[0]+'  --'+a[2][:-1]+'\n\n')

win.mainloop()