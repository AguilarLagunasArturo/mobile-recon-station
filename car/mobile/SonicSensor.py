import RPi.GPIO as GPIO
from time import sleep, time

GPIO.setmode(GPIO.BOARD)

TRIG = 36
ECHO = 37

GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG, 0)

GPIO.setup(ECHO, GPIO.IN)

sleep(0.1)
GPIO.output(TRIG, 1)
sleep(0.00001)
GPIO.output(TRIG, 0)


while GPIO.input(ECHO) == 0:
	pass
start = time()

while GPIO.input(ECHO) == 1:
	pass
stop = time()

d = (start - stop) * 17000
