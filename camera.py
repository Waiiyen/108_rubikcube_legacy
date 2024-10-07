import time
import cv2
import numpy as np 
import keyboard
import random
import os
import os.path
import sys
from collections import Counter

trace = [
    [185,210,190,260], #0 
    [185,205,280,360], #1
    [180,200,380,450], #2
    [230,260,170,245], #3
    [240,270,280,360], #4
    [225,260,400,470], #5
    [290,340,160,220],  #6
    [290,340,280,370], #7
    [290,340,410,500]] #8
    
cap = cv2.VideoCapture(0) 
while True:
    ret, img = cap.read()
    for t in range(9):
	    cv2.rectangle(img, (trace[t][2],trace[t][0]), (trace[t][3],trace[t][1]),(0, 255, 0),5)
    if not ret:
	    continue
    cv2.imshow('camera',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
    
    
        
        
