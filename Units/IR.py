#Author Elliott Tiver
#IR module test code
#written on PI 3 B
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
GPIO.setup(23, GPIO.IN)


while True:
	leftsensor = GPIO.input(18)
	if leftsensor == 0:
		print("Left Sensor Detected")
		sleep(0.1)
	rightsensor = GPIO.input(23)
	if rightsensor == 0:
		print("Right Sensor Detected")
		sleep(0.1)


