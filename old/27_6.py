import time
import RPi.GPIO as GPIO
from signal import pause
import cv2
import threading 
import numpy as np 
import keyboard
import twophase.solver  as sv
check = 0
state=  {
            'up':['white','white','white','white','white','white','white','white','white',],
            'right':['white','white','white','white','white','white','white','white','white',],
            'front':['white','white','white','white','white','white','white','white','white',],
            'down':['white','white','white','white','white','white','white','white','white',],
            'left':['white','white','white','white','white','white','white','white','white',],
            'back':['white','white','white','white','white','white','white','white','white',]
        }
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
            [180, 185], [305, 185], [420, 180],
            [150, 230], [300, 230], [450, 225],
            [130, 300], [300, 300], [480, 300]
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
def color_detect(h,s,v):
    # print(h,s,v)
    if ( h < 8 or h > 150 ) and s > 50  :
        return 'red'
    elif ( h > 7 and h < 30 ) and s > 40 :
        return 'orange'
    elif ( h > 31 and h < 45) and s > 5 :
        return 'yellow'
    elif ( h >= 45 and h <= 80) and s > 60:
        return 'green'
    elif ( h >= 90 and h <= 130) and s > 70:
        return 'blue'
    elif h > 45 and s < 70:
        return 'white'
    else:
        return 'test'
def scan_U():
    k = 0
    run_L(3)
    run_R(1)
    time.sleep(1)
    upgrade_color(k)
    k = k+1
    run_L(1)
    run_R(3)
    run_U(1)
    run_L(3)
    run_R(1)
    time.sleep(1)
    upgrade_color(k)
    k = k+1
    run_L(1)
    run_R(3)
    run_U(3)
def scan_R():
    k = 2
    run_U(3)
    run_D(1)
    time.sleep(1)
    upgrade_color(k)
    k = k+1
    run_U(1)
    run_D(3)
    run_R(1)
    run_U(3)
    run_D(1)
    time.sleep(1)
    upgrade_color(k)
    run_D(3)
    run_U(1)
    run_R(3)
def scan_F():
    k = 4
    time.sleep(1)
    upgrade_color(k)
    k = k+1
    upgrade_color(k)
def scan_D():
    k = 6
    run_L(1)
    run_R(3)
    time.sleep(1)
    upgrade_color(k)
    k = k+1
    run_L(3)
    run_R(1)
    run_D(1)
    run_L(1)
    run_R(3)
    time.sleep(1)
    upgrade_color(k)
    run_L(3)
    run_R(1)
    run_D(3)
def scan_L():
    k = 8
    run_U(1)
    run_D(3)
    time.sleep(1)
    upgrade_color(k)
    k = k+1
    run_D(1)
    run_U(3)
    run_L(1)
    run_D(3)
    run_U(1)
    time.sleep(1)
    upgrade_color(k)
    run_U(3)
    run_D(1)
    run_L(3)
def scan_B():
    k = 10 
    run_U(2)
    run_D(2)
    time.sleep(1)
    upgrade_color(k)
    k = k + 1
    run_U(2)
    run_D(2)
    run_B(1)
    run_U(2)
    run_D(2)
    time.sleep(1)
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
def color_change():
    run_D(1)
    run_U(3)
    run_L(1)
    run_D(3)
    run_U(1)   
    run_R(1)
    run_D(3)
    run_L(1)
    run_U(3)
    run_R(1)
    run_D(1)
    run_U(3)
    run_L(1)
    run_D(3)
    run_U(1)   
    run_R(1)
    run_D(3)
    run_L(1)
    run_U(3)
    run_R(1)
    run_U(3)
    run_R(1)
    run_D(1)
    run_U(3)
    run_L(1)
    run_D(3)
    run_U(1)   
    run_R(1)
    run_D(3)
    run_L(1)
    run_U(3)
    run_R(1)
def control_GPIO():
    scan_color()
    solve(state)
    # color_change()
def solve(state):
    raw=''
    for i in state:
        for j in state[i]:
            raw+=sign_conv[j]
    print("answer:",sv.solve(raw))
    answer = sv.solve(raw)
    #U2 B2 R2 U3 B1 U1 L3 U3 D3 R1 U3 D2 B3 L2 B3 U2 F2 B3 L2 B2 (20f)
    GPIO.output(DIR__, 1)# 1 di xuong
    delay__ = .0001

    GPIO.output(ENA__, 0)
    for t in range(10050):
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
def upgrade_color(k):
    if k <= 11:
        print(k)
        hsv=[]
        h=[]
        s=[]
        v=[]
        current_state = []
        # Read a frame from the camera
        # ret, img = cap.read()
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = np.zeros(frame.shape, dtype=np.uint8) 
        for i in range(9):
            hsv.append(frame[box[i][1]+10][box[i][0]+10])
            a=0
        for x,y in box:
            h.append(hsv[a][0])
            s.append(hsv[a][1])
            v.append(hsv[a][2])
            color_name=color_detect(hsv[a][0],hsv[a][1],hsv[a][2])
            cv2.rectangle(img, (x,y), (x+70, y+20), color[color_name], -1) 
            a+=1
            current_state.append(color_name)
        print(h)
        print(s)
        print(v)
        print(current_state)
        if k%2 == 0:
            previous_state = state[sign[k//2]]
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

    else:
        exit()
cap = cv2.VideoCapture(0) 
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 60  
#video_writer = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
GPIO.setwarnings(False)
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
#     # hsv=[]
#     # h=[]
#     # s=[]
#     # v=[]
#     # current_state = []
#     # # Read a frame from the camera
#     # # ret, img = cap.read()
#     # frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     # mask = np.zeros(frame.shape, dtype=np.uint8) 
#     # for i in range(9):
#     #     hsv.append(frame[box[i][1]+10][box[i][0]+10])
#     #     a=0
#     # for x,y in box:
#     #     h.append(hsv[a][0])
#     #     s.append(hsv[a][1])
#     #     v.append(hsv[a][2])
#     #     color_name=color_detect(hsv[a][0],hsv[a][1],hsv[a][2])
#     #     cv2.rectangle(img, (x,y), (x+70, y+20), color[color_name], -1) 
#     #     a+=1
#     #     current_state.append(color_name)
#     #     print(h)
#     #     print(s)
#     #     print(v)
#     #     print(current_state)
#     cv2.imshow("Camera Feed", img)
#     # output_file.write(img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# #video_writer.release()

gpio_thread.join()

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
