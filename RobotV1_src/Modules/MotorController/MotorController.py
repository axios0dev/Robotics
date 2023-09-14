#!/usr/bin/env python3
# This module contains the controller code for the drive chain,
# motors that move the AxiosRoboticsRCv1 unit.
import RPi.GPIO as GPIO
from time import sleep
from Modules.LedSubsystem import TailLightController 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Front motor controller pin config.
# Front left motor.
FrontLeftMtrForwardPin = 24
FrontLeftMtrReversePin = 23
FrontLeftMtrSpeedControlPin = 14
GPIO.setup(FrontLeftMtrReversePin, GPIO.OUT)  # IN1
GPIO.setup(FrontLeftMtrForwardPin, GPIO.OUT)  # IN2
GPIO.setup(FrontLeftMtrSpeedControlPin, GPIO.OUT)
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
RearLeftMtrForwardPin = 27
RearLeftMtrReversePin = 22
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


# Front motor speed control function, 
# speed >= 0 && <= 100.
def FrontMtrSpeed(speed):
    FrontLeftMtrPWM.ChangeDutyCycle(speed)
    FrontRightMtrPWM.ChangeDutyCycle(speed)


# Back motor speed control function.
# speed >= 0 && <= 100
def RearMtrSpeed(speed):
    RearLeftMtrPWM.ChangeDutyCycle(speed)
    RearRightMtrPWM.ChangeDutyCycle(speed)


# Movement functions.
def DriveForward(speed, duration):
    # Speed controls.
    FrontMtrSpeed(speed)
    RearMtrSpeed(speed)
    # Motor controls.
    # Front motors.
    GPIO.output(FrontLeftMtrForwardPin, True)
    GPIO.output(FrontLeftMtrReversePin, False)
    GPIO.output(FrontRightMtrForwardPin, True)
    GPIO.output(FrontRightMtrReversePin, False)
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, True)
    GPIO.output(RearLeftMtrReversePin, False)
    GPIO.output(RearRightMtrForwardPin, True)
    GPIO.output(RearRightMtrReversePin, False)
    sleep(duration)
    # Pin state clean up.
    StopMotors()

    
def DriveBackwards(speed, duration):
    # Tail light controls.
    TailLightController.LeftBrakeLightOn(speed)
    TailLightController.RightBrakeLightOn(speed)
    # Speed controls.
    FrontMtrSpeed(speed)
    RearMtrSpeed(speed)
    # Motor controls.
    # Front motors.
    GPIO.output(FrontLeftMtrForwardPin, False)
    GPIO.output(FrontLeftMtrReversePin, True)  
    GPIO.output(FrontRightMtrForwardPin, False)  
    GPIO.output(FrontRightMtrReversePin, True)  
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, False)  
    GPIO.output(RearLeftMtrReversePin, True)
    GPIO.output(RearRightMtrForwardPin, False)  
    GPIO.output(RearRightMtrReversePin, True)  
    sleep(duration)
    # Pin state clean up.
    StopMotors()
    TailLightController.BrakeLightsOff()

    
def TurnLeft(speed, duration):
    # Tail light controls.
    TailLightController.LeftIndicatorOn(100)
    # Speed controls.
    FrontMtrSpeed(speed)
    RearMtrSpeed(speed)
    # Motor controls.
    # Front motors.
    GPIO.output(FrontLeftMtrForwardPin, False)  
    GPIO.output(FrontLeftMtrReversePin, False)
    GPIO.output(FrontRightMtrForwardPin, True)
    GPIO.output(FrontRightMtrReversePin, False)  
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, False)
    GPIO.output(RearLeftMtrReversePin, False)  
    GPIO.output(RearRightMtrForwardPin, True)
    GPIO.output(RearRightMtrReversePin, False)
    sleep(duration)
    # Pin state clean up.
    StopMotors()
    TailLightController.IndicatorLightsOff("LEFT")

    
def PivotLeft(speed, duration):
    # Tail light controls.
    TailLightController.LeftIndicatorOn(speed)
    # Speed controls.
    FrontMtrSpeed(speed)
    RearMtrSpeed(speed)
    # Motor controls.
    # Front motors.
    GPIO.output(FrontLeftMtrForwardPin, False)  
    GPIO.output(FrontLeftMtrReversePin, True)  
    GPIO.output(FrontRightMtrForwardPin, True)  
    GPIO.output(FrontRightMtrReversePin, False)  
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, False)  
    GPIO.output(RearLeftMtrReversePin, True)  
    GPIO.output(RearRightMtrForwardPin, True)  
    GPIO.output(RearRightMtrReversePin, False)  
    sleep(duration)
    # Pin state clean up.
    StopMotors()
    TailLightController.IndicatorLightsOff("LEFT")


def TurnRight(speed, duration):
    # Tail light controls.
    TailLightController.RightIndicatorOn(100)
    # Speed controls.
    FrontMtrSpeed(speed)
    RearMtrSpeed(speed)
    # Motor controls.
    # Front motors.
    GPIO.output(FrontLeftMtrForwardPin, True)
    GPIO.output(FrontLeftMtrReversePin, False)  
    GPIO.output(FrontRightMtrForwardPin, False)  
    GPIO.output(FrontRightMtrReversePin, False)  
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, True)  
    GPIO.output(RearLeftMtrReversePin, False)  
    GPIO.output(RearRightMtrForwardPin, False)  
    GPIO.output(RearRightMtrReversePin, False)  
    sleep(duration)
    # Pin state clean up.
    StopMotors()
    TailLightController.IndicatorLightsOff("RIGHT")


def PivotRight(speed, duration):
    # Tail light controls.
    TailLightController.RightIndicatorOn(speed)
    # Speed controls.
    FrontMtrSpeed(speed)
    RearMtrSpeed(speed)
    # Motor controls.
    # Front motors.
    GPIO.output(FrontLeftMtrForwardPin, True)  
    GPIO.output(FrontLeftMtrReversePin, False)  
    GPIO.output(FrontRightMtrForwardPin, False)
    GPIO.output(FrontRightMtrReversePin, True)  
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, True)  
    GPIO.output(RearLeftMtrReversePin, False)  
    GPIO.output(RearRightMtrForwardPin, False)
    GPIO.output(RearRightMtrReversePin, True)
    sleep(duration)
    # Pin state clean up.
    StopMotors()
    TailLightController.IndicatorLightsOff("RIGHT")


def StopMotors():
    # Front motors.
    GPIO.output(FrontLeftMtrForwardPin, False)
    GPIO.output(FrontLeftMtrReversePin, False)  
    GPIO.output(FrontRightMtrForwardPin, False)  
    GPIO.output(FrontRightMtrReversePin, False)  
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, False)  
    GPIO.output(RearLeftMtrReversePin, False)  
    GPIO.output(RearRightMtrForwardPin, False)  
    GPIO.output(RearRightMtrReversePin, False)


def Burnout(speed, duration):
    # Tail light controls.
    TailLightController.LeftIndicatorOn(100)
    TailLightController.RightIndicatorOn(100)
    # Speed controls.
    FrontMtrSpeed(speed)
    RearMtrSpeed(speed)
    # Motor controls.
    # Front motors.
    GPIO.output(FrontLeftMtrForwardPin, True)
    GPIO.output(FrontLeftMtrReversePin, True)  
    GPIO.output(FrontRightMtrForwardPin, True)  
    GPIO.output(FrontRightMtrReversePin, True)
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, True)  
    GPIO.output(RearLeftMtrReversePin, False)  
    GPIO.output(RearRightMtrForwardPin, True)  
    GPIO.output(RearRightMtrReversePin, False)  
    sleep(duration)
    # Pin state clean up.
    StopMotors()
    TailLightController.IndicatorLightsOff()
