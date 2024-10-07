from time import sleep
import RPi.GPIO as GPIO
from signal import pause
GPIO.setwarnings(False)
buzzer = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.output(buzzer,1)
sleep(1)
GPIO.output(buzzer,0)
sleep(1)
GPIO.output(buzzer,1)
sleep(1)
GPIO.output(buzzer,0)
sleep(1)
GPIO.output(buzzer,1)
sleep(1)
GPIO.output(buzzer,0)
sleep(1)
GPIO.output(buzzer,1)
sleep(1)
GPIO.output(buzzer,0)
sleep(1)
