import RPi.GPIO as GPIO
from time import sleep, time

class UltrasonicSensor:
	def __init__(self, trig=36, echo=37):
		GPIO.setmode(GPIO.BOARD)
		self.TRIG = trig
		self.ECHO = echo

		GPIO.setup(self.TRIG, GPIO.OUT)
		GPIO.output(self.TRIG, 0)

		GPIO.setup(self.ECHO, GPIO.IN)

	def getDistance(self):
		sleep(0.1)
		GPIO.output(self.TRIG, 1)
		sleep(0.00001)
		GPIO.output(self.TRIG, 0)

		while GPIO.input(self.ECHO) == 0:
			pass
		start = time()

		while GPIO.input(self.ECHO) == 1:
			pass
		stop = time()

		return (stop - start) * 17000
