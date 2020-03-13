import numpy as np
import cv2,sys
import function.Image_Process as IP
import function.Digital_Identification as DI
import function.Data_Calculation as DC
from matplotlib import pyplot as plt

#图像文件位置
RES=sys.argv[1]

#是否查看中间过程
DEBUG=0
#标准方格大小
GRID_WIDTH=40
GRID_HEIGHT=40
#标准数字大小
NUM_WIDTH=20
NUM_HEIGHT=20
#数读尺寸
SUDOKU_SIZE=9

#存储题目的数组
sudoku=np.zeros(shape=(9*9,NUM_WIDTH*NUM_HEIGHT))

#读取图片
img_original=cv2.imread(RES)
if DEBUG:
    IP.plotImg(img_original,"original")

#预处理及图像校正
img_puzzle=IP.correct(img_original)
if DEBUG:
    IP.plotImg(img_puzzle,"pre-process")

#识别并记录序号
indexes_numbers = []
for i in range(SUDOKU_SIZE):
    for j in range(SUDOKU_SIZE):
        img_number=img_puzzle[i*GRID_HEIGHT:(i+1)*GRID_HEIGHT][:,j*GRID_WIDTH:(j+1)*GRID_WIDTH]
        hasNumber,sudoku[i*9+j,:]=IP.extract_number(img_number)
        if hasNumber:
            indexes_numbers.append(i*9+j)

# 显示提取数字结果
if DEBUG:
    print("There are",len(indexes_numbers),"numbers and the indexes of them are:")
    print(indexes_numbers)
    # 创建子图
    rows=len(indexes_numbers)//5+1
    f,axarr=plt.subplots(rows,5)
    row=0
    for x in range(len(indexes_numbers)):
        ind=indexes_numbers[x]
        if x%5==0 and x!=0:
            row+=1
        axarr[row,x%5].imshow(cv2.resize(sudoku[ind,:].reshape(NUM_WIDTH,NUM_HEIGHT),
                (NUM_WIDTH*5,NUM_HEIGHT*5)),cmap=plt.gray())
    for i in range(rows):
        for j in range(5):
            axarr[i,j].axis("off")
    plt.show()

#构建测试数据集
test=np.zeros(shape=(len(indexes_numbers),NUM_WIDTH*NUM_HEIGHT))
for num in range(len(indexes_numbers)):
    test[num]=sudoku[indexes_numbers[num]]
test=test.reshape(-1, NUM_WIDTH*NUM_HEIGHT).astype(np.float32)
result=DI.knn_ocr_normal(test)

#使用识别结果构建数独问题的二维数组,其他数字用0表示
sudoku_puzzle=np.zeros(SUDOKU_SIZE*SUDOKU_SIZE)
for num in range(len(indexes_numbers)):
    sudoku_puzzle[indexes_numbers[num]]=result[num]
sudoku_puzzle=sudoku_puzzle.reshape((SUDOKU_SIZE,SUDOKU_SIZE)).astype(np.int32)
print(sudoku_puzzle)

#保存提取出的图片(可选)
for num in range(len(indexes_numbers)):
    number_path1="number\\%s"%(str(num))+'.png'
    img_num=sudoku[indexes_numbers[num]].reshape(20,20)
    cv2.imwrite(number_path1,img_num)

# 显示识别出的数字 show the numbers
img_puzzle_white = img_puzzle.copy()
img_puzzle_white = cv2.bitwise_not(img_puzzle_white)
img_puzzle_recognize = cv2.cvtColor(img_puzzle_white, cv2.COLOR_GRAY2BGR)
for i in range(9):
    for j in range(9):
        x=int(i*GRID_WIDTH+10)
        y=int(j*GRID_WIDTH+GRID_WIDTH-8)
        if sudoku_puzzle[j][i]>0:
            cv2.putText(img_puzzle_recognize,str(sudoku_puzzle[j][i]),(x,y),cv2.FONT_HERSHEY_SIMPLEX,
                    1,(0,0,255),2)
#IP.plotImgs(img_puzzle_white,img_puzzle_recognize)

#解数独
sudoku_solved=DC.Sudoku(sudoku_puzzle)._solve_sudoku
sudoku_solved=np.array(sudoku_solved)
print(sudoku_solved)

# 显示结果 show the answer
img_puzzle_solved = img_puzzle_recognize.copy()
for i in range(9):
    for j in range(9):
        x = int(i*GRID_WIDTH+10)
        y = int(j*GRID_WIDTH+GRID_WIDTH-8)
        if sudoku_puzzle[j][i]==0:
            cv2.putText(img_puzzle_solved,str(sudoku_solved[j][i]),(x,y),cv2.FONT_HERSHEY_SIMPLEX,
                    1,(255, 0, 0),2)
#IP.plotImg(img_puzzle_solved)
cv2.imwrite(RES[:-4]+'_solve.png',img_puzzle_solved)