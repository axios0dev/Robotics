#!/usr/bin/env python3

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# Front motor controller pin config.
# Front left motor.
FrontLeftMtrForwardPin = 24
FrontLeftMtrReversePin = 23
FrontLeftMtrSpeedControlPin = 14
GPIO.setup(FrontLeftMtrReversePin, GPIO.OUT)  # IN1
GPIO.setup(FrontLeftMtrForwardPin, GPIO.OUT)  # IN2
GPIO.setup(FrontLeftMotorActivatePin, GPIO.OUT)
# PWM pin config at 100Hz.
FrontLeftMtrPWM = GPIO.PWM(FrontLeftMtrSpeedControlPin, 100)
FrontLeftMtrPWM.start(0)
# Front right motor.
FrontRightMtrForwardPin = 25
FrontRightMtrReversePin = 12
FrontRightMtrSpeedControlPin = 15
GPIO.setup(FrontRightMtrForwardPin, GPIO.OUT)  # IN3
GPIO.setup(FrontRightMtrReversePin, GPIO.OUT)  # IN4
GPIO.setup(FrontRightMtrSpeedControlPin, GPIO.OUT)
# PWM pin config at 100Hz.
FrontRightMtrPWM = GPIO.PWM(FrontRightMtrSpeedControlPin, 100)
FrontRightMtrPWM.start(0)

# Rear motor controller pin config.
# Rear left motor.
RearLeftMtrForwardPin = 22
RearLeftMtrReversePin = 27
RearLeftMtrSpeedControlPin = 0
GPIO.setup(RearLeftMtrReversePin, GPIO.OUT)  # IN3
GPIO.setup(RearLeftMtrForwardPin, GPIO.OUT)  # IN4
GPIO.setup(RearLeftMtrSpeedControlPin, GPIO.OUT)
# PWM pin config at 100Hz.
RearLeftMtrPWM = GPIO.PWM(RearLeftMtrSpeedControlPin, 100)
RearLeftMtrPWM.start(0)
# Rear right motor.
RearRightMtrForwardPin = 18
RearRightMtrReversePin = 17
RearRightMtrSpeedControlPin = 5
GPIO.setup(RearRightMtrReversePin, GPIO.OUT)  # IN1
GPIO.setup(RearRightMtrForwardPin, GPIO.OUT)  # IN2
GPIO.setup(RearRightMtrSpeedControlPin, GPIO.OUT)
# PWM pin config at 100Hz.
RearRightMtrPWM = GPIO.PWM(RearRightMtrSpeedControlPin, 100)
RearRightMtrPWM.start(0)

# Movement functions
def fwd(speed, duration):
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
