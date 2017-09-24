import cv2
import numpy as np

cap = cv2.VideoCapture(0)
lower_yellow = np.array([20,100,80])
upper_yellow = np.array([100,255,255])

while(1):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    median = cv2.medianBlur(res,13)

    cv2.imshow('median',median)


cv2.destroyAllWindows()
cap.release()