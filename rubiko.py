from time import sleep
import RPi.GPIO as GPIO
from signal import pause
GPIO.setwarnings(False)
ENA_F = 14
STEP_F = 15
DIR_F = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_F,GPIO.OUT)
GPIO.setup(STEP_F,GPIO.OUT)
GPIO.setup(ENA_F,GPIO.OUT)
GPIO.output(ENA_F, 1)
GPIO.output(DIR_F, 1) #o la di len 

delay = .0002

GPIO.output(ENA_F, 0)
for t in range(10100):
	GPIO.output(STEP_F,1)
	sleep(delay)
	GPIO.output(STEP_F,0)
	sleep(delay)
GPIO.output(ENA_F, 1)
