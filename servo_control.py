import RPi.GPIO as GPIO
from time import sleep

pin1 = 19
pin2 = 26

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)

pwm1 = GPIO.PWM(pin1, 50)
pwm2 = GPIO.PWM(pin2, 50)
pwm1.start(0)
pwm2.start(0)


def rotate(pin, pwm, rotations):
	if rotations > 0:
		fill = 2.5
	else:
		fill = 12.5
	
	GPIO.output(pin, True)
	pwm.ChangeDutyCycle(fill)
	sleep(rotations * 1.1)
	GPIO.output(pin, False)
	pwm.ChangeDutyCycle(0)


def move_left(rotations):
	rotate(pin1, pwm1, rotations)


def move_right(rotations):
	rotate(pin2, pwm2, rotations)
	

def truncate_pwm():
	pwm1.stop()
	pwm2.stop()
	GPIO.cleanup()


move_left(0.5)
sleep(5)
move_right(0.5)
sleep(5)
move_left(0.5)
truncate_pwm()
