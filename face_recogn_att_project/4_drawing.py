#!/usr/bin/python3

import numpy as np
import cv2

canvas = np.zeros((300, 300, 3), dtype="uint8")
"""
cv2.imshow('canvas', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
for row in range (0, 300):
    for col in range (0, 300):
        canvas[row][col] = [255, 255, 255]
green = [0, 255, 0]
cv2.line(canvas, (0,0), (300, 300), green)
cv2.imshow('canvas', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.rectangle(canvas, (10, 10), (30, 30), green)
cv2.imshow('canvas_rectangle', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
red = [0, 0, 255]
cv2.rectangle(canvas, (50, 200), (200, 225), red, 5)
cv2.imshow('canvas_rectangle', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
blue = [255, 0, 0]
cv2.rectangle(canvas, (200, 50), (225, 200), blue, -1)
cv2.imshow('canvas_rectangle', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
center = (150, 150)
radius = 10
thickness = 3
cv2.circle(canvas, center, radius, (0, 0, 0), thickness)
cv2.imshow('circle', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('./images/canvas.png', canvas)
for r in range (0, 175, 25):
    cv2.circle(canvas, center, r, (0, 0, 0), thickness)
cv2.imshow('canvas_circle', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
