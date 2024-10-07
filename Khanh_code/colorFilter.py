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
            [150, 230], [300, 240], [450, 225],
            [130, 300], [300, 300], [480, 300]
        ]
main = [
            [20, 20], [54, 20], [88, 20],
            [20, 54], [54, 54], [88, 54],
            [20, 88], [54, 88], [88, 88]
]

colorRGB = {
        'red'    : (255,0,0),
        'orange' : (255,100,0),
        'blue'   : (0,0,255),
        'green'  : (0,255,0),
        'white'  : (255,255,255),
        'yellow' : (255,255,0),
        'test'   : (0,0,0)
        }

color = {
        'red'    : (0,0,255),
        'orange' : (0,165,255),
        'blue'   : (255,0,0),
        'green'  : (0,255,0),
        'white'  : (255,255,255),
        'yellow' : (0,255,255),
        'test'   : (0,0,0)
        }

def color_detectRGB(r, g, b):
    
    if r>100 and (abs(g-b)<10) and (abs(r-g )< 10) and (abs(r-b) < 10):
        return 'white'
    elif r >= 150 and ((g-b) > 10) and (r-g > 10) and r > g:
        return 'orange'
    elif r >= 150 and ((g-b) >= 10) and ((g-r) < 30): 
        return 'yellow'
    elif r >= 150 and (abs(g-b) <= 10):
        return 'red' 
    elif g >= 75 and g > b:
        return 'green'
    elif b >= 75 and b > g:
        return 'blue'   
    
    else:
        return 'test'

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

def upgrade_color():
    hsv=[]
    h=[]
    s=[]
    v=[]
    current_state = []
    crop_frame = []  
    frame_read =[0]
    
    #alpha = 0.5
    #eta = 60
    #con_img = cv2.convertScaleAbs(img, alpha = alpha, beta = beta)
    
    new_img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 10, 10)
    frame = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
	
    
    rectangle_y = 20
    rectangle_x = 50

    for i in range(9):
        for u in range(rectangle_y):
            for y in range(rectangle_x):
                frame_read = frame_read +  frame[box[i][1]+ rectangle_y][box[i][0]+ rectangle_x]
        frame_read = frame_read / (rectangle_x*rectangle_y*1.05)
        hsv.append(frame_read)
        a=0
        crop_frame.append(frame[box[i][1]:box[i][1] + rectangle_y,box[i][0]:box[i][0]+rectangle_x])
    #print(np.asarray(crop_frame[1]).shape)
    for x,y in box:
        hsv[a][0] = int(hsv[a][0])  
        hsv[a][1] = int(hsv[a][1])
        hsv[a][2] = int(hsv[a][2])
        
        h.append(hsv[a][0]) 
        s.append(hsv[a][1])
        v.append(hsv[a][2])
        
        color_name=color_detectRGB(hsv[a][0],hsv[a][1],hsv[a][2])
        cv2.rectangle(new_img, (x,y), (x+rectangle_x, y+rectangle_y), color[color_name], 2) 
        a+=1
        current_state.append(color_name)
	
    cv2.imshow("Camera Feed", new_img)
	#cv2.imshow("Crop image", crop_frame[i])
    print(current_state)
    print(hsv)
        
cap = cv2.VideoCapture(0) 
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 60  

while True:
    ret, img = cap.read()
    
    upgrade_color()
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break
cap.release()
cv2.destroyAllWindows()

