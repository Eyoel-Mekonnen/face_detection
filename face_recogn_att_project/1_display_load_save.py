#!/usr/bin/python3
import numpy as np
import cv2

img = cv2.imread('./images/240_F_594773641_8rrPYslOpBs62dSOWKFi1awSfyj5szni.jpg')
if img is None:
    print("Error")
else:
    print(img)
print(img.shape)
cv2.imshow('example', img)
cv2.waitKey(10000)
cv2.destroyAllWindows()
cv2.imwrite('./images/flamingo.png', img)
img2 = cv2.imread('./images/flamingo.png')
cv2.imshow('example2', img2)
cv2.waitKey(10000)
