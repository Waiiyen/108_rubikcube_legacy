#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------
# --- Author         : Ahmet Ozlu
# --- Mail           : ahmetozlu93@gmail.com
# --- Date           : 31st December 2017 - new year eve :)
# ----------------------------------------------

from PIL import Image
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import itemfreq
from color_recognition_api import knn_classifier as knn_classifier


def color_histogram_of_test_image(test_src_image):

    # load the image
    image = test_src_image
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    chans = cv2.split(image)
    colors = ('h', 's', 'v')
    features = []
    feature_data = ''
    counter = 0
    for (chan, color) in zip(chans, colors):
        counter = counter + 1

        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        features.extend(hist)

        # find the peak pixel values for R, G, and B
        elem = np.argmax(hist)

        if counter == 1:
            blue = str(elem)
        elif counter == 2:
            green = str(elem)
        elif counter == 3:
            red = str(elem)
            feature_data = red + ',' + green + ',' + blue
            # print(feature_data)

    with open('test_hsv.data', 'w') as myfile:
        myfile.write(feature_data)


def color_histogram_of_training_image(img_name):

    # detect image color by using image file name to label training data
    if 'red' in img_name:
        data_source = 'red'
    elif 'yellow' in img_name:
        data_source = 'yellow'
    elif 'green' in img_name:
        data_source = 'green'
    elif 'orange' in img_name:
        data_source = 'orange'
    elif 'white' in img_name:
        data_source = 'white'
    elif 'blue' in img_name:
        data_source = 'blue'

    # load the image
    image = cv2.imread(img_name)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    chans = cv2.split(image)
    colors = ('h', 's', 'v')
    features = []
    feature_data = ''
    counter = 0
    for (chan, color) in zip(chans, colors):
        counter = counter + 1

        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        features.extend(hist)

        # find the peak pixel values for R, G, and B
        elem = np.argmax(hist)

        if counter == 1:
            blue = str(elem)
        elif counter == 2:
            green = str(elem)
        elif counter == 3:
            red = str(elem)
            feature_data = red + ',' + green + ',' + blue

    with open('training_hsv.data', 'a') as myfile:
        myfile.write(feature_data + ',' + data_source + '\n')


def training():

    # red color training images
    for f in os.listdir('./training_dataset/red'):
        color_histogram_of_training_image('./training_dataset/red/' + f)

    # yellow color training images
    for f in os.listdir('./training_dataset/yellow'):
        color_histogram_of_training_image('./training_dataset/yellow/' + f)

    # green color training images
    for f in os.listdir('./training_dataset/green'):
        color_histogram_of_training_image('./training_dataset/green/' + f)

    # orange color training images
    for f in os.listdir('./training_dataset/orange'):
        color_histogram_of_training_image('./training_dataset/orange/' + f)

    # white color training images
    for f in os.listdir('./training_dataset/white'):
        color_histogram_of_training_image('./training_dataset/white/' + f)

    # blue color training images
    for f in os.listdir('./training_dataset/blue'):
        color_histogram_of_training_image('./training_dataset/blue/' + f)		
