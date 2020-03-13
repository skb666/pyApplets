import cv2
import numpy as np
from matplotlib import pyplot as plt

#是否查看中间过程
DEBUG=0
# 标准方格大小
GRID_WIDTH = 40
GRID_HEIGHT = 40
# 标准数字大小
NUM_WIDTH = 20
NUM_HEIGHT = 20
# 判定非零像素书最小阈值
N_MIN_ACTIVE_PIXELS = 30

IMAGE_LENGTH=40
SUDOKU_SIZE=9
SIZE_PUZZLE=IMAGE_LENGTH*SUDOKU_SIZE

#转换图像格式,并使用matplotlib显示opencv图像(单)
def plotImg(img,title=""):
    if img.ndim==3:
        b,g,r=cv2.split(img)
        img=cv2.merge([r,g,b])
        plt.imshow(img),plt.axis("off")
        plt.title(title)
        plt.show()

#转换图像格式,并使用matplotlib显示opencv图像(双)
def plotImgs(img1, img2):
    if img1.ndim == 3:
        b, g, r = cv2.split(img1)
        img1 = cv2.merge([r, g, b])
        plt.subplot(121), plt.imshow(img1), plt.axis("off")
    else:
        plt.subplot(121), plt.imshow(img1, cmap='gray'), plt.axis("off")
    if img2.ndim == 3:
        b, g, r = cv2.split(img2)
        img2 = cv2.merge([r, g, b])
        plt.subplot(122), plt.imshow(img2), plt.axis("off")
    else:
        plt.subplot(122), plt.imshow(img2, cmap='gray'), plt.axis("off")
    plt.show()

#处理图像
def correct(img_original):
    #灰度化
    img_gray=cv2.cvtColor(img_original,cv2.COLOR_BGR2GRAY)
    if DEBUG:
        plotImg(img_gray,"gray")

    #中值滤波
    img_blur=cv2.medianBlur(img_gray,1)
    if DEBUG:
        plotImg(img_blur,"median Blur")

    #高斯滤波
    img_blur=cv2.GaussianBlur(img_blur,(3,3),0)
    if DEBUG:
        plotImg(img_blur, "Gaussian Blur")

    #将每个像素除以闭操作后的像素,可以调整图像亮度
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11, 11))
    close=cv2.morphologyEx(img_blur,cv2.MORPH_CLOSE,kernel)
    div=np.float32(img_blur)/close
    img_brightness_adjusted=np.uint8(cv2.normalize(div, div, 0, 255, cv2.NORM_MINMAX))
    if DEBUG:
        plotImg(img_brightness_adjusted,"brightness adjust")

    #自适应阈值二值化,注意其返回值只有一个
    img_thresh=cv2.adaptiveThreshold(img_brightness_adjusted,255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,11,7)
    if DEBUG:
        img_thresh=cv2.medianBlur(img_thresh,3)
        plotImg(img_thresh,"adaptive Threshold")

    #寻找轮廓
    b,contours,hierarchy=cv2.findContours(img_thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if DEBUG:
        img_contours=img_original.copy()
        cv2.drawContours(img_contours, contours,-1,(0,0,255),2)
        plotImg(img_contours, "contours")

    #找到最大轮廓
    max_area=0
    biggest_contour=None
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>max_area:
            max_area=area
            biggest_contour=cnt

    #图像加标记
    mask=np.zeros(img_brightness_adjusted.shape,np.uint8)
    cv2.drawContours(mask,[biggest_contour],0,255,cv2.FILLED)
    cv2.drawContours(mask,[biggest_contour],0,0,2)
    image_with_mask=cv2.bitwise_and(img_brightness_adjusted,mask)
    if DEBUG:
        plotImg(image_with_mask,"image_with_mask")

    #角点检测
    dst=cv2.cornerHarris(image_with_mask, 2, 3, 0.04)
    if DEBUG:
        plotImg(dst,"image_cornerHarris")

    #水平方向Sobel算子，膨胀操作连接断线，边缘检测找出竖线
    dx=cv2.Sobel(image_with_mask,cv2.CV_16S,1,0)
    dx=cv2.convertScaleAbs(dx)
    cv2.normalize(dx,dx,0,255,cv2.NORM_MINMAX)
    ret, close=cv2.threshold(dx,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    kernelx=cv2.getStructuringElement(cv2.MORPH_RECT,(2,10))
    close=cv2.morphologyEx(close,cv2.MORPH_DILATE,kernelx,iterations=1)

    b,contour,hierarchy=cv2.findContours(close,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contour:
        x,y,w,h=cv2.boundingRect(cnt)
        if h/w>5:
            cv2.drawContours(close,[cnt],0,255,-1)
        else:
            cv2.drawContours(close,[cnt],0,0,-1)

    close=cv2.morphologyEx(close,cv2.MORPH_CLOSE,None,iterations=2)
    closex=close.copy()

    #找出横线
    dy=cv2.Sobel(image_with_mask,cv2.CV_16S,0,2)
    dy=cv2.convertScaleAbs(dy)
    cv2.normalize(dy,dy,0,255,cv2.NORM_MINMAX)
    retVal,close=cv2.threshold(dy,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    kernely=cv2.getStructuringElement(cv2.MORPH_RECT,(10,2))
    close=cv2.morphologyEx(close,cv2.MORPH_DILATE,kernely)

    b,contour,hierarchy=cv2.findContours(close,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contour:
        x,y,w,h=cv2.boundingRect(cnt)
        if w/h>5:
            cv2.drawContours(close,[cnt],0,255,-1)
        else:
            cv2.drawContours(close,[cnt],0,0,-1)

    close=cv2.morphologyEx(close,cv2.MORPH_DILATE,None,iterations=2)
    closey=close.copy()

    #求网格交点
    res=cv2.bitwise_and(closex,closey)

    #查找轮廓,求每个轮廓的质心
    img_dots=cv2.cvtColor(img_brightness_adjusted,cv2.COLOR_GRAY2BGR)
    b,contour,hierarchy=cv2.findContours(res,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    centroids=[]
    for cnt in contour:
        if cv2.contourArea(cnt)>20:
            mom=cv2.moments(cnt)
            (x,y)=int(mom['m10']/mom['m00']),int(mom['m01']/mom['m00'])
            cv2.circle(img_dots,(x,y),4,(0,255,0),-1)
            centroids.append((x,y))
    if DEBUG:
        plotImg(img_dots, "centroids")

    centroids=np.array(centroids,dtype=np.float32)
    c=centroids.reshape((100,2))
    c2=c[np.argsort(c[:,1])]
    b=np.vstack([c2[i*10:(i+1)*10][np.argsort(c2[i*10:(i+1)*10,0])] for i in range(10)])
    bm=b.reshape((10,10,2))

    #使用透视变换,根据以上角点将每个方格矫正,最后拼接成校正后图像
    res2=cv2.cvtColor(img_brightness_adjusted,cv2.COLOR_GRAY2BGR)
    output=np.zeros((450,450,3), np.uint8)
    for i,j in enumerate(b):
        ri=i//10
        ci=i%10
        if ci!=9 and ri!=9:
            src=bm[ri:ri+2,ci:ci+2,:].reshape((4,2))
            dst=np.array([[ci*50,ri*50],[(ci+1)*50-1,ri*50],[ci*50,(ri+1)*50-1],
                    [(ci+1)*50-1,(ri+1)*50-1]],np.float32)
            retval=cv2.getPerspectiveTransform(src,dst)
            warp=cv2.warpPerspective(res2,retval,(450,450))
            output[ri*50:(ri+1)*50-1,ci*50:(ci+1)*50-1]=warp[ri*50:(ri+1)*50-1,
                    ci*50:(ci+1)*50-1].copy()
    img_correct=cv2.cvtColor(output,cv2.COLOR_BGR2GRAY)
    img_puzzle=cv2.adaptiveThreshold(img_correct,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV, 5, 7)
    img_puzzle=cv2.resize(img_puzzle,(SIZE_PUZZLE,SIZE_PUZZLE),interpolation=cv2.INTER_LINEAR)
    return img_puzzle

def preprocess_grid(im_number):
    """
    二值化；去除离中心较远的像素（排除边框干扰）；统计非零像素数（判断方格中是否有数字）
    :param im_number: 方格图像
    :return: im_number_thresh: 二值化及处理后图像
             n_active_pixels: 非零像素数
    """

    # 二值化
    retVal,im_number_thresh=cv2.threshold(im_number,150,255,cv2.THRESH_BINARY)

    # 去除离中心较远的像素点（排除边框干扰）
    for i in range(im_number.shape[0]):
        for j in range(im_number.shape[1]):
            dist_center=np.sqrt(np.square(GRID_WIDTH//2-i)+np.square(GRID_HEIGHT//2-j))
            if dist_center>GRID_WIDTH//2-2:
                im_number_thresh[i,j] = 0

    # 统计非零像素数,以判断方格中是否有数字
    n_active_pixels=cv2.countNonZero(im_number_thresh)

    return [im_number_thresh,n_active_pixels]

def find_biggest_bounding_box(im_number_thresh):
    """
    找出小方格中外接矩形面积最大的轮廓，返回其外接矩形参数
    :param im_number_thresh: 当前方格的二值化及处理后图像
    :return: 外接矩形参数（左上坐标及长和宽）
    """
    # 轮廓检测
    b,contour, hierarchy1 = cv2.findContours(im_number_thresh.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)

    # 找出外接矩形面积最大的轮廓
    biggest_bound_rect=[]
    bound_rect_max_size=0
    for i in range(len(contour)):
        bound_rect=cv2.boundingRect(contour[i])
        size_bound_rect=bound_rect[2]*bound_rect[3]
        if size_bound_rect>bound_rect_max_size:
            bound_rect_max_size=size_bound_rect
            biggest_bound_rect=bound_rect

    # 将外接矩形扩大一个像素
    x_b,y_b,w,h=biggest_bound_rect
    x_b-=1
    y_b-=1
    w+=2
    h+=2
    return [x_b,y_b,w,h]

def extract_number(im_number):
    """
    判断当前方格是否存在数字并存储该数字
    :param im_number: 方格图像
    :return: 是否有数字，数字的一维数组
    """
    # 预处理方格图像
    [im_number_thresh,n_active_pixels]=preprocess_grid(im_number)

    # 条件1：非零像素大于设定的最小值
    if n_active_pixels>N_MIN_ACTIVE_PIXELS:

        # 找出外接矩形
        [x_b,y_b,w,h]=find_biggest_bounding_box(im_number_thresh)

        # 计算矩形中心与方格中心距离
        cX=x_b+w//2
        cY=y_b+h//2
        d=np.sqrt(np.square(cX-GRID_WIDTH//2)+np.square(cY-GRID_HEIGHT//2))

        # 条件2: 外接矩形中心与方格中心距离足够小
        if d<GRID_WIDTH//4:

            # 取出方格中数字
            number_roi=im_number[y_b:y_b+h,x_b:x_b+w]

            # 扩充数字图像为正方形，边长取长宽较大者
            h1,w1=np.shape(number_roi)
            if h1>w1:
                number=np.zeros(shape=(h1,h1))
                number[:,(h1-w1)//2:(h1-w1)//2+w1]=number_roi
            else:
                number=np.zeros(shape=(w1,w1))
                number[(w1-h1)//2:(w1-h1)//2+h1,:]=number_roi

            # 将数字缩放为标准大小
            number=cv2.resize(number,(NUM_WIDTH,NUM_HEIGHT),interpolation=cv2.INTER_LINEAR)

            retVal,number=cv2.threshold(number,50,255,cv2.THRESH_BINARY)

            # 转换为1维数组并返回
            return True,number.reshape(1,NUM_WIDTH*NUM_HEIGHT)

    # 没有数字，则返回全零1维数组
    return False,np.zeros(shape=(1,NUM_WIDTH*NUM_HEIGHT))
