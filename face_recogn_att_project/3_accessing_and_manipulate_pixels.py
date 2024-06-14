#!/usr/bin/python3

import numpy as np
import cv2

img = cv2.imread('./images/eagle.jpg')
cv2.imshow('eagle', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
for row in range (0, 100):
    for col in range(0, 100):
        img[row][col][0] = 55
        img[row][col] = [0, 255, 0]
cv2.imshow('modified', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(img)

