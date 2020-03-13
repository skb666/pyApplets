import numpy as np
import cv2
face_cascade = cv2.CascadeClassifier(r"HaarCascade\haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(r"HaarCascade\haarcascade_eye.xml")
# 开启摄像头
cap = cv2.VideoCapture(0)
while True:
    ret,img=cap.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.1,5)
    if len(faces)>0:
        for faceRect in faces:
            x,y,w,h = faceRect
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h//2,x:x+w]
            roi_color = img[y:y+h//2,x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray,1.1,1,cv2.CASCADE_SCALE_IMAGE,(2,2))
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    cv2.imshow("img",img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
