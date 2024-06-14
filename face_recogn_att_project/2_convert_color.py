#!/usr/bin/python3

import numpy as np
import cv2

img = cv2.imread('./images/flamingo.png')
b,g,r = cv2.split(img)
print(img)
print(b)
cv2.imshow('blue', b)
cv2.imshow('green', g)
cv2.imshow('red', r)
cv2.waitKey(0)
cv2.destroyAllWindows()

