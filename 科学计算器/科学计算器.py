from tkinter import *
from math import *
root = Tk()
root.title("计算器")
root.geometry("850x260+200+200")

 
def come(event):
  event.widget["background"]= "orange"#event的widget方法,恩,恩,值得看看
def go(event):
  event.widget["background"] = "#%02x%02x%02x" % (240,240,240)#实现RGB和十六进制的换算
def num1():
  text.insert(END,1)
def num2():
  text.insert(END,2)
def num3():
  text.insert(END,3)
def num4():
  text.insert(END,4)
def num5():
  text.insert(END,5)
def num6():
  text.insert(END,6)
def num7():
  text.insert(END,7)
def num8():
  text.insert(END,8)
def num9():
  text.insert(END,9)
def num0():
  if text.get(END) =="/":
    messagebox.showinfo(title ="除数不能为零")
  else:
    text.insert(END,0)
def dot_it():
  text.insert(END,".")
   
def Addnum():
  if text.get(1.0,END):
    text.insert(END,"+")
def minus_num():
  if text.get(1.0,END):
    text.insert(END,"-")
def times_num():
  if text.get(1.0,END):
    text.insert(END,"*")
def div_num():
  if text.get(1.0,END):
    text.insert(END,"/")
   
def equal_it():#可以使用text的search方法排除除法和开根号的例外
  global list_power,x,list_log,xylog
  se = text.get(1.0,END)
  if se:
    if "/" in text.get(1.0,END):
      div_pos = text.search("/",1.0,END)
      pos = div_pos.split(".")
      text_row = pos[0]
      text_column = pos[1]
      newpos = "%d.%d" % (int(text_row),int(text_column)+1)
      cool = eval(text.get(newpos,END))
      if cool == 0:
        text_alert.insert(1.0,"被除数不能为零")
        return
      else:
        se = eval(se)
        text.delete(1.0,END)
        text.insert(1.0,se)
    elif xypower==True:#通过设全局变量为哨兵,看函数是否被调用
      list_power.append(eval(se))
      text.delete(1.0,END)
      text.insert(1.0,pow(list_power[0],list_power[1]))
      list_power = []
    elif xylog ==True:
      list_log.append(eval(se))
      text.delete(1.0,END)
      text.insert(1.0,log(list_log[1],list_log[0]))
      list_log = []
       
       
    else:
      se = eval(se)
      text.delete(1.0,END)
      text.insert(1.0,se)
  else:
    text.delete(1.0,END)
def negative():
  text.insert(END,"-")
def Square_root():
  if eval(text.get(1.0,END))>=0:
    rootit =sqrt(eval(text.get(1.0,END)))
    text.delete(1.0,END)
    text.insert(1.0,rootit)
def Per():
  if text.get(1.0,END):
    num = eval(text.get(1.0,END))
    text.insert(END,"%")
    newnum = num*0.01
    text.delete(1.0,END)
    text.insert(1.0,newnum)
 
def Reci_num():
  #text.get(1.0,"%s-2c" % END).strip("\n")
  #if text.get(1.0,"%s-1c" % END).isdigit():
    # if type(aa)==type(bb) 可以用来判断数据类型
    # if type(aa)==type(1)
    #if type(aa)==type("我")
    #if type(aa)==type(3.14)
  if eval(text.get(1.0,END))!=0:
    num = eval(text.get(1.0,END).strip("\n"))
    num = 1/num
    text.delete(1.0,END)
    text.insert(1.0,num)
  else:
      text_alert.insert(1.0,"零不能求倒数")
   
def C():
  global memorylist,list_power,list_log# global的用法
  text.delete(1.0,END)
  text_alert.delete(1.0,END)
  memorylist = []
  list_power = []
  list_log =[]
   
def CE():
  text.delete(1.0,END)
  text_alert.delete(1.0,END)
def delete_onechar():
  text.delete("%s-1c" % INSERT,INSERT)#字符index的移动
def Mc():
  global memorylist
  memorylist = []
def Ms():
  global memorylist
  memorylist.append(eval(text.get(1.0,END)))
  text.delete(1.0,END)
def M_plus():
  global memorylist
  global m_plus
  m_plus = True
  memorylist.append(eval(text.get(1.0,END)))
  text.delete(1.0,END)
  return True
def M_minus():
  global memorylist
  global m_minus
  m_minus =True
  memorylist.append(eval(text.get(1.0,END)))
  text.delete(1.0,END)
  return True
def Mr():
  global memorylist
  global m_plus
  global m_minus
  text.delete(1.0,END)
  if m_plus == True:
    sum1 =0
    for i in range(len(memorylist)):
      sum1 = sum1 + memorylist[i]
    memorylist =[]
    memorylist.append(sum1)
    text.insert(1.0,sum1)
  elif m_minus == True:
    difference = 0
    for i in range(len(memorylist)):
      difference = memorylist[i]-difference
    difference = - difference
    memorylist.append(difference)
    text.insert(1.0,difference)
def angle_radio():
  text.delete(1.0,END)
  global angle_is
  angle_is =True
     
def radium_radio():
  text.delete(1.0,END)
  global radium_is
  radium_is =True
def angle_choice():
  global x
  if angle_is == True:
    x = pi*eval(text.get(1.0,END))/180
  if radium_is == True:
    x = eval(text.get(1.0,END))
def circle_ratio():
  text.insert(END,pi)
def sin_x():
  global x
  angle_choice()
  text.delete(1.0,END)
  text.insert(1.0,sin(x))
   
def cos_x():
  global x
  angle_choice()
  text.delete(1.0,END)
  text.insert(1.0,cos(x))
   
def tan_x():
  angle_choice()
  if x == 90 or x == pi/2:
    text_alert.insert(1.0,"正切角度不能为90度或π/2弧度")
    return
  else:
    text.delete(1.0,END)
    text.insert(1.0,tan(x))
   
def square_it():
  temp = eval(text.get(1.0,END))
  text.delete(1.0,END)
  text.insert(1.0,pow(temp,2))
def x_ypower():
  global list_power,x,xypower
  xypower =True
  x = eval(text.get(1.0,END))
  list_power.append(x)
  text.delete(1.0,END)
def tri_power():
  temp = eval(text.get(1.0,END))
  text.delete(1.0,END)
  text.insert(1.0,pow(temp,3))
def Bracket_left():
  text.insert(END,"(")
def Bracket_right():
  text.insert(END,")")
def nature_log():
  temp = eval(text.get(1.0,END))
  text.delete(1.0,END)
  text.insert(1.0,log1p(temp))
def deci_log():
  temp = eval(text.get(1.0,END))
  text.delete(1.0,END)
  text.insert(1.0,log10(temp))
def bina_log():
  temp = eval(text.get(1.0,END))
  text.delete(1.0,END)
  text.insert(1.0,log2(temp))
def y_based_on_x_log():
  global list_log,x,xylog
  xylog =True
  x = eval(text.get(1.0,END))
  list_log.append(x)
  text.delete(1.0,END)
def natur_const():
  text.insert(END,e)
def anti_sin():
  temp = eval(text.get(1.0,END))
  text.delete(1.0,END)
  text.insert(1.0,asin(temp)*180/pi)
def anti_cos():
  temp = eval(text.get(1.0,END))
  text.delete(1.0,END)
  text.insert(1.0,acos(temp)*180/pi)
def anti_tan():
  temp = eval(text.get(1.0,END))
  text.delete(1.0,END)
  text.insert(1.0,atan(temp)*180/pi)
def sqrt_num():
  temp = eval(text.get(1.0,END))
  text.delete(1.0,END)
  text.insert(1.0,sqrt(temp))
def tri_root():
  temp = eval(text.get(1.0,END))
  text.delete(1.0,END)
  text.insert(1.0,pow(temp,1/3))
   
def standard():
  MC = Button(root,text ="MC",width =10,command = Mc)
  MC.bind("<Enter>",come)
  MC.bind("<Leave>",go)
  MC.grid(row=2,column =0,sticky =W,padx =1)
  MR = Button(root,text ="MR",width =10,command = Mr)
  MR.grid(row=2,column =1,stick = W,padx =1)
  MR.bind("<Enter>",come)
  MR.bind("<Leave>",go)
  MS = Button(root,text ="MS",width =10,command =Ms)
  MS.grid(row=2,column =2,sticky =W,padx =1)
  MS.bind("<Enter>",come)
  MS.bind("<Leave>",go)
  M_ADD = Button(root,text ="M+",width =10,command =M_plus)
  M_ADD.grid(row=2,column =3,sticky =W,padx =1)
  M_ADD.bind("<Enter>",come)
  M_ADD.bind("<Leave>",go)
  M_ADD.bind("<>")
  M_Minus = Button(root,text ="M-",width =10,command =M_minus)
  M_Minus.grid(row=2,column =4,sticky =W,padx =1)
  M_Minus.bind("<Enter>",come)
  M_Minus.bind("<Leave>",go)
 
  DEL = Button(root,text ="→",width =10,command =delete_onechar)
  DEL.grid(row=3,column =0,sticky =W,padx =1)
  DEL.bind("<Enter>",come)
  DEL.bind("<Leave>",go)
  CEbtn = Button(root,text ="CE",width =10,command =CE)
  CEbtn.grid(row=3,column =1,sticky =W,padx =1)
  CEbtn.bind("<Enter>",come)
  CEbtn.bind("<Leave>",go)
  Cbtn = Button(root,text ="C",width =10,command =C)
  Cbtn.grid(row=3,column =2,sticky =W,padx =1)
  Cbtn.bind("<Enter>",come)
  Cbtn.bind("<Leave>",go)
  negativ = Button(root,text ="负号 - ",width =10,command = negative)
  negativ.grid(row=3,column =3,sticky =W,padx =1)
  negativ.bind("<Enter>",come)
  negativ.bind("<Leave>",go)
  sqr_root = Button(root,text ="平方根√",width =10,command =Square_root )
  sqr_root.grid(row =3,column =4,sticky =W,padx =1)
  sqr_root.bind("<Enter>",come)
  sqr_root.bind("<Leave>",go)
 
 
  btn7 = Button(root,text =7,width =10,command = num7)
  btn7.grid(row=4,column =0,sticky =W,padx =1)
  btn7.bind("<Enter>",come)
  btn7.bind("<Leave>",go)
  btn8 = Button(root,text =8,width =10,command = num8)
  btn8.grid(row=4,column =1,sticky =W,padx =1)
  btn8.bind("<Enter>",come)
  btn8.bind("<Leave>",go)
  btn9 = Button(root,text =9,width =10,command = num9)
  btn9.grid(row=4,column =2,sticky =W,padx =1)
  btn9.bind("<Enter>",come)
  btn9.bind("<Leave>",go)
  div = Button(root,text ="除法 /",width =10,command = div_num)
  div.grid(row=4,column =3,sticky =W,padx =1)
  div.bind("<Enter>",come)
  div.bind("<Leave>",go)
  per = Button(root,text ="百分之 %",width =10,command =Per)
  per.grid(row=4,column =4,sticky =W,padx =1)
  per.bind("<Enter>",come)
  per.bind("<Leave>",go)
 
  btn4 = Button(root,text =4,width =10,command = num4)
  btn4.grid(row=5,column =0,sticky =W,padx =1)
  btn4.bind("<Enter>",come)
  btn4.bind("<Leave>",go)
  btn5 = Button(root,text =5,width =10,command = num5)
  btn5.grid(row=5,column =1,sticky =W,padx =1)
  btn5.bind("<Enter>",come)
  btn5.bind("<Leave>",go)
  btn6 = Button(root,text =6,width =10,command = num6)
  btn6.grid(row=5,column =2,sticky =W,padx =1)
  btn6.bind("<Enter>",come)
  btn6.bind("<Leave>",go)
  times = Button(root,text ="乘法 ×",width =10,command = times_num)
  times.grid(row=5,column =3,sticky =W,padx =1)
  times.bind("<Enter>",come)
  times.bind("<Leave>",go)
  reciprocal = Button(root,text ="倒数 1/x",width =10,command =Reci_num)
  reciprocal.grid(row=5,column =4,sticky =W,padx =1)
  reciprocal.bind("<Enter>",come)
  reciprocal.bind("<Leave>",go)
 
 
  btn1 = Button(root,text =1,width =10,command = num1)
  btn1.grid(row=6,column =0,sticky =W,padx =1)
  btn1.bind("<Enter>",come)
  btn1.bind("<Leave>",go)
  btn2 = Button(root,text =2,width =10,command = num2)
  btn2.grid(row=6,column =1,sticky =W,padx =1)
  btn2.bind("<Enter>",come)
  btn2.bind("<Leave>",go)
  btn3 = Button(root,text =3,width =10,command = num3)
  btn3.grid(row=6,column =2,sticky =W,padx =1)
  btn3.bind("<Enter>",come)
  btn3.bind("<Leave>",go)
  minus = Button(root,text ="减 - ",width =10,command =minus_num )
  minus.grid(row=6,column =3,sticky =W,padx =1)
  minus.bind("<Enter>",come)
  minus.bind("<Leave>",go)
  equal = Button(root,text ="=",width =10,height =3,command = equal_it)
  equal.grid(row=6,column =4,sticky =W,padx =1,rowspan =2)
  equal.bind("<Enter>",come)
  equal.bind("<Leave>",go)
 
  btn0 = Button(root,text =0,width =22,height =1,command = num0)
  btn0.grid(row=7,column =0,sticky =W,padx =1,columnspan =2)
  btn0.bind("<Enter>",come)
  btn0.bind("<Leave>",go)
  dot = Button(root,text =".",width =7,font =("Times","14"),height =1,command =dot_it)
  dot.grid(row=7,column =2,sticky =W,padx =1)
  dot.bind("<Enter>",come)
  dot.bind("<Leave>",go)
  add = Button(root,text ="加 +",width =10,command = Addnum)
  add.grid(row=7,column =3,sticky =W,padx =1)
  add.bind("<Enter>",come)
  add.bind("<Leave>",go)
 
def sci():
  v =IntVar()
  angle = Radiobutton(root,text = "角度",variable =v,value =1,command =angle_radio)
  angle.grid(row=0,column=6)
  radium = Radiobutton(root,text = "弧度",variable =v,value =2,command =radium_radio )
  radium.grid(row=0,column=7)
 
  sinaa = Button(root,text = "Sin(x)",width =18,command = sin_x)
  sinaa.grid(row = 1,column =6)
  sinaa.bind("<Enter>",come)
  sinaa.bind("<Leave>",go)
  cosaa = Button(root,text = "COS(x)",width =18,command = cos_x)
  cosaa.grid(row =1,column =7)
  cosaa.bind("<Enter>",come)
  cosaa.bind("<Leave>",go)
  tanaa = Button(root,text = "tan(x)",width =18,command =tan_x)
  tanaa.grid(row = 1,column =8)
  tanaa.bind("<Enter>",come)
  tanaa.bind("<Leave>",go)
  x_square = Button(root,text = "x的平方",width =18,command = square_it)
  x_square.grid(row =2,column =6)
  x_square.bind("<Enter>",come)
  x_square.bind("<Leave>",go)
  X_Ytimes = Button(root,text = "x的Y次方",width =18,command =x_ypower)
  X_Ytimes.grid(row = 2,column =7)
  X_Ytimes.bind("<Enter>",come)
  X_Ytimes.bind("<Leave>",go)
  X_tri= Button(root,text = "x的三次方",width =18,command = tri_power)
  X_tri.grid(row = 2,column =8)
  X_tri.bind("<Enter>",come)
  X_tri.bind("<Leave>",go)
 
  leftbra = Button(root,text = "左括号 ( ",width =18,command = Bracket_left)
  leftbra.grid(row = 3,column =6)
  leftbra.bind("<Enter>",come)
  leftbra.bind("<Leave>",go)
  rightbra = Button(root,text = "右括号  )",width =18,command = Bracket_right)
  rightbra.grid(row =3,column =7)
  rightbra.bind("<Enter>",come)
  rightbra.bind("<Leave>",go)
  natural_logs = Button(root,text = "自然对数 In(x)",width =18,command =nature_log)
  natural_logs.grid(row = 7,column =6)
  natural_logs.bind("<Enter>",come)
  natural_logs.bind("<Leave>",go)
  square_root = Button(root,text = "x的平方根",width =18,command = sqrt_num)
  square_root.grid(row =4,column =6)
  square_root.bind("<Enter>",come)
  square_root.bind("<Leave>",go)
  X_Yroot = Button(root,text = "x的Y次方根",width =18,command = x_ypower)
  X_Yroot.grid(row = 4,column =7)
  X_Yroot.bind("<Enter>",come)
  X_Yroot.bind("<Leave>",go)
  X_tri_root = Button(root,text = "x的三次方根",width =18,command = tri_root)
  X_tri_root.grid(row = 4,column =8)
  X_tri_root.bind("<Enter>",come)
  X_tri_root.bind("<Leave>",go)
 
  log10aa = Button(root,text = "以10为底的对数Logx",width =18,command =deci_log)
  log10aa.grid(row = 5,column =6)
  log10aa.bind("<Enter>",come)
  log10aa.bind("<Leave>",go)
  log2aa = Button(root,text = "以2为底的对数Logx",width =18,command =bina_log)
  log2aa.grid(row = 5,column =8)
  log2aa.bind("<Enter>",come)
  log2aa.bind("<Leave>",go)
  pow10 = Button(root,text = "以x为底,y为真数的logx",width =18,command =y_based_on_x_log)
  pow10.grid(row =5,column =7)
  pow10.bind("<Enter>",come)
  pow10.bind("<Leave>",go)
  radio = Button(root,text = "圆周率 π",width =18,command =circle_ratio)
  radio.grid(row = 7,column =7)
  radio.bind("<Enter>",come)
  radio.bind("<Leave>",go)
  natur_con = Button(root,text = "自然常数e",width =18,command =natur_const)
  natur_con.grid(row = 7,column =8)
  natur_con.bind("<Enter>",come)
  natur_con.bind("<Leave>",go)
 
  antisin = Button(root,text = "反三角正弦sin(-1)x",width =18,height =1,command =anti_sin)
  antisin.grid(row = 6,column =6)
  antisin.bind("<Enter>",come)
  antisin.bind("<Leave>",go)
  anticos = Button(root,text = "反三角余弦cos(-1)x",width =18,height =1,command =anti_cos)
  anticos.grid(row =6,column =7)
  anticos.bind("<Enter>",come)
  anticos.bind("<Leave>",go)
  antitan = Button(root,text = "反三角正切tan(-1)x",width =18,height =1,command = anti_tan)
  antitan.grid(row = 6,column =8)
  antitan.bind("<Enter>",come)
  antitan.bind("<Leave>",go)
 
###################
if __name__ == "__main__":
  ################################菜单设计
  standard_it =True
  sci_it = False
  static_it = False
  code_it = False
  memorylist = []
  m_plus = False
  m_minus = False
  angle_is = False
  radium_is = False
  x =0
  list_power = []
  list_log =[]
  xypower = False
  xylog = False
  text = Text(root,height =1,font = ("Times","20"),width =31,fg = "#%02x%02x%02x" % (46,150,67),bd =0)
  text.grid(row = 0,column =0,columnspan =6)
  text_alert = Text(root,height=1,width =31,fg = "red",font = ("Times","20"),bd = 0)
  text_alert.grid(row =1,column =0,columnspan =6)
 
  menubar = Menu(root)
  mode_menu = Menu(menubar,tearoff= 0)
  v_mode = IntVar()
  mode_menu.add_radiobutton(label = "标准型",variable = v_mode,value =0,command =standard)
  mode_menu.add_radiobutton(label = "科学型",variable = v_mode,value =1,command = sci)
  mode_menu.add_radiobutton(label = "程序员型",variable =v_mode,value =2)
  mode_menu.add_radiobutton(label = "统计型",variable = v_mode,value =3)
 
  mode_menu.insert_separator(7)
  v_his_math = IntVar()
  mode_menu.add_radiobutton(label = "历史记录",variable = v_his_math,value =0)
  mode_menu.add_radiobutton(label = "数字分组",variable = v_his_math,value =1)
  menubar.add_cascade(label = "查看",menu = mode_menu)
 
  mode_menu.insert_separator(11)
  v_transform = IntVar()
  mode_menu.add_radiobutton(label = "单位转换",variable =v_transform,value =1)
 
  edit = Menu(menubar)
  edit.add_command(label = "复制")
  edit.add_command(label = "黏贴")
  menubar.add_cascade(label = "编辑",menu = edit)
 
  helpm = Menu(menubar)
  helpm.add_command(label = "使用说明")
  helpm.add_command(label = "版本为1.0")
  menubar.add_cascade(label = "帮助",menu = helpm)
  root.config(menu = menubar)#有这句菜单栏才能正常工作
#########################################窗体设计
   
  standard()
   
  sci()
  root.mainloop()