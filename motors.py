#Author Elliott Tiver
#Flinders Uinvierty Information Technology Student
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Front
#output for front motor controller
GPIO.setup(23, GPIO.OUT) #IN1
GPIO.setup(24, GPIO.OUT) #IN2
GPIO.setup(25, GPIO.OUT) #IN3
GPIO.setup(8, GPIO.OUT)  #IN4
#Back
#output for rear motor controller
GPIO.setup(17, GPIO.OUT) #IN1
GPIO.setup(18, GPIO.OUT) #IN2
GPIO.setup(27, GPIO.OUT) #IN3
GPIO.setup(22, GPIO.OUT) #IN4
#IR Sensors
#output for IR sensors
GPIO.setup(8, GPIO.OUT) #VCC Sensor 1 Left side  (Power)
GPIO.setup(9, GPIO.IN) #Left sensor obstace detection (Input)
GPIO.setup(10,GPIO.OUT) #VCC sensor 2 Right side (Power)
GPIO.setup(11, GPIO.IN) #Right sensor obstace detection (Input)
#define movment functions
def fwd(i):
	#Front
	GPIO.output(24, True)  #F/L FWD
	GPIO.output(23, False) #F/L REV
	GPIO.output(25, True)  #F/R FWD
 	GPIO.output(8, False)  #F/R REV
	#Back
        GPIO.output(22, True)  #B/L FWD
	GPIO.output(27, False) #B/L REV
	GPIO.output(18, True)  #B/R FWD
	GPIO.output(17, False) #B/R REV
	time.sleep(i)
def rev(i):
	#Front
	GPIO.output(24, False) #F/L FWD
	GPIO.output(23, True)  #F/L REV
	GPIO.output(25, False) #F/R FWD
	GPIO.output(8, True)   #F/R REV
	#Back
	GPIO.output(22, False) #B/L FWD
	GPIO.output(27, True)  #B/L REV
	GPIO.output(18, False) #B/R FWD
	GPIO.output(17, True)  #B/R REV
	time.sleep(i)
def turnLEFT(i):
	#Front
	GPIO.output(25, True)  #F/R FWD
	GPIO.output(8, False)  #F/R REV
	GPIO.output(24, False) #F/L FWD
	GPIO.output(23, False) #F/L REV
 	#Back
	GPIO.output(18, True)  #B/R FWD
	GPIO.output(17, False) #B/R REV	
	GPIO.output(22, False) #B/L FWD
	GPIO.output(27, False) #B/L REV
	time.sleep(i)
def pivotleft(i):
	#Front
	GPIO.output(24, False) #F/L FWD
	GPIO.output(23, True)  #F/L REV
	GPIO.output(25, True)  #F/R FWD
	GPIO.output(8, False)  #F/R REV
	#Back
	GPIO.output(22, False) #B/L FWD
	GPIO.output(27, True)  #B/L REV
	GPIO.output(18, True)  #B/R FWD
	GPIO.output(17, False) #B/R REV
	time.sleep(i)
def turnRIGHT(i):
	#Front
	GPIO.output(24, True)  #F/L FWD
	GPIO.output(23, False) #F/L REV
	GPIO.output(25, False) #F/R FWD
	GPIO.output(8, False)  #F/R REV
	#Back
	GPIO.output(22, True)  #B/L FWD
	GPIO.output(27, False) #B/L REV
	GPIO.output(18, False) #B/R FWD
	GPIO.output(17, False) #B/R REV
	time.sleep(i)
def pivotright(i):
	#Front
	GPIO.output(24, True)  #F/L FWD
	GPIO.output(23, False) #F/L REV	
	GPIO.output(25, False) #F/R FWD
	GPIO.output(8, True)   #F/R REV
	#Back
	GPIO.output(22, True)  #B/L FWD
	GPIO.output(27, False) #B/L REV
	GPIO.output(18, False) #B/R FWD
	GPIO.output(17, True)  #B/R REV
	time.sleep(i)
def stop(i):
	#Front
    	GPIO.output(24, True) #F/L FWD
	GPIO.output(23, True) #F/L REV
	GPIO.output(25, True) #F/R FWD
	GPIO.output(8, True)  #F/R REV
	#Back
	GPIO.output(22, True) #B/L FWD
	GPIO.output(27, True) #B/L REV
	GPIO.output(18, True) #B/R FWD
	GPIO.output(17, True) #B/R REV		
	time.sleep(i)
def skid(i):
	#Front
	GPIO.output(24, True) #F/L FWD
	GPIO.output(23, True) #F/L REV
	GPIO.output(25, True) #F/R FWD
	GPIO.output(8, True)  #F/R REV
	#Back
	GPIO.output(22, True)  #B/L FWD
	GPIO.output(27, False) #B/L REV
	GPIO.output(18, True)  #B/R FWD
	GPIO.output(17, False) #B/R REV	
	time.sleep(i)

#IR based obstacle avoidence desicsion tree
def detect():
	#Go until obstace detected then reverse and turn
	while True:
		leftsensor = GPIO.input(9)
		rightsensor = GPIO.input(11)
		#if obstacle detected on left turn reverse and turn right
		if(leftsensor == False):
			print("obstacle on left")
			stop(0.5)
			rev(2)
			pivotright(2)
		#if obstacle is deteced on right reverse and turn left
		elif(rightsensor == False):
			print ("obstacle on right")
			stop(0.5)
			rev(2)
			pivotleft(2)
		#if obstacle detected on both sensors reverse and turn right
		elif(leftsensor == False and rightsensor == False):
			print("Obstacle on Left and Right sensors")
			stop(0.5)
			rev(2)
			pivotright(2)
		else:
			fwd(1)
#Xbox controller override
#def controller():
	
#Mode Select
def optionselect():
	print("Booting up...")
	print("Press 1 For Autonomus Obstacle Avoidence")
	print("Press 2 For Skids")
	print("Press 2 For Wireless Controller Mode")
	print("Press 3 To Shutdown")
	selection = input("Select Mode: ")
	if selection == 1:
		detect()
	elif selection == 2:
		skid(10)
	elif selection == 3:
		print("Shutting Down...")
		while True:
			stop(1)
	elif selection == 0:
		fwd(0.5)
		turnRIGHT(0.2)
		fwd(0.5)
		turnLEFT(0.2)
		fwd(0.5)
		GPIO.cleanup()
optionselect()



