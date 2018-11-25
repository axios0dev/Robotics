#Author Elliott Tiver
#Flinders Uinvierty Information Technology Student
import RPi.GPIO as GPIO
import time
import curses
import os
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Front
#output for front motor controller
GPIO.setup(23, GPIO.OUT) #IN1
GPIO.setup(24, GPIO.OUT) #IN2
GPIO.setup(25, GPIO.OUT) #IN3
GPIO.setup(12, GPIO.OUT) #IN4
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
#Arrow Pad Control Of Robot
#First RC Function Test
def keypad():
	import curses
	#Curses setup for keyboard input
	screen = curses.initscr()
	curses.noecho()
	#curses.cbreak()
	#screen.nodelay(1)
	curses.halfdelay(5)
	screen.keypad(True)
	#Option Read Out
	screen.addstr("Use The Arrow Keys To Control Robot\n")
	screen.addstr("To Quit Current Mode Press Q\n")
	screen.addstr("Current Command: ")
	while True:
		char = screen.getch()
		#return to main menu 
		if char == ord('q'):
			curses.nocbreak(); screen.keypad(False); curses.echo() 
			curses.endwin()
			os.system('clear')
			optionselect()
			break
		elif char == ord('k'):
			screen.addstr(3,0,'Skids!!')
			skid(0.01)
		elif char == ord('d'):
			screen.addstr(3,0,'Right\n')
			turnRIGHT(0.01)
		elif char == ord('a'):
			screen.addstr(3,0,'Left\n')
			turnLEFT(0.01)
		elif char == ord('w'):
			screen.addstr(3,0,'Forward\n')
			fwd(0.01)
		elif char == ord('s'):
			screen.addstr(3,0,'Reverse\n')
			rev(0.01)
		elif char == ord('j'):
			screen.addstr(3,0,'Left Pivot\n')
			pivotleft(0.01)
		elif char == ord('l'):
			screen.addstr(3,0,'Right Pivot\n')
			pivotright(0.01)
		elif char == curses.ERR:
			screen.addstr(3,0,'Idle\n')
			stop(0.01)
#IR based obstacle avoidence desicsion tree
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

def detect():
	#Go until obstace detected then reverse and turn
	while True:
		leftsensor = GPIO.input(9)
		rightsensor = GPIO.input(11)
		#if obstacle detected on left turn reverse and turn right

		if(leftsensor == False):
			print("obstacle on left")
			stop(0.5)
			rev(0.5)
			pivotright(0.3)
		#if obstacle is deteced on right reverse and turn left
		elif(rightsensor == False):
			print ("obstacle on right")
			stop(0.5)
			rev(0.5)
			pivotleft(0.3)
		#if obstacle detected on both sensors reverse and turn right
		elif(leftsensor == False and rightsensor == False):
			print("Obstacle on Left and Right sensors")
			stop(0.5)
			rev(0.5)
			pivotright(0.3)
		else:
			fwd(0.5)
	
#Xbox controller override
#def controller():
	

#Mode Select Menu
def optionselect():
	print("Robotic Rover Option Menu Selection")
	print("Press 1 For Autonomus Obstacle Avoidence")
	print("Press 2 For Skids")
	print("Press 3 For Keyboard Control Mode")
	print("Press 4 For Wireless Controller Mode")
	print("Press 5 For Remote Motor Shutdown")
	selection = input("Select Mode: ")
	if selection == 1:
		detectmenu()
	elif selection == 2:
		print("Rear Wheel Drive Inclusive Enabled")
		skid(10)
	elif selection == 5:
		print("Cutting Power To All Motors...")
		stop(1)
		os.system('clear')
		optionselect()
	elif selection == 3:
		print("Control Robot With Arrow Pad And A,S,D")
		keypad()
	elif selection == 0:
		fwd(0.5)
		turnRIGHT(0.2)
		fwd(0.5)
		turnLEFT(0.2)
		fwd(0.5)
		GPIO.cleanup()

#Main {};
optionselect()



