import sys
from SerialPort import *
from Detector import *
from threading import Thread

DEBUG = False
DISPLAY = False

task = None
task_end_flag= False
task_running = False

hsv = None

# 颜色采集
def mouse_click(event, x, y, flags, para):
    global hsv
    if event == cv2.EVENT_LBUTTONDOWN:  # 左边鼠标点击
        print('#'*25)
        print('PIX:', x, y)
        #print("BGR:", frame[y, x])
        #print("GRAY:", gray[y, x])
        print("HSV:", hsv[y, x])

def display():
    global hsv, task_end_flag, task_running, DISPLAY
    task_running = True
    detector = Detector()
    #cv2.namedWindow("cam", 1)
    #video = "http://admin:admin@192.168.43.1:8081/"
    #cam = cv2.VideoCapture(video)
    cv2.namedWindow("cam", cv2.WINDOW_NORMAL)
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    cv2.setMouseCallback("cam", mouse_click)
    result_last = {}
    while True:
        # 读取当前帧
        ret, frame = cam.read()
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # 对图像进行识别
        detector.run(frame)
        if detector.status and result_last != detector.result:
            result_last = detector.result.copy()
            for result in detector.result:
                if detector.status == 1:
                    print(f"检测到二维码> 类别: {result['type']}, 内容: {result['content']}")
                else:
                    print(f"检测到色块> 颜色: {result['content']}, 大小: {result['size']}")
        cv2.imshow("cam", detector.img)
        # 按ESC键退出
        if (cv2.waitKey(5) == 27):
            DISPLAY = False
            break
        if task_end_flag:
            break
    task_running = False
    cam.release()
    cv2.destroyAllWindows()

def detect_qrcode(detector, sp):
    global task_end_flag, DEBUG, task_running
    task_running = True
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
    task_running = False
    cam.release()

def detect_color(detector, sp):
    global task_end_flag, DEBUG, task_running
    task_running = True
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
                    if DEBUG:
                        print(result['size'])
                    res_color.append(result['content'])
                    cnt += 1
        if task_end_flag:
            break
    if not task_end_flag:
        t = [color_dict[color] for color in res_color]
        if DEBUG:
            print(res_color, t)
        sp.sendData(_byte=t)
    task_running = False
    cam.release()

def main():
    global task_end_flag, task, DEBUG, task_running

    detector = Detector()

    with SerialPort() as sp:
        while True:
            if sp.receiveData():
                # 复位检测器
                detector.reset()
                try:
                    detect_type = sp.getReceive()['byte'][0]
                    if DEBUG:
                        print(detect_type)

                    if detect_type == 1:
                        if task is not None and task_running:
                            task_end_flag = True
                            task.join()
                            task_end_flag = False
                        task = Thread(target=detect_qrcode, args=[detector, sp,])
                        task.start()
                    elif detect_type == 2:
                        if task is not None and task_running:
                            task_end_flag = True
                            task.join()
                            task_end_flag = False
                        task = Thread(target=detect_color, args=[detector, sp,])
                        task.start()
                except:
                    pass
            else:
                if not task_running and DISPLAY:
                    task = Thread(target=display)
                    task.start()

if __name__ == '__main__':
    if 'DEBUG' in sys.argv:
        DEBUG = True

    if 'DISPLAY' in sys.argv:
        DISPLAY = True
        task = Thread(target=display)
        task.start()

    main()
