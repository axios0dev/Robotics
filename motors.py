#Author Elliott Tiver
#Flinders Uinvierty Information Technology Student
import RPi.GPIO as GPIO
import time
import curses
import os
import xbox
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
        collisionrange = 25
        colstate = 1
	#Rolling Burnout Control Variable
	RBMode = 0
	#Trigger Setup 
	while True:
		Lcollisiondist = leftcollisiondetect()
		Rcollisiondist = rightcollisiondetect()
		Ltrigger = joy.leftTrigger() 
		Rtrigger = joy.rightTrigger()
	#Joystrick Setup
		(lx,ly) = joy.leftStick()
		(rx,ry) = joy.rightStick()
	#Info Screen
		#print("Xbox 360 Controll Active")
		#Control Scheme Tree
		 #Close Down Safley
                if joy.Back():
                        joy.close()
                        optionselect()
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
		elif joy.leftBumper():
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
		#Skid 
		elif joy.A():
			frontspeed(0)
			backspeed(100)
			skid(0.1)
		#Reverse Trigger (2 Speed)
		elif Ltrigger > 0 and Ltrigger <= 0.50:
			frontspeed(50)
			backspeed(50)
                        rev(0.1)
		elif Ltrigger > 0.50 and Ltrigger <= 1.0:
			frontspeed(100)
			backspeed(100)
			rev(0.1)
		#Accelerate Trigger (2 Speed Setup)-  non Rolling Burnout
		elif Rtrigger > 0 and Rtrigger <= 0.50 and RBMode == 0:
			frontspeed(50)
			backspeed(50)
			fwd(0.1)
		elif Rtrigger > 0.50 and Rtrigger <= 1.0 and RBMode == 0:
			frontspeed(100)
			backspeed(100)
			fwd(0.1)
		#Accelerate Trigger Rolling Burnout
		elif Rtrigger > 0 and Rtrigger <= 0.50 and RBMode == 1:
                        frontspeed(15)
                        backspeed(50)
                        fwd(0.1)
                elif Rtrigger > 0.50 and Rtrigger <= 1.0 and RBMode == 1:
                        frontspeed(15)
                        backspeed(100)
                        fwd(0.1)

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
			os.system('clear')
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



