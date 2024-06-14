#!/usr/bin/python3

import numpy as np
import cv2

img = cv2.imread('./images/faces.jpg')
cv2.imshow('face', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

face_detection_model = cv2.dnn.readNetFromCaffe('./model/deploy.prototxt', './model/res10_300x300_ssd_iter_140000_fp16.caffemodel')

