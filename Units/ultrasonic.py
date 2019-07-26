#Ultrasonic distance sensor testing code
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#pin setup 
TRIG = 2
ECHO = 3
GPIO.setup(TRIG, GPIO.OUT) #Trig
GPIO.setup(ECHO, GPIO.IN) #Echo
GPIO.output(TRIG, False)
time.sleep(0.1)
print("Sensor Initialising...")
GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)
print("Measuring Distance..")
while GPIO.input(3) == 0:
	start = time.time()
	pass
while GPIO.input(3) == 1:
	stop = time.time()
	pass

duration = (stop - start)
distance = duration * 17150
roundeddist = round(distance, 2)
print "Distance:", roundeddist, "CM"

