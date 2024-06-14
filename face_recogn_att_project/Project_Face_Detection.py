#!/usr/bin/python3

import numpy as np
import cv2

img = cv2.imread('./images/faces.jpg')
face_cascade = cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')
def face_detection(img):
    image = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    box, detections = face_cascade.detectMultiScale2(gray, scaleFactor=1.1, minNeighbors=5)
    print(box)
    print(detections)
    green = (0, 255, 0)
    for x,y,w,h in box:
        cv2.rectangle(image, (x,y), (x + w, y + h), green, 1)
    return image

img_detection = face_detection(img)
cv2.imshow('face', img_detection)
cv2.waitKey(0)
cv2.destroyAllWindows()

cap = cv2.VideoCapture(-1)
face_cascade = cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if ret == False:
        break
    img_detection = face_detection(frame)
    cv2.imshow('Real Time Face Detection', img_detection)
    if cv2.waitKey(1) & 0xFF == ord('a'):
        break
cap.release()
cv2.destroyAllWindows()
