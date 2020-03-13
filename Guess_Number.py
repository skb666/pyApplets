__author__='skb666'
def guess_number():
	pd=True
	while pd==True: 
		import random,os
		os.system('cls')
		hh=""		
		ws=random.randint(1,5)    #位数等概率
		zd1={1:[1,9],2:[10,99],3:[100,999],4:[1000,9999],5:[10000,99999]}
		ys=random.randint(zd1[ws][0],zd1[ws][1])    #生成随机数ys
		mi=zd1[ws][0]-1
		ma=zd1[ws][1]+1
		print("猜数字游戏开始,已为你生成"+str(len(str(ys)))+"位的随机数!")
		sr=input("你猜该数为("+str(mi)+","+str(ma)+"):")   #输入猜测数
		if sr=="":
			cs=ys
			hh="Y"
		else:
			cs=int(sr)
		js=1   #记录猜测次数
		while cs!=ys:   #判断是否猜对
			if cs>ys:
				if cs<ma:
					ma=cs
				sr=input("太大了，再猜猜("+str(mi)+","+str(ma)+"):")
				if sr=="":
					cs=ys
					hh="Y"
				else:
					cs=int(sr)
				js+=1   #猜测次数加1
			elif cs<ys:
				if cs>mi:
					mi=cs
				sr=input("太小了，再猜猜("+str(mi)+","+str(ma)+"):")
				if sr=="":
					cs=ys
					hh="Y"
				else:
					cs=int(sr)
				js+=1
		if cs==ys and hh=="":
			print("恭喜你，猜对了！你总共猜了"+str(js)+"次!")
			hh=input("要再玩一次吗？(Y/N)")   
			if hh.strip().upper()=="N":
				pd=False   #是否结束循环
if __name__=='__main__':
	guess_number()
