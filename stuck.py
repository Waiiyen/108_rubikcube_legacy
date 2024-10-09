import time
import RPi.GPIO as GPIO
from signal import pause
import cv2
import threading 
import numpy as np 
import keyboard
import random
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

