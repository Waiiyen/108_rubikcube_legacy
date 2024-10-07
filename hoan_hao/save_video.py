import time
import RPi.GPIO as GPIO
from signal import pause
import cv2
import threading 
import numpy 
import keyboard
import twophase.solver  as sv
import random
import os
import os.path
import sys
from color_recognition_api import color_histogram_feature_extraction
from color_recognition_api import knn_classifier
from collections import Counter
raw= ''
PATH = "/home/asus/Desktop/hoan_hao/training.data"
trace = [
    [195,210,190,260], #0
    [190,210,300,380], #1
    [180,200,420,500], #2
    [230,260,160,245], #3
    [230,260,300,400], #4
    [220,250,435,535], #5
    [290,340,105,220],  #6
    [290,340,290,410], #7
    [290,340,480,600]] #8
prediction = 'n.a.'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    print ('training data is ready, classifier is loading...')
else:
    print ('training data is being created...')
    open('training.data', 'w')
    color_histogram_feature_extraction.training()
    print ('training data is ready, classifier is loading...')
GPIO.setwarnings(False)
button_solve = 21
button_puzzle = 20

ENA_F = 4
STEP_F = 3
DIR_F = 2

ENA_D = 22
STEP_D = 27
DIR_D = 17

ENA_U = 11
STEP_U = 9
DIR_U = 10

ENA_R = 0
STEP_R = 5
DIR_R = 6

ENA_L = 8
STEP_L = 7
DIR_L = 1

ENA_B = 23
STEP_B = 24
DIR_B = 25

ENA__ = 14
STEP__ = 15
DIR__ = 18

CW = 1
CCW = 0
SPR = 802
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_solve, GPIO.IN)
GPIO.setup(button_puzzle, GPIO.IN)
GPIO.setup(DIR_U,GPIO.OUT)
GPIO.setup(STEP_U,GPIO.OUT)
GPIO.setup(ENA_U,GPIO.OUT)
GPIO.output(ENA_U, 1)

GPIO.setup(DIR_D,GPIO.OUT)
GPIO.setup(STEP_D,GPIO.OUT)
GPIO.setup(ENA_D,GPIO.OUT)
GPIO.output(ENA_D, 1)

GPIO.setup(DIR_L,GPIO.OUT)
GPIO.setup(STEP_L,GPIO.OUT)
GPIO.setup(ENA_L,GPIO.OUT)
GPIO.output(ENA_L, 1)

GPIO.setup(DIR_R,GPIO.OUT)
GPIO.setup(STEP_R,GPIO.OUT)
GPIO.setup(ENA_R,GPIO.OUT)
GPIO.output(ENA_R, 1)

GPIO.setup(DIR_B,GPIO.OUT)
GPIO.setup(STEP_B,GPIO.OUT)
GPIO.setup(ENA_B,GPIO.OUT)
GPIO.output(ENA_B, 1)

GPIO.setup(DIR_F,GPIO.OUT)
GPIO.setup(STEP_F,GPIO.OUT)
GPIO.setup(ENA_F,GPIO.OUT)
GPIO.output(ENA_F, 1)

GPIO.setup(DIR__,GPIO.OUT)
GPIO.setup(STEP__,GPIO.OUT)
GPIO.setup(ENA__,GPIO.OUT)
GPIO.output(ENA__, 1)
step_count = SPR
delay = .00002
GPIO.output(DIR_U, 1)
GPIO.output(DIR_D, 1)
GPIO.output(DIR_L, 1)
GPIO.output(DIR_R, 1)
GPIO.output(DIR_B, 1)
GPIO.output(DIR_F, 1)
def detect(): 
    current_state = []
    
    for t in range(9):
        prediction = [] 
        # cv2.imshow("{}_{}".format(i,t),source_image[trace[t][0]:trace[t][1],trace[t][2]:trace[t][3]])
        for o in range(5):
            color_histogram_feature_extraction.color_histogram_of_test_image(frame[trace[t][0]:trace[t][1],trace[t][2]:trace[t][3]])
            predict = knn_classifier.main('training.data','test.data')
            prediction.append(predict)
        counter = Counter(prediction)
        most_common_values = counter.most_common(1)
        most_common_value = most_common_values[0][0]
        current_state.append(most_common_value)     
        if most_common_value == "red" :
            cv2.rectangle(frame,(trace[t][2],trace[t][0]),(trace[t][3],trace[t][1]),(0,0,255),-1)
        elif most_common_value == "orange" :
            cv2.rectangle(frame,(trace[t][2],trace[t][0]),(trace[t][3],trace[t][1]),(51,153,255),-1)
        elif most_common_value == "yellow" :
            cv2.rectangle(frame,(trace[t][2],trace[t][0]),(trace[t][3],trace[t][1]),(51,255,255),-1)
        elif most_common_value == "green":
            cv2.rectangle(frame,(trace[t][2],trace[t][0]),(trace[t][3],trace[t][1]),(0,255,0),-1)
        elif most_common_value == "blue":
            cv2.rectangle(frame,(trace[t][2],trace[t][0]),(trace[t][3],trace[t][1]),(255,0,0),-1)
        elif most_common_value == "white":
            cv2.rectangle(frame,(trace[t][2],trace[t][0]),(trace[t][3],trace[t][1]),(255,255,255),-1)
    print(current_state)
def run_U(u):
			GPIO.output(ENA_U, 0)
			for t in range(step_count*u):
				GPIO.output(STEP_U,1)
				time.sleep(delay)
				GPIO.output(STEP_U,0)
				time.sleep(delay)
			GPIO.output(ENA_U,1)
def run_D(d):
			GPIO.output(ENA_D, 0)
			for t in range(step_count*d):
				GPIO.output(STEP_D,1)
				time.sleep(delay)
				GPIO.output(STEP_D,0)
				time.sleep(delay)
			GPIO.output(ENA_D, 1)
def run_L(l):
			GPIO.output(ENA_L, 0)
			for t in range(step_count*l):
				GPIO.output(STEP_L,1)
				time.sleep(delay)
				GPIO.output(STEP_L,0)
				time.sleep(delay)
			GPIO.output(ENA_L, 1)
def run_R(r):
			GPIO.output(ENA_R, 0)
			for t in range(step_count*r):
				GPIO.output(STEP_R,1)
				time.sleep(delay)
				GPIO.output(STEP_R,0)
				time.sleep(delay)
			GPIO.output(ENA_R, 1)
def run_B(b):
			GPIO.output(ENA_B, 0)
			for t in range(step_count*b):
				GPIO.output(STEP_B,1)
				time.sleep(delay)
				GPIO.output(STEP_B,0)
				time.sleep(delay)
			GPIO.output(ENA_B, 1)
def run_F(f):
			GPIO.output(ENA_F, 0)
			for t in range(step_count*f):
				GPIO.output(STEP_F,1)
				time.sleep(delay)
				GPIO.output(STEP_F,0)
				time.sleep(delay)
			GPIO.output(ENA_F, 1)
def control_GPIO():
    while True:
        time.sleep(2)
        run_B(1)
        run_L(1)
        run_D(1)
        run_R(1)
        run_U(1)
        time.sleep(3)
        detect()
        run_B(1)
        run_L(1)
        run_D(1)
        run_R(1)
        run_U(1)
        time.sleep(3)        
video_capture = cv2.VideoCapture(0) 
gpio_thread = threading.Thread(target=control_GPIO)
gpio_thread.start()
while True:
    ret, frame = video_capture.read() 
    if not ret:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow('Video', frame)
gpio_thread.join()
video_capture.release()
cv2.destroyAllWindows()
GPIO.cleanup()  

