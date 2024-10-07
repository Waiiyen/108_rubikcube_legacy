import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
button_1 = 21
button_2 = 20 
button_5 = 13
button_4 = 19
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
GPIO.setup(button_1, GPIO.IN)
GPIO.setup(button_2, GPIO.IN)
GPIO.setup(button_5, GPIO.IN)
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
delay = .00001
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
while True:
	if GPIO.input(button_4) == GPIO.LOW:
		GPIO.output(buzzer,1)
		time.sleep(0.1)
		GPIO.output(buzzer,0)
		time.sleep(0.1)
	# elif GPIO.input(button_1) == GPIO.LOW:
	# 	GPIO.output(buzzer,1)
	# 	time.sleep(0.1)
	# 	GPIO.output(buzzer,0)
	# 	time.sleep(0.1)
	# 	GPIO.output(buzzer,1)
	# 	time.sleep(0.1)
	# 	GPIO.output(buzzer,0)
	# 	time.sleep(0.1)
	# if GPIO.input(button_5) == GPIO.LOW:
	# 	GPIO.output(buzzer,1)
	# 	time.sleep(0.1)
	# 	GPIO.output(buzzer,0)
	# 	time.sleep(0.1)
	# 	GPIO.output(buzzer,1)
	# 	time.sleep(0.1)
	# 	GPIO.output(buzzer,0)
	# 	time.sleep(0.1)
	# 	GPIO.output(buzzer,1)
	# 	time.sleep(0.1)
	# 	GPIO.output(buzzer,0)
	# 	time.sleep(0.1)
	# if GPIO.input(out) == GPIO.LOW:
	# 	GPIO.output(buzzer,1)
	# 	time.sleep(0.1)
	# 	GPIO.output(buzzer,0)
	# 	time.sleep(0.1)
	# 	GPIO.output(buzzer,1)
	# 	time.sleep(0.1)
	# 	GPIO.output(buzzer,0)
	# 	time.sleep(0.1)
	# 	GPIO.output(buzzer,1)
	# 	time.sleep(0.1)
	# 	GPIO.output(buzzer,0)
	# 	time.sleep(0.1)
	# 	GPIO.output(buzzer,1)
	# 	time.sleep(0.1)
	# 	GPIO.output(buzzer,0)
	# 	time.sleep(0.1) 