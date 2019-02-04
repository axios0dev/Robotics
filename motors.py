#Author Elliott Tiver
#Flinders Univiersty Information Technology Student
import RPi.GPIO as GPIO
import time
import curses
import os
import xbox
from picamera import PiCamera
from datetime import datetime
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Pin Setup
#Front Motors
#output for front motor controller
GPIO.setup(23, GPIO.OUT) #IN1
GPIO.setup(24, GPIO.OUT) #IN2
GPIO.setup(25, GPIO.OUT) #IN3
GPIO.setup(12, GPIO.OUT) #IN4
#Back Motors
#output for rear motor controller
GPIO.setup(17, GPIO.OUT) #IN1
GPIO.setup(18, GPIO.OUT) #IN2
GPIO.setup(27, GPIO.OUT) #IN3
GPIO.setup(22, GPIO.OUT) #IN4

#Left Ultrasonic Sensor
LTRIG = 20
LECHO = 21 
GPIO.setup(LTRIG, GPIO.OUT)
GPIO.setup(LECHO, GPIO.IN)
GPIO.output(LTRIG, False) #Disable Transmitter
#Right Ultrasonic sensor
RTRIG = 2
RECHO = 3
GPIO.setup(RTRIG, GPIO.OUT)
GPIO.setup(RECHO, GPIO.IN)
GPIO.output(RTRIG, False)

#PWM Speed Control Setup
#Pin Setup
GPIO.setup(14, GPIO.OUT) #Front Left Motor
GPIO.setup(15, GPIO.OUT) #Front Right Motor
GPIO.setup(0, GPIO.OUT)  #Back Left Motor
GPIO.setup(5, GPIO.OUT)  #Back Right Motor
#PWM Setup
FLM_pwm = GPIO.PWM(14,100)
FRM_pwm = GPIO.PWM(15,100)
BLM_pwm = GPIO.PWM(0,100)
BRM_pwm = GPIO.PWM(5,100)
#Start PWM instances at 0
FLM_pwm.start(0)
FRM_pwm.start(0)
BLM_pwm.start(0)
BRM_pwm.start(0)

#RBG Headlight Pin Setup
GPIO.setup(26,GPIO.OUT) #RED
GPIO.setup(13,GPIO.OUT) #GREEN
GPIO.setup(19,GPIO.OUT) #BLUE

#Camera Setup
camera = PiCamera()
camera.resolution = (1280,720)
camera.framerate = (25)
time.sleep(1)

#RGB Headlight Colours
#RGB  COLOUR FUNCTIONS/COMBINATIONS
def redLED(state):
	if (state == "ON"):
		GPIO.output(26, True)
	elif (state == "OFF"):
		GPIO.output(26, False)
def greenLED(state):
	if (state == "ON"):
		GPIO.output(13, True)
	elif (state == "OFF"):
		GPIO.output(13,False)
def blueLED(state):
	if (state == "ON"):
		GPIO.output(19, True)
	elif (state == "OFF"):
		GPIO.output(19, False)
def yellowLED(state):
	if (state == "ON"):
		redLED("ON")
		greenLED("ON")
	elif (state == "OFF"):
		redLED("OFF")
		greenLED("OFF")
def cyanLED(state):
	if (state == "ON"):
		greenLED("ON")
		blueLED("ON")
	elif (state == "OFF"):
		greenLED("OFF")
		blueLED("OFF")
def magLED(state):
	if (state == "ON"):
		redLED("ON")
		blueLED("ON")
	elif (state == "OFF"):
        	redLED("OFF")
                blueLED("OFF")
def whiteLED(state):
	if (state == "ON"):
		redLED("ON")
                blueLED("ON")
		greenLED("ON")
	elif (state == "OFF"):
                redLED("OFF")
                blueLED("OFF")
		greenLED("OFF")
def orangeLED(state):
	if (state == "ON"):
                redLED("ON")
                yellowLED("ON")
        elif (state == "OFF"):
                redLED("OFF")
                yellowLED("OFF")

#Program To Cycle RGB Headlight Colours On 360 Controller D-Pad
def RGBcolorcycle(selection):
	if selection == 1:
		orangeLED("OFF")
		greenLED("OFF")
		redLED("ON")
	elif selection == 2:
		redLED("OFF")
		blueLED("OFF")
		greenLED("ON")
	elif selection == 3:
		greenLED("OFF")
		yellowLED("OFF")
		blueLED("ON")
	elif selection == 4:
		blueLED("OFF")
		cyanLED("OFF")
		yellowLED("ON")
	elif selection == 5:
		yellowLED("OFF")
		magLED("OFF")
		cyanLED("ON")
	elif selection == 6:
		cyanLED("OFF")
		whiteLED("OFF")
		magLED("ON")
	elif selection == 7:
		magLED("OFF")
		orangeLED("OFF")
		whiteLED("ON")
	elif selection == 8:
		whiteLED("OFF")
		redLED("OFF")
		orangeLED("ON")

#Movment And Functions
def fwd(i):
	#Front
	GPIO.output(24, True)  #F/L FWD
	GPIO.output(23, False) #F/L REV
	GPIO.output(25, True)  #F/R FWD
 	GPIO.output(12, False)  #F/R REV
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
	GPIO.output(12, True)   #F/R REV
	#Back
	GPIO.output(22, False) #B/L FWD
	GPIO.output(27, True)  #B/L REV
	GPIO.output(18, False) #B/R FWD
	GPIO.output(17, True)  #B/R REV
	time.sleep(i)
def turnLEFT(i):
	#Front
	GPIO.output(25, True)  #F/R FWD
	GPIO.output(12, False)  #F/R REV
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
	GPIO.output(12, False)  #F/R REV
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
	GPIO.output(12, False)  #F/R REV
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
	GPIO.output(12, True)   #F/R REV
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
	GPIO.output(12, True)  #F/R REV
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
	GPIO.output(12, True)  #F/R REV
	#Back
	GPIO.output(22, True)  #B/L FWD
	GPIO.output(27, False) #B/L REV
	GPIO.output(18, True)  #B/R FWD
	GPIO.output(17, False) #B/R REV	
	time.sleep(i)

#Front Motor Speed Control Function
def frontspeed(i):
	FLM_pwm.ChangeDutyCycle(i)
	FRM_pwm.ChangeDutyCycle(i)
#Back Motor Speed Control Function
def backspeed(i):
	BLM_pwm.ChangeDutyCycle(i)
	BRM_pwm.ChangeDutyCycle(i)

#Ultrasonic Collision Avoidance Measuring Distance
def leftcollisiondetect():
	#Send and recvice pulse
	GPIO.output(LTRIG, True)
	time.sleep(0.00001)
	GPIO.output(LTRIG, False)
	#convert input to a centimere distance
	while GPIO.input(LECHO) == 0:
		pass
	start = time.time()
	while GPIO.input(LECHO) == 1:
		pass
	stop = time.time()
	duration = stop - start
	distance = duration * 17150
	rdist = round(distance, 2)
	return rdist

def rightcollisiondetect():
	#Send recive pulse
	GPIO.output(RTRIG, True)
	time.sleep(0.00001)
	GPIO.output(RTRIG, False)
	#convert and return data
	while GPIO.input(RECHO) == 0:
		pass
	start = time.time()
	while GPIO.input(RECHO) == 1:
		pass
	stop = time.time()
	duration = stop - start
	distance = duration * 17150
	rdist = round(distance, 2)
	return rdist

def autodetectAI():
	 #Entrapment detect Variables
         leftcount = 0
         rightcount = 0
         obsdist = 25
	 while True:
         	Ldetectdistance = leftcollisiondetect()
         	Rdetectdistance = rightcollisiondetect()
         	#Infinitely avoid collision desicison tree
         	#If entrament is detected reverse and turn 180 degress
         	if leftcount  == 2:
                	leftcount = 0
                        rev(0.2)
                       	pivotleft(0.6)
           	elif rightcount == 2:
                        rightcount = 0
                        rev(0.2)
                        pivotright(0.6)
            	elif Rdetectdistance <= obsdist:
                        leftcount = 0
                        rightcount += 1
                        rev(0.2)
                        pivotright(0.3)
          	elif Ldetectdistance <= obsdist:
                       	rightcount = 0
                        leftcount += 1
                        rev(0.2)
                       	pivotleft(0.3)
           	else:
                       	fwd(0.1)	
#Arrow Pad Control of Robot
#First RC Function Test
def keypad():
	#Curses setup for keyboard input
	screen = curses.initscr()
	curses.noecho()
	#curses.cbreak()
	#screen.nodelay(1)
	curses.halfdelay(5)
	screen.keypad(True)
	#Collision detection control variable
	collisionstate = 'ON'
	#Option Read Out
	screen.addstr("Use The Arrow Keys To Control Robot\n")
	screen.addstr("To Quit Current Mode Press Q\n")
	screen.addstr("To Enable Collision Detection And Avoidance Press E, To Disable Press D\n")
	#screen.addstr("Collision Avoidance State: ", collisionstate\n)
	screen.addstr("Current Command: ")
	while True:
		#Default avoidance distance
		offsetavoidance = 25
		char = screen.getch()
		#Ultrasonic colission avoidance implementation
		leftcollisionavoidance = leftcollisiondetect()
		rightcolavd = rightcollisiondetect()
		#control structure
		if leftcollisionavoidance <= offsetavoidance and rightcolavd <= offsetavoidance and collisionstate == 'ON':
			screen.addstr(3,0, '>> Avoiding Collision!!')
			stop(0.1)
			rev(0.2)
		elif char == ord('e') and collisionstate == 'OFF':
			screen.addstr(4,0, '>> Collision Avoidance Enabled')
			collisionstate = 'ON'
		elif char == ord('e') and collisionstate == 'ON':
			screen.addstr(4,0, '>> Warning Collision Avoidance Disabled')
			collisionstate = 'OFF'	
		#return to main menu 
		elif char == ord('q'):
			curses.nocbreak(); screen.keypad(False); curses.echo() 
			curses.endwin()
			os.system('clear')
			optionselect()
			break
		#Keyboard keybinds
		elif char == curses.KEY_UP:
			#offsetadvoidance = 15
			screen.addstr(3,0,'>> Skids!!')
			skid(0.01)
		elif char == curses.KEY_RIGHT:
			screen.addstr(3,0,'>> Right\n')
			turnRIGHT(0.01)
		elif char == curses.KEY_LEFT:
			screen.addstr(3,0,'>> Left\n')
			turnLEFT(0.01)
		elif char == ord('w'):
			screen.addstr(3,0,'>> Forward\n')
			fwd(0.01)
		elif char == ord('s'):
			screen.addstr(3,0,'>> Reverse\n')
			rev(0.01)
		elif char == ord('a'):
			screen.addstr(3,0,'>> Left Pivot\n')
			pivotleft(0.01)
		elif char == ord('d'):
			screen.addstr(3,0,'>> Right Pivot\n')
			pivotright(0.01)
		elif char == curses.ERR:
			screen.addstr(3,0,'>> Idle\n')
			stop(0.01)
		#elif char == ord('w') and offsetavoidance == 15:
			#offsetavoidance = 45
			#screen.addstr(3,0,'>> Changing Distance Value To HighSpeed Calibration\n')
		
#testing 	
def detectmenu():
	print("Auto Roam With Collision Detection Enabled")
	print("Press 1 To Roam Autonomusly")
	print("Press 2 To Stop")
	print("Press 3 To Return To Main Menu")
	USRINPT = input("Select Mode: ")
	if USRINPT == 1:
		print("Collision Detection Log: ")
		detect()
	elif USRINPT == 2:
		stop(1)
		detectmenu()
	elif USRINPT == 3:
		os.system('clear')
		optionselect()

#Xbox 360 controller 
#Maps Movment Functions and other functions to controoller buttons
def controller():
	#Initialize controller
	joy = xbox.Joystick()
	#Collision Avoidance
        collisionrange = 15
        colstate = 0
	#Rolling Burnout Control Variable
	RBMode = 0
	#Collsion Avoidance variable control
	colavd = 0
	#RGB Headlight Control Varaible
	RGB = 0
	select = 0
	#Handbreak Control Variable
	hbrake = 0
	#Camera Recording Control Variabl
	rec = 0

	#Trigger Setup 
	while True:
	#Auto Refresh Value Store Varaibles
		Lcollisiondist = leftcollisiondetect()
		Rcollisiondist = rightcollisiondetect()
		Ltrigger = joy.leftTrigger() 
		Rtrigger = joy.rightTrigger()
	#Joystrick Setup
		(lx,ly) = joy.leftStick()
		(rx,ry) = joy.rightStick()
	#Info Screen
		#print("Xbox 360 Controller Active")
		#Control Scheme Tree
		#Close Down Safley
                if joy.Back():
                        joy.close()
			#camera.stop_recording()
			redLED("OFF")
                       	greenLED("OFF")
                        blueLED("OFF")
			optionselect()
		#Camera Recording Activation/Deactivation
		elif joy.Start():
			if rec == 0:
				rec = 1
				time.sleep(1)
				print("Camera Active")
				moment = datetime.now()
				camera.start_recording('/home/pi/Videos/RobotVision_%02d_%02d_%02d.h264' % (moment.hour, moment.minute, moment.second))
			elif rec == 1:
				rec = 0
				print("Camera Disabled")
				camera.stop_recording()
				time.sleep(1)
		#Collision Detection Features
		elif joy.Y():
                        if colstate == 1:
                                colstate = 0
                                print("Collision Avoidance System Offline")
                                time.sleep(1)
                        elif colstate == 0:
                                colstate = 1
                                print("Collision Avoidance System Online")
                                time.sleep(1)
		elif Lcollisiondist < collisionrange and colstate == 1:
			frontspeed(100)
			backspeed(100)
			rev(0.2)
		elif Rcollisiondist < collisionrange and colstate == 1:
			frontspeed(100)
			backspeed(100)
			rev(0.2)
		#Rolling Burnout Mode
		elif joy.Guide():
			if RBMode == 0:
				RBMode = 1
				print("Rolling Burnout Mode Engaged")
				time.sleep(1)
			elif RBMode == 1:
				RBMode = 0
				print("Rolling Burnout Mode Disabled")
				time.sleep(1)
		#Left ThumbStick X-Axis Turning
		elif lx < -0.4:
			frontspeed(100)
			backspeed(100)
			turnLEFT(0.1)
			fwd(0.01)
		elif lx > 0.4:
			frontspeed(100)
			backspeed(100)
			turnRIGHT(0.1)
			fwd(0.01)
		#Right ThumbStick X-Axis Pivoting (2 Speed)
		elif rx <= -0.6 and rx >= -1.0:
			frontspeed(100)
			backspeed(100)
			pivotleft(0.1)
		elif rx <= -0.2 and rx >= -0.6:
			frontspeed(50)
			backspeed(50)
			pivotleft(0.1)
		elif rx >= 0.2 and rx <= 0.6:
			frontspeed(50)
			backspeed(50)
			pivotright(0.1)
		elif rx > 0.6 and rx <= 1.0:
			frontspeed(100)
			backspeed(100)
			pivotright(0.1)
		#Skid Mode Handbreak Enable/Disable 
		elif joy.A():
			if hbrake == 0:
				hbrake = 1
				print("HandBreak ON")
				time.sleep(1)
			elif hbrake == 1:
				hbrake = 0
				print("Handbreak OFF")
				time.sleep(1)
		#4 Speed Skid Mode (HandBreak ON)
		elif Rtrigger > 0 and Rtrigger <= 0.25 and hbrake == 1:
			frontspeed(0)
			backspeed(25)
			fwd(0.1)
		elif Rtrigger > 0.25 and Rtrigger <= 0.50 and hbrake == 1:
                        frontspeed(0)
                        backspeed(50)
                        fwd(0.1)
		elif Rtrigger > 0.50 and Rtrigger <= 0.75 and hbrake == 1:
                        frontspeed(0)
                        backspeed(75)
                        fwd(0.1)
		elif Rtrigger > 0.75 and Rtrigger <= 1.0 and hbrake == 1:
                        frontspeed(0)
                        backspeed(100)
                        fwd(0.1)
		#Reverse Trigger (2 Speed)
		elif Ltrigger > 0 and Ltrigger <= 0.50:
			frontspeed(30)
			backspeed(30)
                        rev(0.1)
		elif Ltrigger > 0.50 and Ltrigger <= 1.0:
			frontspeed(100)
			backspeed(100)
			rev(0.1)
		#Accelerate Trigger (2 Speed Setup)-  non Rolling Burnout
		elif Rtrigger > 0 and Rtrigger <= 0.50 and RBMode == 0:
			frontspeed(30)
			backspeed(30)
			fwd(0.1)
		elif Rtrigger > 0.50 and Rtrigger <= 1.0 and RBMode == 0:
			frontspeed(100)
			backspeed(100)
			fwd(0.1)
		#Accelerate Trigger Rolling Burnout
		elif Rtrigger > 0 and Rtrigger <= 0.50 and RBMode == 1:
                        frontspeed(5)
                        backspeed(50)
                        fwd(0.1)
                elif Rtrigger > 0.50 and Rtrigger <= 1.0 and RBMode == 1:
                        frontspeed(5)
                        backspeed(100)
                        fwd(0.1)
		elif joy.leftBumper():
			if colavd == 0:
				colavd = 1
				time.sleep(1)
				#Entrapment detect Variables
         			leftcount = 0
         			rightcount = 0
         			obsdist = 25
         			while colavd == 1:
                			Ldetectdistance = leftcollisiondetect()
                			Rdetectdistance = rightcollisiondetect()
                			#Infinitely avoid collision desicison tree
                			#If entrament is detected reverse and turn 180 degress
					if joy.leftBumper():
						stop(0.1)
						colavd = 0
						time.sleep(1)
                			elif leftcount  == 2:
						frontspeed(100)
						backspeed(100)
                        			leftcount = 0
                        			rev(0.2)
                        			pivotleft(0.6)
                			elif rightcount == 2:
						frontspeed(100)
						backspeed(100)
                        			rightcount = 0
                        			rev(0.2)
                        			pivotright(0.6)
                			elif Rdetectdistance <= obsdist:
						frontspeed(50)
						backspeed(50)
                        			leftcount = 0
                        			rightcount += 1
                        			rev(0.2)
                        			pivotright(0.3)
                			elif Ldetectdistance <= obsdist:
						frontspeed(50)
						backspeed(50)
                        			rightcount = 0
                        			leftcount += 1
                        			rev(0.2)
                        			pivotleft(0.3)
                			else:
						frontspeed(100)
						backspeed(100)
                        			fwd(0.1)
	 
                #RGB Headlight Dpad Integration
		elif joy.dpadUp():
			if RGB == 0:
				RGB = 1
				select = 1
				RGBcolorcycle(select)
				time.sleep(1)
			elif RGB == 1:
				RGB = 0
				redLED("OFF")
				greenLED("OFF")
				blueLED("OFF")
				time.sleep(1)
		#Cycle Back Through colours
		elif joy.dpadLeft():
			if select > 1:
				select -= 1
				RGBcolorcycle(select)
				time.sleep(1)
			elif select == 1:
				select = 8
				RGBcolorcycle(select)
				time.sleep(1)
		#Cycle Through colours
		elif joy.dpadRight():
			if select < 8:
				select += 1
				RGBcolorcycle(select)
				time.sleep(1)
			elif select == 8:
				select = 1
				RGBcolorcycle(select)
				time.sleep(1)			
		#Default Case For No Current Input
		else:
			stop(0.1)
#Main Mode Select Menu
def optionselect():
	print("Robotic Rover Option Menu Selection")
	print("Press 1 For Autonomus Obstacle Avoidence")
	print("Press 2 For Skids")
	print("Press 3 For Keyboard Control Mode")
	print("Press 4 For Wireless Controller Mode")
	print("Press 5 For Remote Motor Shutdown")
	selection = input("Select Mode: ")
	#Collision Avoidence Demo
	if selection == 1:
		#Entrapment detect Variables
		leftcount = 0
		rightcount = 0
		obsdist = 30
		while True:
			Ldetectdistance = leftcollisiondetect()
			Rdetectdistance = rightcollisiondetect()
			print("Avoiding Collision...")
			print "Left Sensor Distance:", Ldetectdistance, "CM"
			print "Right Sensor Distance:", Rdetectdistance, "CM"
			print "leftcount  :", leftcount
			print "rightcount : ", rightcount
			#os.system('clear')
			#Infinitely avoid collision desicison tree
			#If entrament is detected reverse and turn 180 degress 
			if leftcount  == 3:
				leftcount = 0
                                rev(0.2)
                                pivotright(0.6)
                        elif rightcount == 3:
				rightcount = 0
                                rev(0.2)
                                pivotleft(0.6)
                        elif Rdetectdistance <= obsdist:
                                leftcount = 0
                                rightcount += 1
                                rev(0.2)
                                pivotright(0.3)
                        elif Ldetectdistance <= obsdist:
                                rightcount = 0
                                leftcount += 1
                                rev(0.2)
                                pivotleft(0.3)			
			else:
                                fwd(0.1)

	#Skid Only Mode
	elif selection == 2:
		print("Rear Wheel Drive Inclusive Enabled")
		skid(10)
	#Remote Engine Power Cut Signal
	elif selection == 5:
		print("Cutting Power To All Motors...")
		stop(1)
		os.system('clear')
		optionselect()
	#Keypad Control Mode
	elif selection == 3:
		print("Control Robot With Arrow Pad And A,S,D")
		keypad()
	#Debug test
	elif selection == 0:
		pivotright(0.6)
		stop(0.1)
	#Xbox 360 Controller Mode
	elif selection == 4:
		controller()

#Main {};
optionselect()



