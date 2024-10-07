import time
import RPi.GPIO as GPIO
from signal import pause
import cv2
import threading 
import numpy as np 
import keyboard
import twophase.solver  as sv
import random
import os
import os.path
import sys
from color_recognition_api_hsv import color_histogram_feature_extraction
from color_recognition_api_hsv import knn_classifier
from collections import Counter
correct = [0,2,4,6,8]
check = 0
global frame_cap_initial
frame_cap_initial = [[[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]]
# frame_cap_initial = []
# for i in range(12):
#     inner_list = []
#     for j in range(6):
#         inner_list.append([] * 5)
#     frame_cap_initial.append(inner_list)
global  state_initial 
state_initial =  {
            'up':['white','white','white','white','white','white','white','white','white',],
            'right':['white','white','white','white','white','white','white','white','white',],
            'front':['white','white','white','white','white','white','white','white','white',],
            'down':['white','white','white','white','white','white','white','white','white',],
            'left':['white','white','white','white','white','white','white','white','white',],
            'back':['white','white','white','white','white','white','white','white','white',]
        }
global frame_cap 
global state
frame_cap = frame_cap_initial
state = state_initial
sign = ['up','right','front','down','left','back']
nuke = {
    'up': 'yellow',
    'right': 'red',
    'front': 'blue',
    'down': 'white',
    'left': 'orange',
    'back': 'green',
}
sign_conv={
            'green'  : 'B',
            'white'  : 'D',
            'blue'   : 'F',
            'red'   : 'R',
            'orange' : 'L',
            'yellow' : 'U'
          }
box = [
            [180, 190], [305, 185], [430, 180],
            [150, 236], [300, 236], [456, 225],
            [120, 315], [310, 300], [495, 305]
        ]
main = [
            [20, 20], [54, 20], [88, 20],
            [20, 54], [54, 54], [88, 54],
            [20, 88], [54, 88], [88, 88]
]
color = {
        'red'    : (0,0,255),
        'orange' : (0,165,255),
        'blue'   : (255,0,0),
        'green'  : (0,255,0),
        'white'  : (255,255,255),
        'yellow' : (0,255,255),
        'test'   : (0,0,0)
        }
raw= ''
answer = ""
PATH = "/home/asus/Desktop/hoan_hao/training_hsv.data"
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
prediction = 'n.a.'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    print ('training data is ready, classifier is loading...')
else:
    print ('training data is being created...')
    open('training_hsv.data', 'w')
    color_histogram_feature_extraction.training()
    print ('training data is ready, classifier is loading...')
def scan_U():
    k = 0
    run_L(3)
    run_R(1)
    time.sleep(1.3)
    upgrade_color(k)
    k = k+1
    run_L(1)
    run_R(3)
    run_U(1)
    run_L(3)
    run_R(1)
    time.sleep(1.3)
    upgrade_color(k)
    k = k+1
    run_L(1)
    run_R(3)
    run_U(3)
def scan_R():
    k = 2
    run_U(3)
    run_D(1)
    time.sleep(1.3)
    upgrade_color(k)
    k = k+1
    run_U(1)
    run_D(3)
    run_R(1)
    run_U(3)
    run_D(1)
    time.sleep(1.3)
    upgrade_color(k)
    run_D(3)
    run_U(1)
    run_R(3)
def scan_F():
    k = 4
    time.sleep(1.3)
    upgrade_color(k)
    k = k+1
    upgrade_color(k)
def scan_D():
    k = 6
    run_L(1)
    run_R(3)
    time.sleep(1.3)
    upgrade_color(k)
    k = k+1
    run_L(3)
    run_R(1)
    run_D(1)
    run_L(1)
    run_R(3)
    time.sleep(1.3)
    upgrade_color(k)
    run_L(3)
    run_R(1)
    run_D(3)
def scan_L():
    k = 8
    run_U(1)
    run_D(3)
    time.sleep(1.3)
    upgrade_color(k)
    k = k+1
    run_D(1)
    run_U(3)
    run_L(1)
    run_D(3)
    run_U(1)
    time.sleep(1.3)
    upgrade_color(k)
    run_U(3)
    run_D(1)
    run_L(3)
def scan_B():
    k = 10 
    run_U(2)
    run_D(2)
    time.sleep(1.3)
    upgrade_color(k)
    k = k + 1
    run_U(2)
    run_D(2)
    run_B(1)
    run_U(2)
    run_D(2)
    time.sleep(1.3)
    upgrade_color(k)
    run_D(2)
    run_U(2)
    run_B(3)
def scan_color():
    scan_U()
    scan_R()
    scan_F()
    scan_D()
    scan_L()
    scan_B()

def control_GPIO():
    GPIO.output(buzzer,1)
    time.sleep(0.3)
    GPIO.output(buzzer,0)
    time.sleep(0.3)
    GPIO.output(buzzer,1)
    time.sleep(0.3)
    GPIO.output(buzzer,0)
    time.sleep(0.3)
    while True:
        global frame_cap 
        global state
        global answer
        answer=''
        state =  {
            'up':['white','white','white','white','white','white','white','white','white',],
            'right':['white','white','white','white','white','white','white','white','white',],
            'front':['white','white','white','white','white','white','white','white','white',],
            'down':['white','white','white','white','white','white','white','white','white',],
            'left':['white','white','white','white','white','white','white','white','white',],
            'back':['white','white','white','white','white','white','white','white','white',]
        }
        frame_cap = [[[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]]
        if GPIO.input(out) == GPIO.LOW:
            GPIO.output(buzzer,1)
            time.sleep(0.3)
            GPIO.output(buzzer,0)
            time.sleep(0.3)
            break
        if GPIO.input(button_puzzle) == GPIO.LOW:
            GPIO.output(buzzer,1)
            time.sleep(0.3)
            GPIO.output(buzzer,0)
            time.sleep(0.3)
            puzzle()
            GPIO.output(buzzer,1)
            time.sleep(0.3)
            GPIO.output(buzzer,0)
            time.sleep(0.3)
            # print("hello")
        if GPIO.input(button_solve) == GPIO.LOW:
            GPIO.output(buzzer,1)
            time.sleep(0.3)
            GPIO.output(buzzer,0)
            time.sleep(0.3)
            state =  {
            'up':['white','white','white','white','white','white','white','white','white',],
            'right':['white','white','white','white','white','white','white','white','white',],
            'front':['white','white','white','white','white','white','white','white','white',],
            'down':['white','white','white','white','white','white','white','white','white',],
            'left':['white','white','white','white','white','white','white','white','white',],
            'back':['white','white','white','white','white','white','white','white','white',]
        }
            frame_cap = [[[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]],
             [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]]
            # print(frame_cap)
            # print(state)
            scan_color()
            for b in range(5):
                state = rubiko(b)
                answer=check(state)
                # print("answer{}: ".format(b) + answer)
                if(answer[-1]==")"):
                    GPIO.output(buzzer,1)
                    time.sleep(0.3)
                    GPIO.output(buzzer,0)
                    time.sleep(0.3)
                    GPIO.output(buzzer,1)
                    time.sleep(0.3)
                    GPIO.output(buzzer,0)
                    time.sleep(0.3)
                    solve(answer)
                    # print("reset")
                    break
                time.sleep(1)
            GPIO.output(buzzer,1)
            time.sleep(0.1)
            GPIO.output(buzzer,0)
            time.sleep(0.1)
            GPIO.output(buzzer,1)
            time.sleep(0.1)
            GPIO.output(buzzer,0)
            time.sleep(0.1)
            time.sleep(1)
            GPIO.output(buzzer,1)
            time.sleep(0.1)
            GPIO.output(buzzer,0)
            time.sleep(0.1)
            GPIO.output(buzzer,1)
            time.sleep(0.1)
            GPIO.output(buzzer,0)
            time.sleep(0.1)
            time.sleep(1)
            GPIO.output(buzzer,1)
            time.sleep(0.1)
            GPIO.output(buzzer,0)
            time.sleep(0.1)
            GPIO.output(buzzer,1)
            time.sleep(0.1)
            GPIO.output(buzzer,0)
            time.sleep(0.1)
            time.sleep(1)
            GPIO.output(buzzer,1)
            time.sleep(0.1)
            GPIO.output(buzzer,0)
            time.sleep(0.1)
            GPIO.output(buzzer,1)
            time.sleep(0.1)
            GPIO.output(buzzer,0)
            time.sleep(0.1)
        
        if GPIO.input(button_reset) == GPIO.LOW:
            GPIO.output(ENA_U, 1)
            GPIO.output(ENA_D, 1)
            GPIO.output(ENA_F, 1)
            GPIO.output(ENA_B, 1)
            GPIO.output(ENA_R, 1)
            GPIO.output(ENA_L, 1)
            GPIO.output(ENA__, 1)
                

    # puzzle()
    # scan_color()
    # solve(state)
    # color_change()
def puzzle():
    functions = [run_U, run_D, run_L, run_R, run_F, run_B]
    GPIO.output(DIR__, 1)# 1 di xuong
    delay__ = .0002

    GPIO.output(ENA__, 0)
    for t in range(10200):
        GPIO.output(STEP__,1)
        time.sleep(delay__)
        GPIO.output(STEP__,0)
        time.sleep(delay__)
    GPIO.output(ENA__, 1)
    for i in range (1,random.randint(25,40)):
        random_function = random.choice(functions)
        random_function(random.randint(1,3))
    GPIO.output(DIR__, 0)
    GPIO.output(ENA__, 0)
    for t in range(10000):
        GPIO.output(STEP__,1)
        time.sleep(delay__)
        GPIO.output(STEP__,0)
        time.sleep(delay__)
    GPIO.output(ENA__, 1)
def check(state):
    raw=''
    for i in state:
        for j in state[i]:
            raw+=sign_conv[j]
    print("answer:",sv.solve(raw))
    answer = sv.solve(raw)
    return answer          
def solve(answer):

    #U2 B2 R2 U3 B1 U1 L3 U3 D3 R1 U3 D2 B3 L2 B3 U2 F2 B3 L2 B2 (20f)
    GPIO.output(DIR__, 1)# 1 di xuong
    delay__ = .0002

    GPIO.output(ENA__, 0)
    for t in range(10200):
        GPIO.output(STEP__,1)
        time.sleep(delay__)
        GPIO.output(STEP__,0)
        time.sleep(delay__)
    GPIO.output(ENA__, 1)
    for i in range(len(answer)):
           if answer[i] ==  'U':
                  run_U(4 - int(answer[i+1]))
           if answer[i] ==  'R':
                  run_R(4 - int(answer[i+1]))
           if answer[i] == 'F':
                  run_F(4 - int(answer[i+1]))
           if answer[i] == 'D':
                  run_D(4 - int(answer[i+1]))
           if answer[i] == 'L':
                  run_L(4 - int(answer[i+1]))
           if answer[i] == 'B':
                  run_B(4 - int(answer[i+1]))
           if answer[i] == '(':
                    break
    GPIO.output(DIR__, 0)
    GPIO.output(ENA__, 0)
    for t in range(10000):
        GPIO.output(STEP__,1)
        time.sleep(delay__)
        GPIO.output(STEP__,0)
        time.sleep(delay__)
    GPIO.output(ENA__, 1)              
    # back_value = write_read(sv.solve(raw))
    # print(back_value)
def color_detect(h,s,v):
    # print(h,s,v)
    if ( h < 9 or h > 150 ) and s > 50  :
        return 'red'
    elif ( h > 8 and h < 30 ) and s > 40 :
        return 'orange'
    else :
        return 'yellow'
def rubiko(b):
    global frame_cap
    global state
    global state_initial
    state=state_initial
    for k in range(12):
        current_state = []
        for t in range(9):
            # print("{}".format(k) +" "+ "{}".format(t) +" "+ "{}".format(b))
            color_histogram_feature_extraction.color_histogram_of_test_image(frame_cap[k][t][b][0])
            prediction = knn_classifier.main('training_hsv.data','test_hsv.data')
            # if prediction == 'red' or prediction == 'orange':
            #     b_channel, g_channel, r_channel = cv2.split(frame_cap[k][t][b][0])
            #     average_green = np.mean(g_channel)
            #     average_blue = np.mean(b_channel)
            #     if average_green - average_blue > 10 and average_green > 100:
            #         prediction = 'orange'
            #     else:
            #         prediction = 'red'
                    
            # if prediction == "yellow" or prediction == "red" or prediction == "orange":
            #     frame = cv2.cvtColor(frame_cap[k][t][b][0], cv2.COLOR_BGR2HSV)
            #     h, s, v = cv2.split(frame)
            #     h_mean = np.mean(h)
            #     s_mean = np.mean(s)
            #     v_mean = np.mean(v) 
            #     print(" {} ".format(h_mean) + " {} ".format(s_mean) + " {} ".format(v_mean))
            #     prediction = color_detect(h_mean,s_mean,v_mean) 
            current_state.append(prediction)
        # print(current_state)
        if k%2 == 0:
                # previous_state = state[sign[k//2]]
            # print(previous_state)
            state[sign[k//2]] = current_state
            # print("1")
        else: 
            if k == 1:
                state[sign[k//2]][1] = current_state[3]
                state[sign[k//2]][4] = nuke[sign[k//2]]
                state[sign[k//2]][7] = current_state[5]
                # print("2")
            if k == 3:
                state[sign[k//2]][3] = current_state[7]
                state[sign[k//2]][4] = nuke[sign[k//2]]
                state[sign[k//2]][5] = current_state[1]
            if k == 7:
                state[sign[k//2]][1] = current_state[3]
                state[sign[k//2]][4] = nuke[sign[k//2]]
                state[sign[k//2]][7] = current_state[5]
            if k == 9:
                state[sign[k//2]][3] = current_state[7]
                state[sign[k//2]][4] = nuke[sign[k//2]]
                state[sign[k//2]][5] = current_state[1]
            if k == 11:
                state[sign[k//2]][3] = current_state[7]
                state[sign[k//2]][4] = nuke[sign[k//2]]
                state[sign[k//2]][5] = current_state[1]
            print(state[sign[k//2]])
    return state   

def upgrade_color(k):
    global frame_cap
   
    
    # if k <= 11:
    #     print(k)
        
    for t in range(9): 
        # cv2.imshow("{}_{}".format(i,t),source_image[trace[t][0]:trace[t][1],trace[t][2]:trace[t][3]])
        for b in range(5):
            # frame_cap[k][t][b].append(img[trace[t][0]:trace[t][1],trace[t][2]+correct[b]:trace[t][3]])
            # print("{}".format(k) +" "+ "{}".format(t) +" "+ "{}".format(b))
            frame_cap[k][t][b].append(img[trace[t][0]:trace[t][1],trace[t][2]+correct[b]:trace[t][3]])
            # print("{}".format(k) +" "+ "{}".format(t) +" "+ "{}".format(b))
                # color_histogram_feature_extraction.color_histogram_of_test_image(img[trace[t][0]:trace[t][1],trace[t][2]+correct[b]:trace[t][3]])
                #  
            # counter = Counter(prediction)
            # most_common_values = counter.most_common(1)
            # most_common_value = most_common_values[0][0]
            # current_state.append(most_common_value)
        #         current_state[b].append(predict)
        # print(current_state)
        # for b in range(10):
        #     if k%2 == 0:
        #         # previous_state = state[sign[k//2]]
        #         # print(previous_state)
        #         state[b][sign[k//2]] = current_state[b]
        #         # print("1")
        #     else: 
        #         if k == 1:
        #             state[b][sign[k//2]][1] = current_state[b][3]
        #             state[b][sign[k//2]][4] = nuke[sign[k//2]]
        #             state[b][sign[k//2]][7] = current_state[b][5]
        #             # print("2")
        #         if k == 3:
        #             state[b][sign[k//2]][3] = current_state[b][7]
        #             state[b][sign[k//2]][4] = nuke[sign[k//2]]
        #             state[b][sign[k//2]][5] = current_state[b][1]
        #         if k == 7:
        #             state[b][sign[k//2]][1] = current_state[b][3]
        #             state[b][sign[k//2]][4] = nuke[sign[k//2]]
        #             state[b][sign[k//2]][7] = current_state[b][5]
        #         if k == 9:
        #             state[b][sign[k//2]][3] = current_state[b][7]
        #             state[b][sign[k//2]][4] = nuke[sign[k//2]]
        #             state[b][sign[k//2]][5] = current_state[b][1]
        #         if k == 11:
        #             state[b][sign[k//2]][3] = current_state[b][7]
        #             state[b][sign[k//2]][4] = nuke[sign[k//2]]
        #             state[b][sign[k//2]][5] = current_state[b][1]
        #         print(state[b][sign[k//2]])
    
cap = cv2.VideoCapture(0) 
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 60  
#video_writer = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
GPIO.setwarnings(False)
button_solve = 21
button_puzzle = 20
button_reset = 13
out = 19
ENA_F = 4
STEP_F = 3
DIR_F = 2
buzzer = 26
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
GPIO.setup(button_reset, GPIO.IN)
GPIO.setup(out, GPIO.IN)
GPIO.setup(buzzer, GPIO.OUT)
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
delay = .0002
GPIO.output(DIR_U, 1)
GPIO.output(DIR_D, 1)
GPIO.output(DIR_L, 1)
GPIO.output(DIR_R, 1)
GPIO.output(DIR_B, 1)
GPIO.output(DIR_F, 1)
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

gpio_thread = threading.Thread(target=control_GPIO)
gpio_thread.start()
start_time = time.time()
while True:
    ret, img = cap.read()
    if not ret:
        break
    cv2.waitKey(0)
gpio_thread.join()

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
sys.exit(0)
