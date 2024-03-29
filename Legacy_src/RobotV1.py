#!/usr/bin/env python3

# Author Elliott Tiver Flinders University Information Technology Student
import RPi.GPIO as GPIO
import time
import os
import xbox
import socket
from picamera import PiCamera
from datetime import datetime
from subprocess import call
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin Setup
# Front Motors
# output for front motor controller
GPIO.setup(23, GPIO.OUT)  # IN1
GPIO.setup(24, GPIO.OUT)  # IN2
GPIO.setup(25, GPIO.OUT)  # IN3
GPIO.setup(12, GPIO.OUT)  # IN4
# Back Motors
# output for rear motor controller
GPIO.setup(17, GPIO.OUT)  # IN1
GPIO.setup(18, GPIO.OUT)  # IN2
GPIO.setup(27, GPIO.OUT)  # IN3
GPIO.setup(22, GPIO.OUT)  # IN4

# PWM Speed Control Setup
# Pin Setup
GPIO.setup(14, GPIO.OUT)  # Front Left Motor
GPIO.setup(15, GPIO.OUT)  # Front Right Motor
GPIO.setup(0, GPIO.OUT)  # Back Left Motor
GPIO.setup(5, GPIO.OUT)  # Back Right Motor
# PWM Setup
FLM_pwm = GPIO.PWM(14, 100)
FRM_pwm = GPIO.PWM(15, 100)
BLM_pwm = GPIO.PWM(0, 100)
BRM_pwm = GPIO.PWM(5, 100)
# Start PWM instances at 0
FLM_pwm.start(0)
FRM_pwm.start(0)
BLM_pwm.start(0)
BRM_pwm.start(0)

# RBG Headlight Pin Setup
GPIO.setup(26, GPIO.OUT)  # RED
GPIO.setup(13, GPIO.OUT)  # GREEN
GPIO.setup(19, GPIO.OUT)  # BLUE

# Tail Light Pin Setup
# Left Side
GPIO.setup(10, GPIO.OUT)  # Left Brake Light
GPIO.setup(9, GPIO.OUT)  # Left Indicator
# Right Side
GPIO.setup(11, GPIO.OUT)  # Right Brake Light
GPIO.setup(6, GPIO.OUT)  # Right Indicator
# Tail Light Cluster Setup
rightbrake_pwm = GPIO.PWM(10, 100)
leftind_pwm = GPIO.PWM(9, 100)
leftbrake_pwm = GPIO.PWM(11, 100)
rightind_pwm = GPIO.PWM(6, 100)
# Start PWM instances at 0
leftbrake_pwm.start(0)
leftind_pwm.start(0)
rightbrake_pwm.start(0)
rightind_pwm.start(0)

# Camera Setup
# #camera.resolution = (640,480)
# camera.framerate = (24)
# ime.sleep(1)

# Streaming Socket Server Setup
# server_socket = socket.socket()
# server_socket.bind(('0.0.0.0', 8000))
# server_socket.listen(0)
# connection = server_socket.accept()[0].makefile('wb')

# Arduino setup Collision Avoidance System
promini = 8
LeftalrtReg = 21
LeftalrtAI = 16
RightalrtReg = 20
RightalrtAI = 1
# Pin Mode Setup
GPIO.setup(promini, GPIO.OUT)
GPIO.setup(LeftalrtReg, GPIO.IN)
GPIO.setup(LeftalrtAI, GPIO.IN)
GPIO.setup(RightalrtReg, GPIO.IN)
GPIO.setup(RightalrtAI, GPIO.IN)

    
# RGB Headlight Colours
# RGB  COLOUR FUNCTIONS/COMBINATIONS
def redLED(state):
    if (state == "ON"):
        GPIO.output(26, True)
    elif (state == "OFF"):
        GPIO.output(26, False)

        
def greenLED(state):
    if (state == "ON"):
        GPIO.output(13, True)
    elif (state == "OFF"):
        GPIO.output(13, False)

        
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

               
# Program To Cycle RGB Headlight Colours On 360 Controller D-Pad
def RGBcolorcycle(selection):
    # All Led States Account For Both The Next And Prevous Led Colour And Disables Them
    # Red Led
    if selection == 1:
        orangeLED("OFF")
        greenLED("OFF")
        redLED("ON")
    # Green Led
    elif selection == 2:
        redLED("OFF")
        blueLED("OFF")
        greenLED("ON")
    # Blue Led
    elif selection == 3:
        greenLED("OFF")
        yellowLED("OFF")
        blueLED("ON")
    # Yellow Led
    elif selection == 4:
        blueLED("OFF")
        cyanLED("OFF")
        yellowLED("ON")
    # Cyan Led
    elif selection == 5:
        yellowLED("OFF")
        magLED("OFF")
        cyanLED("ON")
    # Magenta Led
    elif selection == 6:
        cyanLED("OFF")
        whiteLED("OFF")
        magLED("ON")
    # White Led
    elif selection == 7:
        magLED("OFF")
        orangeLED("OFF")
        whiteLED("ON")
    # Orange Led
    elif selection == 8:
        whiteLED("OFF")
        redLED("OFF")
        orangeLED("ON")


# Movement And Functions
def fwd(i):
    # Front
    GPIO.output(24, True)  # F/L FWD
    GPIO.output(23, False)  # F/L REV
    GPIO.output(25, True)  # F/R FWD
    GPIO.output(12, False)  # F/R REV
    # Back
    GPIO.output(22, True)  # B/L FWD
    GPIO.output(27, False)  # B/L REV
    GPIO.output(18, True)  # B/R FWD
    GPIO.output(17, False)  # B/R REV
    time.sleep(i)

    
def rev(i):
    # Front
    GPIO.output(24, False)  # F/L FWD
    GPIO.output(23, True)  # F/L REV
    GPIO.output(25, False)  # F/R FWD
    GPIO.output(12, True)  # F/R REV
    # Back
    GPIO.output(22, False)  # B/L FWD
    GPIO.output(27, True)  # B/L REV
    GPIO.output(18, False)  # B/R FWD
    GPIO.output(17, True)  # B/R REV
    time.sleep(i)

    
def turnLEFT(i):
    # Front
    GPIO.output(25, True)  # F/R FWD
    GPIO.output(12, False)  # F/R REV
    GPIO.output(24, False)  # F/L FWD
    GPIO.output(23, False)  # F/L REV
    # Back
    GPIO.output(18, True)  # B/R FWD
    GPIO.output(17, False)  # B/R REV
    GPIO.output(22, False)  # B/L FWD
    GPIO.output(27, False)  # B/L REV
    time.sleep(i)


def pivotleft(i):
    # Front
    GPIO.output(24, False)  # F/L FWD
    GPIO.output(23, True)  # F/L REV
    GPIO.output(25, True)  # F/R FWD
    GPIO.output(12, False)  # F/R REV
    # Back
    GPIO.output(22, False)  # B/L FWD
    GPIO.output(27, True)  # B/L REV
    GPIO.output(18, True)  # B/R FWD
    GPIO.output(17, False)  # B/R REV
    time.sleep(i)

    
def turnRIGHT(i):
    # Front
    GPIO.output(24, True)  # F/L FWD
    GPIO.output(23, False)  # F/L REV
    GPIO.output(25, False)  # F/R FWD
    GPIO.output(12, False)  # F/R REV
    # Back
    GPIO.output(22, True)  # B/L FWD
    GPIO.output(27, False)  # B/L REV
    GPIO.output(18, False)  # B/R FWD
    GPIO.output(17, False)  # B/R REV
    time.sleep(i)


def pivotright(i):
    # Front
    GPIO.output(24, True)  # F/L FWD
    GPIO.output(23, False)  # F/L REV
    GPIO.output(25, False)  # F/R FWD
    GPIO.output(12, True)  # F/R REV
    # Back
    GPIO.output(22, True)  # B/L FWD
    GPIO.output(27, False)  # B/L REV
    GPIO.output(18, False)  # B/R FWD
    GPIO.output(17, True)  # B/R REV
    time.sleep(i)


def stop(i):
    # Front
    GPIO.output(24, True)  # F/L FWD
    GPIO.output(23, True)  # F/L REV
    GPIO.output(25, True)  # F/R FWD
    GPIO.output(12, True)  # F/R REV
    # Back
    GPIO.output(22, True)  # B/L FWD
    GPIO.output(27, True)  # B/L REV
    GPIO.output(18, True)  # B/R FWD
    GPIO.output(17, True)  # B/R REV
    time.sleep(i)


def skid(i):
    # Front
    GPIO.output(24, True)  # F/L FWD
    GPIO.output(23, True)  # F/L REV
    GPIO.output(25, True)  # F/R FWD
    GPIO.output(12, True)  # F/R REV
    # Back
    GPIO.output(22, True)  # B/L FWD
    GPIO.output(27, False)  # B/L REV
    GPIO.output(18, True)  # B/R FWD
    GPIO.output(17, False)  # B/R REV
    time.sleep(i)


# Front Motor Speed Control Function
def frontspeed(i):
    FLM_pwm.ChangeDutyCycle(i)
    FRM_pwm.ChangeDutyCycle(i)


# Back Motor Speed Control Function
def backspeed(i):
    BLM_pwm.ChangeDutyCycle(i)
    BRM_pwm.ChangeDutyCycle(i)


# Tail Light Cluster Functions
# Brake Lights
def leftbrake(i):
    leftbrake_pwm.ChangeDutyCycle(i)


def rightbrake(i):
    rightbrake_pwm.ChangeDutyCycle(i)


# Indicator Lights
def leftind(i):
    leftind_pwm.ChangeDutyCycle(i)


def rightind(i):
    rightind_pwm.ChangeDutyCycle(i)


# Xbox 360 controller
# Maps Movment Functions and other functions to controoller buttons
def controller():
    # Initialize controller
    joy = xbox.Joystick()
    # Rolling Burnout Control Variable
    RBMode = 0
    # Collsion Avoidance variable control
    colstate = 0
    colavd = 0
    # RGB Headlight Control Varaible
    RGB = 0
    select = 0
    # Handbreak Control Variable
    hbrake = 0
    # Camera Recording Control Variabl
    rec = 0
    # Trigger Setup
    while True:
        # Auto Refresh Value Store Varaible
        Ltrigger = joy.leftTrigger()
        Rtrigger = joy.rightTrigger()
        # Joystrick Setup
        (lx, ly) = joy.leftStick()
        (rx, ry) = joy.rightStick()
        # Info Screen
        # Control Scheme Tree
        # Close Down Safley
        if joy.Back():
            # Cleanly Close Controller Connection
            joy.close()
            # Headlights Off
            redLED("OFF")
            greenLED("OFF")
            blueLED("OFF")
			 # Tail Lights Off
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
                
            # Camera Recording Shutoff
            if rec == 1:
                camera.stop_recording()
				# Close Streaming Socket Server
                server_socket.close()
			# Power Off Pi Computation Module
            else:
                call("sudo nohup shutdown -h now", shell=True)
                # Camera Recording Activation/Deactivation
        elif joy.Start():
            if rec == 0:
                rec = 1
                time.sleep(1)
                camera.start_recording(connection, format='h264')
				# camera.start_recording()
            elif rec == 1:
                rec = 0
                camera.stop_recording()
                time.sleep(1)

		# Power On And Enable Collision Detection Sensor Managment Module
        elif joy.Y():
            if colstate == 1:
                colstate = 0
                # Turn Off Sensor Managment Module
                GPIO.output(promini, False)
                time.sleep(1)
            elif colstate == 0:
                colstate = 1
                # Turn On Sensor Managment Module
                GPIO.output(promini, True)
                time.sleep(1)
		# Prevent Collision Detected By Left Sensor
        elif GPIO.input(LeftalrtReg) == 1  and colstate == 1:
            # Tail Light setup
            leftbrake(100)
            rightbrake(0)
            leftind(100)
            rightind(100)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            rev(0.3)
		# Prevent Collision Detected By Right Sensor
        elif GPIO.input(RightalrtReg) == 1 and colstate == 1:
            # Tail Light setup
            leftbrake(0)
            rightbrake(100)
            leftind(100)
            rightind(100)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            rev(0.3)

            # Rolling Burnout Mode Toggle
       	elif joy.Guide():
            if RBMode == 0:
                RBMode = 1
                time.sleep(1)
            elif RBMode == 1:
            	RBMode = 0
            	time.sleep(1)

        # Rear Wheel Drive  Mode Handbreak Toggle
        elif joy.A():
            if hbrake == 0:
                hbrake = 1
                time.sleep(1)
            elif hbrake == 1:
                hbrake = 0
                time.sleep(1)

        # Thumbsticks
        # Left ThumbStick X-Axis Turning
        elif lx < -0.4:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(100)
            rightind(0)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            turnLEFT(0.1)
            fwd(0.01)
        elif lx > 0.4:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(100)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            turnRIGHT(0.1)
            fwd(0.01)
            
        # Right ThumbStick X-Axis Pivoting (2 Speed)
        elif rx <= -0.6 and rx >= -1.0:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(100)
            rightind(0)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            pivotleft(0.1)
        elif rx <= -0.2 and rx >= -0.6:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(50)
            rightind(0)
            # Movment Functions
            frontspeed(50)
            backspeed(50)
            pivotleft(0.1)
        elif rx >= 0.2 and rx <= 0.6:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(50)
            # Movment Functions
            frontspeed(50)
            backspeed(50)
            pivotright(0.1)
        elif rx > 0.6 and rx <= 1.0:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(100)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            pivotright(0.1)
        # Triggers
        # Accelerate Trigger 
        # 4 Speed Rear Wheel Drive Mode (HandBreak ON)
        elif hbrake == 1 and Rtrigger > 0.1 and Rtrigger <= 0.25:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(0)
            backspeed(25)
            fwd(0.1)
        elif hbrake == 1 and Rtrigger > 0.25 and Rtrigger <= 0.50:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(0)
            backspeed(50)
            fwd(0.1)
        elif hbrake == 1 and Rtrigger > 0.50 and Rtrigger <= 0.75:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(0)
            backspeed(75)
            fwd(0.1)
        elif hbrake == 1 and Rtrigger > 0.75 and Rtrigger <= 1.0:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(0)
            backspeed(100)
            fwd(0.1)
        # Rolling Burnout(4 speed)
        elif RBMode == 1 and Rtrigger > 0.1 and Rtrigger <= 0.25:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(4)
            backspeed(25)
            fwd(0.1)
        elif RBMode == 1 and Rtrigger > 0.25 and Rtrigger <= 0.50:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(4)
            backspeed(50)
            fwd(0.1)
        elif RBMode == 1 and Rtrigger > 0.50 and Rtrigger <= 0.75:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(4)
            backspeed(75)
            fwd(0.1)
        elif RBMode == 1 and Rtrigger > 0.75 and Rtrigger <= 1.0:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(4)
            backspeed(100)
            fwd(0.1)

        # All Wheel Drive 2-Speed
        elif Rtrigger > 0.1 and Rtrigger <= 0.50:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(30)
            backspeed(30)
            fwd(0.1)
        elif Rtrigger > 0.50 and Rtrigger <= 1.0:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            fwd(0.1)

        # Reverse 2-Speed
        elif Ltrigger > 0.1 and Ltrigger <= 0.50:
            # Tail Light setup
            leftbrake(50)
            rightbrake(50)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(30)
            backspeed(30)
            rev(0.1)
        elif Ltrigger > 0.50 and Ltrigger <= 1.0:
            # Tail Light setup
            leftbrake(100)
            rightbrake(100)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            rev(0.1)            
        # AI Auto Pilot Override
        elif joy.leftBumper() and colstate == 1:
            if colavd == 0:
                colavd = 1
                time.sleep(1)
                # Entrapment detect Variables
                leftcount = 0
                rightcount = 0
                while colavd == 1:
                    # Infinitely avoid collision desicison tree
                    # If entrament is detected reverse and turn 180 degres
                    if joy.leftBumper():
                        stop(0.1)
                        colavd = 0
                        time.sleep(1)
                    elif leftcount == 2:
                        # Tail Light setup
                        leftbrake(0)
                        rightbrake(0)
                        leftind(100)
                        rightind(0)
                        # Movment Functions
                       	frontspeed(100)
                        backspeed(100)
                        leftcount = 0
                        rev(0.4)
                        pivotleft(0.6)
                    elif rightcount == 2:
                        # Tail Light setup
                        leftbrake(0)
                        rightbrake(0)
                        leftind(0)
                        rightind(100)
                        # Movment Functions
                        frontspeed(100)
                        backspeed(100)
                        rightcount = 0
                        rev(0.4)
                        pivotright(0.6)
                    elif GPIO.input(RightalrtAI) == 1:
                        # Tail Light setup
                        leftbrake(0)
                        rightbrake(100)
                        leftind(100)
                        rightind(100)
                        # Movment Functions
                        frontspeed(50)
                        backspeed(50)
                        leftcount = 0
                        rightcount += 1
                        rev(0.5)
                        pivotright(0.3)
                    elif GPIO.input(LeftalrtAI) == 1:
                        # Tail Light setup
                        leftbrake(100)
                        rightbrake(0)
                        leftind(100)
                        rightind(100)
                        # Movment Functions
                        frontspeed(50)
                        backspeed(50)
                        rightcount = 0
                        leftcount += 1
                        rev(0.5)
                        pivotleft(0.3)
                    else:
                        # Tail Light setup
                        leftbrake(0)
                        rightbrake(0)
                        leftind(0)
                        rightind(0)
                        # Movment Functions
                        frontspeed(100)
                        backspeed(100)
                        fwd(0.1)

        # RGB Headlight Dpad Integration
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
       	 	# Cycle Back Through colours
            elif joy.dpadLeft():
                if select > 1:
                    select -= 1
                    RGBcolorcycle(select)
                    time.sleep(1)
                elif select == 1:
                	select = 8
                	RGBcolorcycle(select)
                	time.sleep(1)
        	# Cycle Forward Through colours
            elif joy.dpadRight():
                if select < 8:
                	select += 1
                	RGBcolorcycle(select)
                	time.sleep(1)
                elif select == 8:
                	select = 1
                	RGBcolorcycle(select)
                	time.sleep(1)
        # Default Case For No Current Input
        else:
            # Tail Light setup
            leftbrake(100)
            rightbrake(100)
            leftind(0)
            rightind(0)
            # Movment Functions
            stop(0.1)


# Main {};
controller()
