import sys
from SerialPort import *
from Detector import *
from threading import Thread


task_end_flag= False
task = None

def detect_qrcode(detector, sp):
    global task_end_flag
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
    # 识别二维码
    while True:
        # 读取当前帧
        ret, frame = cam.read()
        # 对图像进行识别
        detector.detectQrcode(frame)
        # 判断识别状态
        if detector.status == 1:
            res_qrcode = list(detector.result[0]['content'])
            t = [int(c) for c in res_qrcode]
            if DEBUG:
                print(res_qrcode, t)
            sp.sendData(_byte=t)
            break
        if task_end_flag:
            break
    cam.release()

def detect_color(detector, sp):
    global task_end_flag
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
    color_dict = {'red': 1, 'green': 2, 'blue': 3}
    res_color = []
    # 识别色块
    res_color.clear()
    cnt = 0
    while cnt < 3:
        # 读取当前帧
        ret, frame = cam.read()
        # 对图像进行识别
        detector.detectColor(frame)
        # 判断识别状态
        if detector.status == 2:
            for result in detector.result:
                if result['content'] not in res_color:
                    res_color.append(result['content'])
                    cnt += 1
        if task_end_flag:
            break
    if not task_end_flag:
        t = [color_dict[color] for color in res_color]
        if DEBUG:
            print(res_color, t)
        sp.sendData(_byte=t)
    cam.release()

def main():
    global task_end_flag, task

    detector = Detector()

    with SerialPort() as sp:
        while True:
            if sp.receiveData():
                # 复位检测器
                detector.reset()
                #try:
                detect_type = sp.getReceive()['byte'][0]
                if DEBUG:
                    print(detect_type)

                if detect_type == 1:
                    if task is not None:
                        task_end_flag = True
                        task.join()
                        task_end_flag = False
                    task = Thread(target=detect_qrcode, args=[detector, sp,])
                    task.start()
                elif detect_type == 2:
                    if task is not None:
                        task_end_flag = True
                        task.join()
                        task_end_flag = False
                    task = Thread(target=detect_color, args=[detector, sp,])
                    task.start()


if __name__ == '__main__':
    if 'DEBUG' in sys.argv:
        DEBUG = True
    else:
        DEBUG = False
    main()
