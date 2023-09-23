#!/usr/bin/env python3
# This module contains the controller code for the drive chain,
# motors that move the AxiosRoboticsRCv1 unit.
import RPi.GPIO as GPIO
from time import sleep
from typing import Final
from Modules.LedSubsystem import TaillightController 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Front motor controller pin config.
# Front left motor.
#FRONTLEFTMTRFORWARDPIN = 24
FRONTLEFTMTRFORWARDPIN: Final[int] = 24
FrontLeftMtrReversePin = 23
FrontLeftMtrSpeedControlPin = 14
GPIO.setup(FrontLeftMtrReversePin, GPIO.OUT)  # IN1
GPIO.setup(FRONTLEFTMTRFORWARDPIN, GPIO.OUT)  # IN2
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

# Full brightness definition.
FullBrightness = 100


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
    
    TaillightController.BrakeLightsOff()
    TaillightController.IndicatorLightsOff()
    
    # Speed controls.
    FrontMtrSpeed(speed)
    RearMtrSpeed(speed)
    # Motor controls.
    # Front motors.
    GPIO.output(FRONTLEFTMTRFORWARDPIN, True)
    GPIO.output(FrontLeftMtrReversePin, False)
    GPIO.output(FrontRightMtrForwardPin, True)
    GPIO.output(FrontRightMtrReversePin, False)
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, True)
    GPIO.output(RearLeftMtrReversePin, False)
    GPIO.output(RearRightMtrForwardPin, True)
    GPIO.output(RearRightMtrReversePin, False)
    sleep(duration)

    
def DriveBackwards(speed, duration):
    
    TaillightController.IndicatorLightsOff()
    
    # Tail light controls.
    TaillightController.BrakeLightsOn(speed)
    # Speed controls.
    FrontMtrSpeed(speed)
    RearMtrSpeed(speed)
    # Motor controls.
    # Front motors.
    GPIO.output(FRONTLEFTMTRFORWARDPIN, False)
    GPIO.output(FrontLeftMtrReversePin, True)  
    GPIO.output(FrontRightMtrForwardPin, False)  
    GPIO.output(FrontRightMtrReversePin, True)  
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, False)  
    GPIO.output(RearLeftMtrReversePin, True)
    GPIO.output(RearRightMtrForwardPin, False)  
    GPIO.output(RearRightMtrReversePin, True)  
    sleep(duration)

    
def TurnLeft(speed, duration):
    
    TaillightController.BrakeLightsOff()
    TaillightController.IndicatorLightsOff("RIGHT")
    
    # Tail light controls.
    TaillightController.IndicatorLightsOn(FullBrightness, "LEFT")
    # Speed controls.
    FrontMtrSpeed(speed)
    RearMtrSpeed(speed)
    # Motor controls.
    # Front motors.
    GPIO.output(FRONTLEFTMTRFORWARDPIN, False)  
    GPIO.output(FrontLeftMtrReversePin, False)
    GPIO.output(FrontRightMtrForwardPin, True)
    GPIO.output(FrontRightMtrReversePin, False)  
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, False)
    GPIO.output(RearLeftMtrReversePin, False)  
    GPIO.output(RearRightMtrForwardPin, True)
    GPIO.output(RearRightMtrReversePin, False)
    sleep(duration)

    
def PivotLeft(speed, duration):
    
    TaillightController.BrakeLightsOff()
    TaillightController.IndicatorLightsOff("RIGHT")
    
    # Tail light controls.
    TaillightController.IndicatorLightsOn(speed, "LEFT")
    # Speed controls.
    FrontMtrSpeed(speed)
    RearMtrSpeed(speed)
    # Motor controls.
    # Front motors.
    GPIO.output(FRONTLEFTMTRFORWARDPIN, False)  
    GPIO.output(FrontLeftMtrReversePin, True)  
    GPIO.output(FrontRightMtrForwardPin, True)  
    GPIO.output(FrontRightMtrReversePin, False)  
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, False)  
    GPIO.output(RearLeftMtrReversePin, True)  
    GPIO.output(RearRightMtrForwardPin, True)  
    GPIO.output(RearRightMtrReversePin, False)  
    sleep(duration)


def TurnRight(speed, duration):
    
    TaillightController.BrakeLightsOff()
    TaillightController.IndicatorLightsOff("LEFT")
    
    # Tail light controls.
    TaillightController.IndicatorLightsOn(FullBrightness, "RIGHT")
    # Speed controls.
    FrontMtrSpeed(speed)
    RearMtrSpeed(speed)
    # Motor controls.
    # Front motors.
    GPIO.output(FRONTLEFTMTRFORWARDPIN, True)
    GPIO.output(FrontLeftMtrReversePin, False)  
    GPIO.output(FrontRightMtrForwardPin, False)  
    GPIO.output(FrontRightMtrReversePin, False)  
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, True)  
    GPIO.output(RearLeftMtrReversePin, False)  
    GPIO.output(RearRightMtrForwardPin, False)  
    GPIO.output(RearRightMtrReversePin, False)  
    sleep(duration)


def PivotRight(speed, duration):
    
    TaillightController.BrakeLightsOff()
    TaillightController.IndicatorLightsOff("LEFT")
    
    # Tail light controls.
    TaillightController.IndicatorLightsOn(speed, "RIGHT")
    # Speed controls.
    FrontMtrSpeed(speed)
    RearMtrSpeed(speed)
    # Motor controls.
    # Front motors.
    GPIO.output(FRONTLEFTMTRFORWARDPIN, True)  
    GPIO.output(FrontLeftMtrReversePin, False)  
    GPIO.output(FrontRightMtrForwardPin, False)
    GPIO.output(FrontRightMtrReversePin, True)  
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, True)  
    GPIO.output(RearLeftMtrReversePin, False)  
    GPIO.output(RearRightMtrForwardPin, False)
    GPIO.output(RearRightMtrReversePin, True)
    sleep(duration)


def StopMotors():
    
    TaillightController.IndicatorLightsOff()
    
    # Turn on brake lights.
    TaillightController.BrakeLightsOn(FullBrightness)
    # Front motors.
    GPIO.output(FRONTLEFTMTRFORWARDPIN, True)
    GPIO.output(FrontLeftMtrReversePin, True)  
    GPIO.output(FrontRightMtrForwardPin, True)  
    GPIO.output(FrontRightMtrReversePin, True)  
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, True)  
    GPIO.output(RearLeftMtrReversePin, True)  
    GPIO.output(RearRightMtrForwardPin, True)  
    GPIO.output(RearRightMtrReversePin, True)
    # Pin state clean up.
    #TaillightController.BrakeLightsOff()
    


def Burnout(speed,duration):
    
    TaillightController.BrakeLightsOff()
    
    # Tail light controls.
    TaillightController.IndicatorLightsOn(FullBrightness)
    # Speed controls.
    FrontMtrSpeed(0)
    RearMtrSpeed(speed)
    # Motor controls.
    # Front motors.
    GPIO.output(FRONTLEFTMTRFORWARDPIN, True)
    GPIO.output(FrontLeftMtrReversePin, True)  
    GPIO.output(FrontRightMtrForwardPin, True)  
    GPIO.output(FrontRightMtrReversePin, True)
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, True)  
    GPIO.output(RearLeftMtrReversePin, False)  
    GPIO.output(RearRightMtrForwardPin, True)  
    GPIO.output(RearRightMtrReversePin, False)  
    sleep(duration)
    
    
def RollingBurnout(frontspeed, rearspeed, duration):
    TaillightController.BrakeLightsOff()
    # Tail light controls.
    TaillightController.IndicatorLightsOn(FullBrightness)
    # Speed controls.
    FrontMtrSpeed(frontspeed)
    RearMtrSpeed(rearspeed)
    # Motor controls.
    # Front motors.
    GPIO.output(FRONTLEFTMTRFORWARDPIN, True)
    GPIO.output(FrontLeftMtrReversePin, False)  
    GPIO.output(FrontRightMtrForwardPin, True)  
    GPIO.output(FrontRightMtrReversePin, False)
    # Rear motors.
    GPIO.output(RearLeftMtrForwardPin, True)  
    GPIO.output(RearLeftMtrReversePin, False)  
    GPIO.output(RearRightMtrForwardPin, True)  
    GPIO.output(RearRightMtrReversePin, False)  
    sleep(duration)
