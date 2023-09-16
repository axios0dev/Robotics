#Author Elliott Tiver
#Flinders Univiersty Information Technology Student
import RPi.GPIO as GPIO
import time
import curses
import os
#import xbox
import socket
from picamera import PiCamera
from datetime import datetime
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Tail Light PinSetup
#Left Side
GPIO.setup(10, GPIO.OUT) #Left Brake Light
GPIO.setup(9, GPIO.OUT) #Left Indicator
#Right Side
GPIO.setup(11, GPIO.OUT) #Right Brake Light
GPIO.setup(6, GPIO.OUT) #Right Indicator

#PWM Setup
LB_pwm = GPIO.PWM(10,100)
LI_pwm = GPIO.PWM(9,100)
RB_pwm = GPIO.PWM(11,100)
RI_pwm = GPIO.PWM(6,100)
#Start PWM instances at 0
LB_pwm.start(0)
LI_pwm.start(0)
RB_pwm.start(0)
RI_pwm.start(0)

#Tail Light Brightness
def tlb(i):
	LB_pwm.ChangeDutyCycle(i)
	RB_pwm.ChangeDutyCycle(i)
#Tail Light State
#def stoplights(state, i):
	

#Indicator Brightness
def ilb(i):
	LI_pwm.ChangeDutyCycle(i)
	RI_pwm.ChangeDutyCycle(i)
#Indicator State
def leftindicator(state):
	if (state == "ON"):
		GPIO.output(9, True) 
	elif (state == "OFF"):
		GPIO.output(9, False)
def rightindicator(state):
	if (state == "ON"):
	       	GPIO.output(6, True) 
	elif (state == "OFF"):
		GPIO.output(6, False)        

tlb(30)
ilb(0)
time.sleep(2)
tlb(0)
ilb(30)
time.sleep(2)
#taillights("OFF")
#leftindicator("ON")
#rightindicator("ON")
#taillights("ON")
#time.sleep(2)
#leftindicator("OFF")
#rightindicator("OFF")
#time.sleep(2)
#taillights("OFF")
#leftindicator("ON")
#rightindicator("ON")



#tlb(100)
#ilb(100)
#leftindicator("ON")
#rightindicator("ON")
#taillights("ON")
#time.sleep(3)
#leftindicator("OFF")
#rightindicator("OFF")
#taillights("OFF")
#time.sleep(1)













