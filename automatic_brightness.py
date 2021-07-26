from cv2 import cv2
from PIL import Image
from PIL import ImageStat
import screen_brightness_control as sbc

cap = cv2.VideoCapture(0)

face_detect = cv2.CascadeClassifier(r"D:\Users\Programs\Python\Python39\Lib\site-packages\cv2\data\haarcascade_frontalface_alt.xml")

warn_dist = 0
flag_1 = 0
while True:
    # 读取视频片段
    flag, frame = cap.read()
    if flag == False:
        print("失败")
        break

    # 灰度处理
    gray = cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)
    # 平均亮度
    im=Image.fromarray(gray)
    stat=ImageStat.Stat(im)
    brightness = int(stat.rms[0]*40/255)

    # 检查人脸 按照1.1倍放到 周围最小像素为5
    face_zone = face_detect.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5)

    # 绘制圆形检测人脸
    num = 0
    
    for x, y, w, h in face_zone:
        num = num + 1
        cv2.circle(frame, center = (x + w//2, y + h//2), radius = w//2, color = [0,255,0], thickness = 2)
        cv2.putText(frame, str(num), (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
        warn_dist = w//2
        
    # 显示图片
    cv2.putText(frame, "{}people".format(num), (10,50), cv2.FONT_HERSHEY_COMPLEX, 1, (142, 125, 52), 1)
    cv2.imshow('video', frame)
    
    if warn_dist > 140:
        print("\r\n",'      太近了，端正坐姿       ',end="",flush=True)
        
    if num == 0:
        if flag_1 > 5:
            flag_1 = 6
            print("\r\n",'检测到人员离开，启用低亮度',end="",flush=True)
            sbc.set_brightness(0)
        else:
            flag_1 = flag_1 + 1
    else:
        flag_1 = 0
        print("\r\n",f'         正常运行{brightness}        ',end="",flush=True)
        sbc.set_brightness(brightness)

    # 以较慢帧率运行 空格退出 500为了控制运行速度
    if ord(' ') == cv2.waitKey(500):
        break

cap.release()

cv2.destroyAllWindows()
