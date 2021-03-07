#!/usr/bin/python3

import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np


class Detector(object):
    """docstring for Detector"""
    def __init__(self, img=None):
        if img is not None:
            self.img = img.copy()
        else:
            self.img = None
        self.status = 0
        self.result = []

    def reset(self):
        self.status = 0
        self.result.clear();

    def detectQrcode(self, img=None):
        if img is not None:
            self.img = img.copy()
        elif self.img is None:
            raise Exception("self.img is None")
        # 转为灰度图像
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)
        for barcode in barcodes:
            # 提取二维码的位置,然后用边框标识出来在视频中
            (x, y, w, h) = barcode.rect
            cv2.rectangle(self.img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # 在图像上面显示识别出来的内容
            cv2.putText(self.img, f"{barcode.type}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # 打印识别后的内容
            self.result.append({
                "type": barcode.type,
                "content": barcode.data.decode('utf-8'),
            })
        if len(barcodes): self.status = 1

    def detectColor(self, img=None):
        if img is not None:
            self.img = img.copy()
        elif self.img is None:
            raise Exception("self.img is None")

        colors = {
            "red": {"lower": np.array([165, 85, 94]),"upper": np.array([175, 255, 255])},
            "blue": {"lower": np.array([105, 135, 90]), "upper": np.array([118, 255, 255])},
            "green": {"lower": np.array([35, 110, 106]), "upper": np.array([77, 255, 255])},
        }
        #把BGR图像转换为HSV格式
        hsv_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        # cv显示识别到的色块
        for color, threshold in colors.items():
            #mask是把HSV图片中在颜色范围内的区域变成白色，其他区域变成黑色
            mask =  cv2.inRange(hsv_img, threshold["lower"], threshold["upper"])
            mask = cv2.medianBlur(mask, 7)  # 中值滤波
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 轮廓检测
            contours.sort(key=lambda x: cv2.contourArea(x), reverse=True)
            # for cnt in contours:
            if len(contours):
                cnt = contours[0]
                (x, y, w, h) = cv2.boundingRect(cnt)
                cv2.rectangle(self.img, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cv2.putText(self.img, color, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                self.status = 2
                self.result.append({
                    "type": "Blocks of color",
                    "content": color,
                })

    def run(self, img=None):
        if img is not None:
            self.img = img.copy()
        elif self.img is None:
            raise Exception("self.img is None")
        self.reset()
        self.detectQrcode()
        if self.status == 0:
            self.detectColor()


if __name__ == '__main__':
    # 颜色采集
    def mouse_click(event, x, y, flags, para):
        if event == cv2.EVENT_LBUTTONDOWN:  # 左边鼠标点击
            print('#'*25)
            print('PIX:', x, y)
            print("BGR:", frame[y, x])
            print("GRAY:", gray[y, x])
            print("HSV:", hsv[y, x])

    detector = Detector()
    #cv2.namedWindow("cam", 1)
    #video = "http://admin:admin@192.168.43.1:8081/"
    #cam = cv2.VideoCapture(video)
    cv2.namedWindow("cam", cv2.WINDOW_NORMAL)
    cam = cv2.VideoCapture(0)
    cv2.setMouseCallback("cam", mouse_click)
    result_last = None
    while True:
        # 读取当前帧
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        detector.run(frame)
        if detector.status and result_last != detector.result:
            result_last = detector.result.copy()
            for result in detector.result:
                if detector.status == 1:
                    print(f"检测到二维码> 类别: {result['type']}, 内容: {result['content']}")
                else:
                    print(f"检测到色块> {result['content']}")
        cv2.imshow("cam", detector.img)
        # 按ESC键退出
        if (cv2.waitKey(5) == 27):
            break
    cam.release()
    cv2.destroyAllWindows()
