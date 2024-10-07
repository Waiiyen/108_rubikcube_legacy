import time
import RPi.GPIO as GPIO
from signal import pause
import cv2
import threading 
import numpy as np 
import keyboard
#import twophase.solver  as sv
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
    elif ( h > 31 and h < 50) and s > 5 :
        return 'yellow'
    elif ( h >= 50 and h <= 80) and s > 60:
        return 'green'
    elif ( h >= 90 and h <= 130) and s > 70:
        return 'blue'   
    elif h > 50 and s < 70:
        return 'white'
    else:
        return 'test'

def upgrade_color(k):
    if k <= 11:
        print(k)
        hsv=[]
        h=[]
        s=[]
        v=[]
        current_state = []
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #mask = np.zeros(frame.shape, dtype=np.uint8) 
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
        #cv2.imshow("Camera Feed", frame)
        cv2.imshow("Camera Feed", img)
        print(h)
        print(s)
        print(v)
        print(current_state)
        
cap = cv2.VideoCapture(0) 
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 60  

while True:
    ret, img = cap.read()
    
    upgrade_color(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break
cap.release()
cv2.destroyAllWindows()

