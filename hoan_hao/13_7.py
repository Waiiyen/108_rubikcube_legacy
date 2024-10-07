import cv2
import numpy
import os
import os.path
import sys
from color_recognition_api import color_histogram_feature_extraction
from color_recognition_api import knn_classifier
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
# i = 0
# r = 0
# g = 0
# b = 0
# o = 0
# w = 0
# y = 0
# cre = r"C:\Users\ASUS\Desktop\test_ras\howgud"
trace = [
    [184,214,185,265], #0
    [183,214,300,390], #1
    [181,209,420,510], #2
    [225,270,150,250], #3
    [210,267,300,400], #4
    [215,265,425,545], #5
    [290,380,95,230],  #6
    [280,370,270,420], #7
    [280,360,460,610]] #8
PATH = r'C:\Users\ASUS\Desktop\test_ras\training.data'
prediction = 'n.a.'
if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    print ('training data is ready, classifier is loading...')
else:
    print ('training data is being created...')
    open('training.data', 'w')
    color_histogram_feature_extraction.training()
    print ('training data is ready, classifier is loading...')
for i in range (100,102):
    source_image = cv2.imread(r'C:\Users\ASUS\Desktop\test_ras\hehe_test\img{}.png'.format(i))
    current_state = []
    for t in range(9):  
        # cv2.imshow("{}_{}".format(i,t),source_image[trace[t][0]:trace[t][1],trace[t][2]:trace[t][3]])
        color_histogram_feature_extraction.color_histogram_of_test_image(source_image[trace[t][0]:trace[t][1],trace[t][2]:trace[t][3]])
        prediction = knn_classifier.main('training.data','test.data')
        current_state.append(prediction)
    print(current_state)
        
    #     if prediction == "red" :
    #         cv2.rectangle(source_image,(trace[t][2],trace[t][0]),(trace[t][3],trace[t][1]),(0,0,255),-1)
    #     elif prediction == "orange" :
    #         cv2.rectangle(source_image,(trace[t][2],trace[t][0]),(trace[t][3],trace[t][1]),(51,153,255),-1)
    #     elif prediction == "yellow" :
    #         cv2.rectangle(source_image,(trace[t][2],trace[t][0]),(trace[t][3],trace[t][1]),(51,255,255),-1)
    #     elif prediction == "green":
    #         cv2.rectangle(source_image,(trace[t][2],trace[t][0]),(trace[t][3],trace[t][1]),(0,255,0),-1)
    #     elif prediction == "blue":
    #         cv2.rectangle(source_image,(trace[t][2],trace[t][0]),(trace[t][3],trace[t][1]),(255,0,0),-1)
    #     elif prediction == "white":
    #         cv2.rectangle(source_image,(trace[t][2],trace[t][0]),(trace[t][3],trace[t][1]),(255,255,255),-1)
    # cv2.imwrite(r"C:\Users\ASUS\Desktop\test_ras\answer\ans{}.png".format(i),source_image)
    cv2.waitKey(0)
                