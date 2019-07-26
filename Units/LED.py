import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)

for x in range (3):
	GPIO.output(2, True)
	time.sleep(0.5)
	print "BLUE LED ON"
	#GPIO.output(2, False)
	#time.sleep(0.5)
	#print "BLUE LED OFF"
	GPIO.output(3, True)
	time.sleep(0.5)
	print "GREEN LED ON"
	#GPIO.output(3, False)
	#time.sleep(0.5)
	#print "GREEN LED OFF"
	GPIO.output(4, True)
	time.sleep(0.5)
	print "RED LED ON"
	#GPIO.output(4, False)
	#time.sleep(0.5)
	#print "RED LED OFF"
	GPIO.output(17, True)
	time.sleep(0.5)
	print "YELL0W LED ON"
	#GPIO.output(17, False)
	#time.sleep(1)
	GPIO.output(2, False)
	time.sleep(0.5)
	GPIO.output(3, False)
	time.sleep(0.5)
	GPIO.output(4, False)
	time.sleep(0.5)
	GPIO.output(17, False)
	time.sleep(0.5)
 	#print "YELLOW LED OFF"	
	
	



