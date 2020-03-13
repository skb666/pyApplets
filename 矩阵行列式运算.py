import numpy as np 
ty=input('type(matrix/determinant):')
oper=input('operation:')
bj=0
op={}
cz={}
if ty=='matrix' or ty=='determinant':
    id_i=0
    for i in oper:
        sj=[]
        if i!='+' and i!='-' and i!='*' and i!='/':
            if not i in op.keys():
                a=input('matrix:').strip().split(';') if ty=='matrix' else input('determinant:').strip().split(';')
                for j in a:
                    tem=[]
                    for k in j.split(','):
                        tem.append(eval(k))
                    sj.append(tem)
                try:
                    op[i]=np.array(sj) if ty=='matrix' else np.linalg.det(np.array(sj))
                except:
                    bj=3
        elif i=='+' or i=='-' or i=='*' or i=='/':
            cz[id_i]=i
        else:
            bj=2
            break
        id_i+=1
else:
    bj=1
if bj==1:
    print("Type Error!")
elif bj==2:
    print("Operation Error!")
elif bj==3:
    print("Value Error!")
print(op)
print(cz)
# else:
#     if ty=='matrix':
#         i=0
#         op_1=[]
#         cz_1={}
#         for ind,opt in cz:
#             if opt=='*':
#                 op_1.append(np.dot(op[oper[ind-1]],op[oper[ind+1]]))
#             if opt=='/':
#                 
