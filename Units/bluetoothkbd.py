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

#Bluetooth Keyboard Script
def keypad():
	import curses
	#Curses setup for keyboard input
	screen = curses.initscr()
	curses.noecho()
	curses.halfdelay(5)
	#curses.cbreak()
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
			break
		elif char == ord('k'):
			screen.addstr(3,0,'Skids!!')
			skid(0.01)
		elif char == ord('j'):
			screen.addstr(3,0,'Right\n')
			turnRIGHT(0.01)
		elif char == ord('l'):
			screen.addstr(3,0,'Left\n')
			turnLEFT(0.01)
		elif char == ord('w'):
			screen.addstr(3,0,'Forward\n')
			fwd(0.01)		
		elif char == ord('s'):
			screen.addstr(3,0,'Reverse\n')
			rev(0.01)
		elif char == ord('a'):
			screen.addstr(3,0,'Left Pivot\n')
			pivotleft(0.01)
		elif char == ord('d'):
			screen.addstr(3,0,'Right Pivot\n')
			pivotright(0.01)
		elif char == curses.ERR:
			screen.addstr(3,0,'Idle\n')
			stop(0.01)
keypad()
