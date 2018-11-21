from tkinter import *
import json,base64,os
from random import *

__author__='SKB666'
__date__='2018-01-20'


def get_data():
    hh={}
    try:
        with open('class_data.txt','r') as f_obj:
            a=f_obj.readlines()
        for i in a:
            h=i.split(':')
            hh[int(h[0])]=h[1].strip()
        return hh
    except FileNotFoundError:
        return {}

def sc(ahh):
    hhh=get_data()
    xxx=[]
    t.delete(1.0,END)
    for lll in ahh.keys():
        if ahh[lll]==1:
            xxx.append(lll)
    xxx.sort()
    for aa in xxx:
        try:
            hhh[aa]
        except KeyError:
            t.insert(END,str(aa)+'\n')
        else:
            t.insert(END,str(aa)+'\t'+hhh[aa]+'\n')

def scsjs(MI,MA,SL,JG):
    ahh={x:0 for x in range(MI,MA+1)}
    jj=0
    gg=MA-MI+1
    while jj<=SL:
        sjn=randint(MI,MA)
        if ahh[sjn]==0:
            ahh[sjn]=1
            gg-=1
            jj+=1
            if jj>=SL:break
            for i in range(1,JG):
                if sjn+i<=MA:
                    if ahh[sjn+i]==0:
                        ahh[sjn+i]=2
                        gg-=1
                if sjn-i>=MI:
                    if ahh[sjn-i]==0:
                        ahh[sjn-i]=2
                        gg-=1
                if gg<=0:
                    ahh={x:0 for x in range(MI,MA+1)}
                    jj=0
                    gg=MA-MI+1
                    break
    sc(ahh)

def tjpd(event=None):
    a=var1.get()
    b=var2.get()
    c=var3.get()
    d=var4.get()
    try:
        MI=int(a)
        MA=int(b)
        SL=int(c)
        JG=int(d)
    except ValueError:
        t.delete(1.0,END)
        t.insert(END,"请输入:\n'整型'数字!\n")
    else:
        if MI>MA:
            t.delete(1.0,END)
            t.insert(END,"'起始号码'\n应大于\n'终止号码'!\n")
        elif SL>MA-MI+1 or SL<=0:
            t.delete(1.0,END)
            t.insert(END,"'产生数量'\n应小于\n可产生数量!\n(且大于0)\n")
        elif JG<=0:
            t.delete(1.0,END)
            t.insert(END,"'最小间隔'\n应大于0!\n")
        else:
            hh=False
            if SL==1:
                hh=True
            elif JG>((MA-MI)/(SL-1)):
                t.delete(1.0,END)
                t.insert(END,"'最小间隔'\n过大!\n")
            else:
                hh=True
            if hh:scsjs(MI,MA,SL,JG)

img =b'AAABAAEAIEAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAB1kor/dcKs/3XCrP91wqz/dcKs/3XCrP91wqz/dcKs/3XCrP91wqz/dcKs/3XCrP91wqz/dcKs/3XCrP9/w7D/qH24/6FwtP+hcLT/oXC0/6FwtP+hcLT/oXC0/6FwtP+hcLT/oXC0/6FwtP+hcLT/oXC0/6FwtP+hcLT/jHiT/22wnf824bD/NuGw/zbhsP824bD/NuGw/zbhsP824bD/NuGw/zbhsP824bD/NuGw/zbhsP824bD/NuGw/0jjt/+kRMn/mCvC/5grwv+YK8L/mCvC/5grwv+YK8L/mCvC/5grwv+YK8L/mCvC/5grwv+YK8L/mCvC/5grwv+aa6v/bbCd/zbhsP824bD/NuGw/zbhsP824bD/NuGw/zbhsP824bD/NuGw/zbhsP824bD/NuGw/zbhsP824bD/SOO3/6REyf+YK8L/mCvC/5grwv+YK8L/mCvC/5grwv+YK8L/mCvC/5grwv+YK8L/mCvC/5grwv+YK8L/mCvC/5prq/9tsJ3/NuGw/zbhsP824bD/P+Kz/2now/9F47b/NuGw/zbhsP814K//YufB/zbgsP824bD/NuGw/zbhsP9I47f/pETJ/5grwv+YK8L/mCvC/5grwv+gPMb/tWbT/7Rm0v+vWs//nDTE/5grwv+YK8L/mCvC/5grwv+YK8L/mmur/22wnf824bD/NuGw/zbhsP9j58H//////3rry/824bD/NeCv/3/rzP/r+/f/NuCw/zbhsP824bD/NuGw/0jjt/+kRMn/mCvC/5grwv+YK8L/mCvC/7lv1f/////////////////58/v/w4Xb/5grwf+YK8L/mCvC/5grwv+aa6v/bbCd/zbhsP824bD/NuGw/2Pnwf//////euvL/zbgsP+M7dH//f7+/+/8+P824LD/NuGw/zbhsP824bD/SOO3/6REyf+YK8L/mCvC/5grwv+YK8L/uW/V///////NmuH/unLW/+rU8v/+/v7/uXHV/5grwv+YK8L/mCvC/5prq/9tsJ3/NuGw/zbhsP824bD/Y+fB//////9768v/m+/X//7+/v/+/v7/7/z4/zbgsP824bD/NuGw/zbhsP9I47f/pETJ/5grwv+YK8L/mCvC/5grwv+5b9X//////7x21/+YK8L/oT3H//37/f/hwu3/mCvC/5grwv+YK8L/mmur/22wnf824bD/NuGw/zbhsP9j58H//////9358f/+/v7/wfXm/8P15//v/Pj/NuCw/zbhsP824bD/NuGw/0jjt/+kRMn/mCvC/5grwv+YK8L/mCvC/7lv1f//////vHbX/5grwv+YLML/+fT7/+jQ8f+YK8L/mCvC/5grwv+aa6v/bbCd/zbhsP824bD/NuGw/2Pnwf///////v7+/7bz4v854bH/uvTj/+/8+P824LD/NuGw/zbhsP824bD/SOO3/6REyf+YK8L/mCvC/5grwv+YK8L/uW/V//////+8dtf/lyvB/8B92f/+/v7/1Kbl/5grwv+YK8L/mCvC/5prq/9tsJ3/NuGw/zbhsP824bD/Y+fB//7+/v+p8d3/N+Gw/zbhsP+69OP/7/z4/zbgsP814K//QOK0/3nny/+T2N//u5Hm/7dx1/+dNcT/lyrB/5grwv+5b9X//////+7d9f/t2/T//v7+//Hk9/+iQcj/mCvC/5grwv+YK8L/mmur/22wnf824bD/NuGw/zbhsP9g58D/nO/X/zbhsP824bD/NuGw/53w2P/H9uj/NuGw/3TZ0P90g/n/OkH//y00//8tNP//OUD//3d0+v+qatr/mCvC/7Be0P/o0PH/58/x/+DB7f/Ij97/njnF/5grwv+YK8L/mCvC/5grwv+aa6v/bbCd/zbhsP824bD/NuGw/zbhsP824LD/NuGw/zbhsP824bD/NuGw/zbhsP9+ytz/QEb+/y41//8uNf//LjX//y41//8uNf//LjX//z5E/v+jdOP/mCvC/5grwv+YK8L/mCvC/5grwv+YK8L/mCvC/5grwv+YK8L/mCvC/5prq/9tsJ3/NuGw/zbhsP824bD/NuGw/zbhsP824bD/NuGw/zbhsP814bD/b93L/0NK/v93fP//u73//y82//9NU///ZWr//y41//+6vP//io7//0BG/v+pY9b/mCvC/5grwv+YK8L/mCvC/5grwv+YK8L/mCvC/5grwv+YK8L/mmur/22wnf824bD/NuGw/zbhsP824bD/NuGw/zbhsP824bD/NuGw/znhsf96k/X/LTT//5qd///5+v//Mjn//8fJ///f4P//NDv///j4//+xtP//LTT//3909v+ZLcL/mCvC/5grwv+YK8L/mCvC/5grwv+YK8L/mCvC/5grwv+aa6v/bbCd/zbhsP824bD/NuGw/zbhsP824bD/NuGw/zbhsP824bD/ZOfB/05U/v8uNf//mp3///n6//98gP///v7///v7//+Okv//9vb//7G0//8uNf//SE7+/65Zz/+YK8L/mCvC/5grwv+YK8L/mCvC/5grwv+YK8L/mCvC/5prq/99saX/VeHC/1Xhwv9V4cL/VeHC/1Xhwv9V4cL/VeHC/1Xhwv+Y6dr/NDr//y41//+anf///f3///Dw//+tsP//foL///X2///8/P//sbT//y41//8xOP//xpTf/61ayv+tWsr/rVrK/61ayv+tWsr/rVrK/61ayv+tWsr/pIKw/2mSuv8rk/v/K5P7/yuT+/8rk/v/K5P7/yuT+/8rk/v/K5P7/3e4/P82Pf//LjX//5qd////////3N7//zc9//8uNf//u77///////+xtP//LjX//zM6///i4sL/29ug/9vboP/b26D/29ug/9vboP/b26D/29ug/9vboP+2tp7/aJG7/yqT/P8qk/z/KpP8/yqT/P8qk/z/KpP8/yqT/P8qk/z/SKL8/1pg/v8uNf//mp3///f4//9UWv//LjX//y41//8+Rf//6ur//6+x//8uNf//VVr+/9/frP/b26D/29ug/9vboP/b26D/29ug/9vboP/b26D/29ug/7a2nf9okbv/KpP8/yqT/P8qk/z/KpP8/yqT/P8qk/z/KpP8/yqT/P8qkvv/c5H9/y00//+anf//hYn//y00//8uNf//LjX//y41//9pbv//rrD//y00//+aneT/2tqf/9vboP/b26D/29ug/9vboP/b26D/29ug/9vboP/b26D/trad/2iRu/8qk/z/KpP8/yqT/P8qk/z/KpP8/yqT/P8qk/z/KpP8/yqT/P9Lofz/VV/+/1Zc//8uNf//LjX//y41//8uNf//LjX//y00//9VW///V136/9vbr//b26D/29ug/9vboP/b26D/29ug/9vboP/b26D/29ug/9vboP+2tp3/aJG7/yqT/P8qk/z/KpP8/yqT/P9Wqfz/Wav8/ymS+/8wlvv/ZLD8/1ep/P9Vofz/VmH+/y00//8uNf//LjX//y41//8uNf//LTT//1xh+f/S07r/6OjD/+Tkuf/b25//29ug/9ran//k5Lj/6OjE/9vbov/b26D/29ug/7a2nf9okbv/KpP8/yqT/P8qk/z/KpP8/9Po/v/g7/7/KZL7/6HP/f/+/v7/eLr8/ymS/P9Fn/z/bZP9/2Rs/v9HTf//Rkz+/2ht/P+mqN3/3Nys/9ran//y8t7//Pz5/+fnwv/n58H/5+fC//z8+f/19eb/2tqg/9vboP/b26D/trad/2iRu/8qk/z/KpP8/yqT/P8qk/z/0+j+/+Dv/v9frvz//P3+/7TZ/f8qk/v/KpP8/yqT/P8pkvv/NZj7/2qz/P/m5r7/3Nyk/9ran//b26D/29ug/+HhsP/+/v3//f36//r68v/9/fr//v7+/+TkuP/b26D/29ug/9vboP+2tp3/aJG7/yqT/P8qk/z/KpP8/yqT/P/T6P7/8fj+/+Xy/v/z+f7/Opv7/yqT/P8qk/z/KpP8/yqT/P8qk/z/PZz8/9/fq//b26D/29ug/9vboP/b26D/2tqf//Ly3//4+O//29ug//n58P/29un/29ug/9vboP/b26D/29ug/7a2nf9okbv/KpP8/yqT/P8qk/z/KpP8/9Po/v/z+P7/p9L9//H4/v+12f3/KpP7/yqT/P8qk/z/KpP8/yqT/P89nPz/39+r/9vboP/b26D/29ug/9vboP/b26D/4eGw//7+/f/u7tP//v7+/+Xlu//b26D/29ug/9vboP/b26D/trad/2iRu/8qk/z/KpP8/yqT/P8qk/z/0+j+/+Dv/v8pkvv/m8z9//z9/v80mPv/KpP8/yqT/P8qk/z/KpP8/z2c/P/f36v/29ug/9vboP/b26D/29ug/9vboP/a2p//8vLf/////v/39+v/29ug/9vboP/b26D/29ug/9vboP+2tp3/aJG7/yqT/P8qk/z/KpP8/yqT/P/T6P7/8vj+/53N/f/r9f7/4O/+/yyU+/8qk/z/KpP8/yqT/P8qk/z/PZz8/9/fq//b26D/29ug/9vboP/b26D/29ug/9vboP/h4bH//v7+/+bmvf/b26D/29ug/9vboP/b26D/29ug/7a2nf9okbv/KpP8/yqT/P8qk/z/KpP8/63V/f/R6P7/zOX+/67W/f9Hovz/KpP8/yqT/P8qk/z/KpP8/yqT/P89nPz/39+r/9vboP/b26D/29ug/9vboP/b26D/29ug/9ran//r683/29ug/9vboP/b26D/29ug/9vboP/b26D/trad/2iRu/8qk/z/KpP8/yqT/P8qk/z/KpP8/yqT/P8qk/z/KpP8/yqT/P8qk/z/KpP8/yqT/P8qk/z/KpP8/z2c/P/f36v/29ug/9vboP/b26D/29ug/9vboP/b26D/29ug/9ran//b26D/29ug/9vboP/b26D/29ug/9vboP+2tp3/aJG7/yqT/P8qk/z/KpP8/yqT/P8qk/z/KpP8/yqT/P8qk/z/KpP8/yqT/P8qk/z/KpP8/yqT/P8qk/z/PZz8/9/fq//b26D/29ug/9vboP/b26D/29ug/9vboP/b26D/29ug/9vboP/b26D/29ug/9vboP/b26D/29ug/7a2nf9okbr/KpP8/yqT/P8qk/z/KpP8/yqT/P8qk/z/KpP8/yqT/P8qk/z/KpP8/yqT/P8qk/z/KpP8/yqT/P89nPz/39+r/9vboP/b26D/29ug/9vboP/b26D/29ug/9vboP/b26D/29ug/9vboP/b26D/29ug/9vboP/b26D/trad/4eOlf+Qpbn/kKW5/5Cluf+Qpbn/kKW5/5Cluf+Qpbn/kKW5/5Cluf+Qpbn/kKW5/5Cluf+Qpbn/kKW5/5aouf+0tKr/s7On/7Ozp/+zs6f/s7On/7Ozp/+zs6f/s7On/7Ozp/+zs6f/s7On/7Ozp/+zs6f/s7On/7Ozp/+Xl5L/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='

win = Tk()
win.title('随机抽号')
win.geometry('+500+300')
win.resizable(width=False, height=False)

tmp = open("tmp.ico","wb+")
tmp.write(base64.b64decode(img))
tmp.close()
win.iconbitmap("tmp.ico")
os.remove("tmp.ico")

l1 = Label(win,text='',bg='#00aaff',font=("幼圆",5),height=1).grid(row=0,column=0,sticky='W'+'N'+'E')

root = Frame(win,bg='#00aaff',borderwidth=2)

l3 = Label(root,text='',bg='#00aaff',font=("幼圆",5),width=1).grid(row=0,column=0,sticky='W'+'N'+'S')

root1 = Frame(root,bg='#00aaff',borderwidth=2)

frm1=Frame(root1,bg='#00aaff',borderwidth=2)

l7 = Label(frm1,text='起始号码:',bg='#00aaff',font=("幼圆",14,"bold"),height=1).grid(row=0,column=0,sticky='W'+'N'+'S')

var1 = StringVar()
ent1=Entry(frm1, textvariable = var1,width=8,font=("幼圆",13,"bold"),bg='#00ddff', fg="#222222")
ent1.grid(row=0,column=1,sticky='W'+'N'+'S'+'E')
ent1.bind('<Return>',tjpd)

frm1.grid(row=0,column=0)

l6 = Label(root1,text='',bg='#00aaff',font=("幼圆",5),height=1).grid(row=1,column=0,sticky='W'+'N'+'S')

frm2=Frame(root1,bg='#00aaff',borderwidth=2)

l8 = Label(frm2,text='终止号码:',bg='#00aaff',font=("幼圆",14,"bold"),height=1).grid(row=0,column=0,sticky='W'+'N'+'S')

var2 = StringVar()
ent2=Entry(frm2, textvariable = var2,width=8,font=("幼圆",13,"bold"),bg='#00ddff', fg="#222222")
ent2.grid(row=0,column=1,sticky='W'+'N'+'S'+'E')
ent2.bind('<Return>',tjpd)

frm2.grid(row=2,column=0)

l9 = Label(root1,text='',bg='#00aaff',font=("幼圆",5),height=1).grid(row=3,column=0,sticky='W'+'N'+'S')

frm3=Frame(root1,bg='#00aaff',borderwidth=2)

l10 = Label(frm3,text='产生数量:',bg='#00aaff',font=("幼圆",14,"bold"),height=1).grid(row=0,column=0,sticky='W'+'N'+'S')

var3 = StringVar()
ent3=Entry(frm3, textvariable = var3,width=8,font=("幼圆",13,"bold"),bg='#00ddff', fg="#222222")
ent3.grid(row=0,column=1,sticky='W'+'N'+'S'+'E')
ent3.bind('<Return>',tjpd)

frm3.grid(row=4,column=0)

l11 = Label(root1,text='',bg='#00aaff',font=("幼圆",5),height=1).grid(row=5,column=0,sticky='W'+'N'+'S')

frm4=Frame(root1,bg='#00aaff',borderwidth=2)

l12 = Label(frm4,text='最小间隔:',bg='#00aaff',font=("幼圆",14,"bold"),height=1).grid(row=0,column=0,sticky='W'+'N'+'S')

var4 = StringVar()
ent4=Entry(frm4, textvariable = var4,width=8,font=("幼圆",13,"bold"),bg='#00ddff', fg="#222222")
ent4.grid(row=0,column=1,sticky='W'+'N'+'S'+'E')
ent4.bind('<Return>',tjpd)

frm4.grid(row=6,column=0)

l13 = Label(root1,text='',bg='#00aaff',font=("幼圆",5),height=2).grid(row=7,column=0,sticky='W'+'N'+'S')

Button(root1, text="抽   号",height=1,font=("幼圆",14,"bold"),bg='RoyalBlue',command =tjpd).grid(row=8,column=0,sticky='W'+'N'+'E')

root1.grid(row=0,column=1)

l4 = Label(root,text='',bg='#00aaff',font=("幼圆",5),width=1).grid(row=0,column=2,sticky='W'+'N'+'S')

root2 = Frame(root,bg='#00aaff',borderwidth=2)

root3 = Frame(root2,bg='#00aaff',borderwidth=2)

l6 = Label(root3,text='抽号结果:',bg='#00aaff',font=("幼圆",14,"bold"),width=8,height=1).grid(row=0,column=0,sticky='W'+'N'+'E')
l7 = Label(root3,text='',bg='#00aaff',font=("幼圆",15),width=5).grid(row=0,column=1,sticky='W'+'N'+'E')

root3.grid(row=0,column=0)

t = Text(root2,width=6,height=10,font=("幼圆",12,"bold"),bg='#00ddff',fg='#222222')
t.grid(row=1,column=0,sticky='W'+'N'+'E'+'S')

root2.grid(row=0,column=3,sticky='W'+'N'+'S'+'E')

l5 = Label(root,text='',bg='#00aaff',font=("幼圆",5),width=1).grid(row=0,column=4,sticky='W'+'N'+'S')

root.grid(row=1,column=0)

l2 = Label(win,text='',bg='#00aaff',font=("幼圆",5),height=1).grid(row=2,column=0,sticky='W'+'N'+'E')

var1.set('1')
var2.set('45')
var3.set('5')
var4.set('1')

win.mainloop()