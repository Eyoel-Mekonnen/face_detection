#!/usr/bin/python3

import cv2
import numpy as np

def sliding_window(canvas, window_size):
    """this function recive canvas(image) and size of the window ex 2 means 2x2"""
    green = (0, 255, 0)
    red = (0, 0, 255)
    blue = (255, 0, 0)
    gray_image = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    I = np.zeros((canvas.shape[0] + 1, canvas.shape[1] + 1), dtype=np.int64)
    for y in range (1, gray_image.shape[0]):
        for x in range(1, gray_image.shape[1] + 1):
            I[y,x] = gray_image[y - 1, x - 1] + I[y - 1, x] + I[y, x - 1] - I[y - 1, x - 1]
    print(I)
    print("Size is {} and {}".format(canvas.shape[0], canvas.shape[1]))
    loop_y = canvas.shape[0] // window_size
    loop_x = canvas.shape[1] // window_size
    if loop_y < loop_x:
        iteration_size = loop_y
    else:
        iteration_size = loop_x
    print("Loop y is {}".format(loop_y))
    print("Loop x is {}".format(loop_x))
    for y in range(0, iteration_size * window_size, window_size):
        for x in range(0, iteration_size * window_size, window_size):
            cv2.rectangle(canvas, (x, y), (x + window_size - 1, y + window_size - 1), green, 1)
            cv2.rectangle(canvas, (x, y), (x + window_size // 2, y + window_size - 1), red, 1)
            cv2.rectangle(canvas, (x + window_size // 2, y), (x + window_size - 1, y + window_size - 1), blue, 1)
            left_x2 = min(x + window_size // 2, canvas.shape[1] - 1)
            left_y2 = min(y + window_size - 1, gray_image.shape[0] - 1)
            right_x1 = min(x + window_size // 2, canvas.shape[0] - 1)
            right_x2 = min(x + window_size - 1, gray_image.shape[1] - 1)
            right_y2 = min(y + window_size - 1, gray_image.shape[0] - 1)
            left_haar_sum = I[left_x2 + 1, left_y2 + 1] - I[x, left_y2 + 1] - I[left_x2 + 1, y] + I[x, y]
            right_haar_sum = I[right_x2 + 1, right_y2 + 1] - I[right_x1, y + 1] - I[right_x2 + 1, y] + I[right_x1, y]
            value = left_haar_sum - right_haar_sum
            print(value)
            #print("Left haar_sum is {}".format(left_haar_sum))
            #print("Right haar_sum is {}".format(right_haar_sum))
    cv2.imshow('sliding window', canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(gray_image)
canvas = cv2.imread('./images/eagle.jpg')
window_size = 50
sliding_window(canvas, window_size)
