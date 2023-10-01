#!/usr/bin/env python3
# This module contains the controller code for the motors that move
# the AxiosRoboticsRCv1 unit.

# Python library imports.
import RPi.GPIO as GPIO
from time import sleep
# AxiosRoboticsRCv1 unit modules.
from Modules.ConstLib import CommonConstants
from Modules.ConstLib import PinConstants
from Modules.LEDSubsystem import TaillightController 

# GPIO pin configuration.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Front left motor.
GPIO.setup(PinConstants.FRONTLEFTMOTORREVERSEPIN, GPIO.OUT)  # IN1
GPIO.setup(PinConstants.FRONTLEFTMOTORFORWARDPIN, GPIO.OUT)  # IN2
GPIO.setup(PinConstants.FRONTLEFTMOTORSPEEDCONTROLPIN, GPIO.OUT)
# PWM pin configuration at 100Hz.
FrontLeftMtrPWM = GPIO.PWM(PinConstants.FRONTLEFTMOTORSPEEDCONTROLPIN, CommonConstants.PWM_FREQUENCY)
FrontLeftMtrPWM.start(CommonConstants.PWM_NO_DUTY)
# Front right motor.
GPIO.setup(PinConstants.FRONTRIGHTMOTORFORWARDPIN, GPIO.OUT)  # IN3
GPIO.setup(PinConstants.FRONTRIGHTMOTORREVERSEPIN, GPIO.OUT)  # IN4
GPIO.setup(PinConstants.FRONTRIGHTMOTORSPEEDCONTROLPIN, GPIO.OUT)
# PWM pin configuration at 100Hz.
FrontRightMtrPWM = GPIO.PWM(PinConstants.FRONTRIGHTMOTORSPEEDCONTROLPIN, CommonConstants.PWM_FREQUENCY)
FrontRightMtrPWM.start(CommonConstants.PWM_NO_DUTY)

# Rear motor controller pin configuration.
# Rear left motor.
GPIO.setup(PinConstants.REARLEFTMOTORREVERSEPIN, GPIO.OUT)  # IN3
GPIO.setup(PinConstants.REARLEFTMOTORFORWARDPIN, GPIO.OUT)  # IN4
GPIO.setup(PinConstants.REARLEFTMOTORSPEEDCONTROLPIN, GPIO.OUT)
# PWM pin configuration at 100Hz.
RearLeftMtrPWM = GPIO.PWM(PinConstants.REARLEFTMOTORSPEEDCONTROLPIN, CommonConstants.PWM_FREQUENCY)
RearLeftMtrPWM.start(CommonConstants.PWM_NO_DUTY)
# Rear right motor.
GPIO.setup(PinConstants.REARRIGHTMOTORREVERSEPIN, GPIO.OUT)  # IN1
GPIO.setup(PinConstants.REARRIGHTMOTORFORWARDPIN, GPIO.OUT)  # IN2
GPIO.setup(PinConstants.REARRIGHTMOTORSPEEDCONTROLPIN, GPIO.OUT)
# PWM pin configuration at 100Hz.
RearRightMtrPWM = GPIO.PWM(PinConstants.REARRIGHTMOTORSPEEDCONTROLPIN, CommonConstants.PWM_FREQUENCY)
RearRightMtrPWM.start(CommonConstants.PWM_NO_DUTY)


# Front motor speed control function.
def FrontMtrSpeed(RequestedSpeed):
    FrontLeftMtrPWM.ChangeDutyCycle(RequestedSpeed)
    FrontRightMtrPWM.ChangeDutyCycle(RequestedSpeed)


# Back motor speed control function.
def RearMtrSpeed(RequestedSpeed):
    RearLeftMtrPWM.ChangeDutyCycle(RequestedSpeed)
    RearRightMtrPWM.ChangeDutyCycle(RequestedSpeed)


# Movement functions.
# Drive the unit forward.
def DriveForward(RequestedSpeed, Duration):
    # Ensure the tail light clusters are reset from previous action.
    TaillightController.BrakeLightsOff()
    TaillightController.IndicatorLightsOff()   
    # Speed controls.
    FrontMtrSpeed(RequestedSpeed)
    RearMtrSpeed(RequestedSpeed)
    
    # Motor controls.
    # Front motors.
    GPIO.output(PinConstants.FRONTLEFTMOTORFORWARDPIN, True)
    GPIO.output(PinConstants.FRONTLEFTMOTORREVERSEPIN, False)
    GPIO.output(PinConstants.FRONTRIGHTMOTORFORWARDPIN, True)
    GPIO.output(PinConstants.FRONTRIGHTMOTORREVERSEPIN, False)
    # Rear motors.
    GPIO.output(PinConstants.REARLEFTMOTORFORWARDPIN, True)
    GPIO.output(PinConstants.REARLEFTMOTORREVERSEPIN, False)
    GPIO.output(PinConstants.REARRIGHTMOTORFORWARDPIN, True)
    GPIO.output(PinConstants.REARRIGHTMOTORREVERSEPIN, False)
    sleep(Duration)


# Drive the unit backward.  
def DriveBackwards(RequestedSpeed, Duration):
    # Ensure the tail light clusters are reset from previous action.
    TaillightController.IndicatorLightsOff()
    # Tail light controls.
    TaillightController.BrakeLightsOn(RequestedSpeed)
    # Speed controls.
    FrontMtrSpeed(RequestedSpeed)
    RearMtrSpeed(RequestedSpeed)
    
    # Motor controls.
    # Front motors.
    GPIO.output(PinConstants.FRONTLEFTMOTORFORWARDPIN, False)
    GPIO.output(PinConstants.FRONTLEFTMOTORREVERSEPIN, True)  
    GPIO.output(PinConstants.FRONTRIGHTMOTORFORWARDPIN, False)  
    GPIO.output(PinConstants.FRONTRIGHTMOTORREVERSEPIN, True)  
    # Rear motors.
    GPIO.output(PinConstants.REARLEFTMOTORFORWARDPIN, False)  
    GPIO.output(PinConstants.REARLEFTMOTORREVERSEPIN, True)
    GPIO.output(PinConstants.REARRIGHTMOTORFORWARDPIN, False)  
    GPIO.output(PinConstants.REARRIGHTMOTORREVERSEPIN, True)  
    sleep(Duration)


# Turn the unit left.    
def TurnLeft(RequestedSpeed, Duration):
    # Ensure the tail light clusters are reset from previous action.
    TaillightController.BrakeLightsOff()
    TaillightController.IndicatorLightsOff(CommonConstants.RIGHT_SIDE)
    # Tail light controls.
    TaillightController.IndicatorLightsOn(CommonConstants.FULL_BRIGHTNESS, CommonConstants.LEFT_SIDE)
    # Speed controls.
    FrontMtrSpeed(RequestedSpeed)
    RearMtrSpeed(RequestedSpeed)
    
    # Motor controls.
    # Front motors.
    GPIO.output(PinConstants.FRONTLEFTMOTORFORWARDPIN, False)  
    GPIO.output(PinConstants.FRONTLEFTMOTORREVERSEPIN, False)
    GPIO.output(PinConstants.FRONTRIGHTMOTORFORWARDPIN, True)
    GPIO.output(PinConstants.FRONTRIGHTMOTORREVERSEPIN, False)  
    # Rear motors.
    GPIO.output(PinConstants.REARLEFTMOTORFORWARDPIN, False)
    GPIO.output(PinConstants.REARLEFTMOTORREVERSEPIN, False)  
    GPIO.output(PinConstants.REARRIGHTMOTORFORWARDPIN, True)
    GPIO.output(PinConstants.REARRIGHTMOTORREVERSEPIN, False)
    sleep(Duration)


# Pivot the unit left turning on the spot.    
def PivotLeft(RequestedSpeed, Duration):
    # Ensure the tail light clusters are reset from previous action.
    TaillightController.BrakeLightsOff()
    TaillightController.IndicatorLightsOff(CommonConstants.RIGHT_SIDE)
    # Tail light controls.
    TaillightController.IndicatorLightsOn(RequestedSpeed, CommonConstants.LEFT_SIDE)
    # Speed controls.
    FrontMtrSpeed(RequestedSpeed)
    RearMtrSpeed(RequestedSpeed)
    
    # Motor controls.
    # Front motors.
    GPIO.output(PinConstants.FRONTLEFTMOTORFORWARDPIN, False)  
    GPIO.output(PinConstants.FRONTLEFTMOTORREVERSEPIN, True)  
    GPIO.output(PinConstants.FRONTRIGHTMOTORFORWARDPIN, True)  
    GPIO.output(PinConstants.FRONTRIGHTMOTORREVERSEPIN, False)  
    # Rear motors.
    GPIO.output(PinConstants.REARLEFTMOTORFORWARDPIN, False)  
    GPIO.output(PinConstants.REARLEFTMOTORREVERSEPIN, True)  
    GPIO.output(PinConstants.REARRIGHTMOTORFORWARDPIN, True)  
    GPIO.output(PinConstants.REARRIGHTMOTORREVERSEPIN, False)  
    sleep(Duration)


# Turn the unit right.
def TurnRight(RequestedSpeed, Duration):
    # Ensure the tail light clusters are reset from previous action.
    TaillightController.BrakeLightsOff()
    TaillightController.IndicatorLightsOff(CommonConstants.LEFT_SIDE)
    # Tail light controls.
    TaillightController.IndicatorLightsOn(CommonConstants.FULL_BRIGHTNESS, CommonConstants.RIGHT_SIDE)
    # Speed controls.
    FrontMtrSpeed(RequestedSpeed)
    RearMtrSpeed(RequestedSpeed)
    
    # Motor controls.
    # Front motors.
    GPIO.output(PinConstants.FRONTLEFTMOTORFORWARDPIN, True)
    GPIO.output(PinConstants.FRONTLEFTMOTORREVERSEPIN, False)  
    GPIO.output(PinConstants.FRONTRIGHTMOTORFORWARDPIN, False)  
    GPIO.output(PinConstants.FRONTRIGHTMOTORREVERSEPIN, False)  
    # Rear motors.
    GPIO.output(PinConstants.REARLEFTMOTORFORWARDPIN, True)  
    GPIO.output(PinConstants.REARLEFTMOTORREVERSEPIN, False)  
    GPIO.output(PinConstants.REARRIGHTMOTORFORWARDPIN, False)  
    GPIO.output(PinConstants.REARRIGHTMOTORREVERSEPIN, False)  
    sleep(Duration)


# Pivot the unit right turning on the spot.   
def PivotRight(RequestedSpeed, Duration):
    # Ensure the tail light clusters are reset from previous action.
    TaillightController.BrakeLightsOff()
    TaillightController.IndicatorLightsOff(CommonConstants.LEFT_SIDE)
    # Tail light controls.
    TaillightController.IndicatorLightsOn(RequestedSpeed, CommonConstants.RIGHT_SIDE)
    # Speed controls.
    FrontMtrSpeed(RequestedSpeed)
    RearMtrSpeed(RequestedSpeed)
    
    # Motor controls.
    # Front motors.
    GPIO.output(PinConstants.FRONTLEFTMOTORFORWARDPIN, True)  
    GPIO.output(PinConstants.FRONTLEFTMOTORREVERSEPIN, False)  
    GPIO.output(PinConstants.FRONTRIGHTMOTORFORWARDPIN, False)
    GPIO.output(PinConstants.FRONTRIGHTMOTORREVERSEPIN, True)  
    # Rear motors.
    GPIO.output(PinConstants.REARLEFTMOTORFORWARDPIN, True)  
    GPIO.output(PinConstants.REARLEFTMOTORREVERSEPIN, False)  
    GPIO.output(PinConstants.REARRIGHTMOTORFORWARDPIN, False)
    GPIO.output(PinConstants.REARRIGHTMOTORREVERSEPIN, True)
    sleep(Duration)


# Halt all motors.
def StopMotors():
    # Ensure the tail light clusters are reset from previous action.
    TaillightController.IndicatorLightsOff()
    # Turn on brake lights.
    TaillightController.BrakeLightsOn(CommonConstants.FULL_BRIGHTNESS)
    # Front motors.
    GPIO.output(PinConstants.FRONTLEFTMOTORFORWARDPIN, True)
    GPIO.output(PinConstants.FRONTLEFTMOTORREVERSEPIN, True)  
    GPIO.output(PinConstants.FRONTRIGHTMOTORFORWARDPIN, True)  
    GPIO.output(PinConstants.FRONTRIGHTMOTORREVERSEPIN, True)  
    # Rear motors.
    GPIO.output(PinConstants.REARLEFTMOTORFORWARDPIN, True)  
    GPIO.output(PinConstants.REARLEFTMOTORREVERSEPIN, True)  
    GPIO.output(PinConstants.REARRIGHTMOTORFORWARDPIN, True)  
    GPIO.output(PinConstants.REARRIGHTMOTORREVERSEPIN, True)


# This mode contains the functionality for the rear wheel drive burnout 
# mode.
def Burnout(RequestedSpeed, Duration):
    # Ensure the tail light clusters are reset from previous action.
    TaillightController.BrakeLightsOff()
    # Tail light controls.
    TaillightController.IndicatorLightsOn(CommonConstants.FULL_BRIGHTNESS)
    # Speed controls.
    FrontMtrSpeed(CommonConstants.PWM_NO_DUTY)
    RearMtrSpeed(RequestedSpeed)
    
    # Motor controls.
    # Front motors.
    GPIO.output(PinConstants.FRONTLEFTMOTORFORWARDPIN, True)
    GPIO.output(PinConstants.FRONTLEFTMOTORREVERSEPIN, True)  
    GPIO.output(PinConstants.FRONTRIGHTMOTORFORWARDPIN, True)  
    GPIO.output(PinConstants.FRONTRIGHTMOTORREVERSEPIN, True)
    # Rear motors.
    GPIO.output(PinConstants.REARLEFTMOTORFORWARDPIN, True)  
    GPIO.output(PinConstants.REARLEFTMOTORREVERSEPIN, False)  
    GPIO.output(PinConstants.REARRIGHTMOTORFORWARDPIN, True)  
    GPIO.output(PinConstants.REARRIGHTMOTORREVERSEPIN, False)  
    sleep(Duration)

    
# This function contains the functionality for the all wheel drive 
# rolling burnout mode.    
def RollingBurnout(FrontRequestedSpeed, RearRequestedSpeed, Duration):
    # Ensure the tail light clusters are reset from previous action.
    TaillightController.BrakeLightsOff()
    # Tail light controls.
    TaillightController.IndicatorLightsOn(CommonConstants.FULL_BRIGHTNESS)
    # Speed controls.
    FrontMtrSpeed(FrontRequestedSpeed)
    RearMtrSpeed(RearRequestedSpeed)
    
    # Motor controls.
    # Front motors.
    GPIO.output(PinConstants.FRONTLEFTMOTORFORWARDPIN, True)
    GPIO.output(PinConstants.FRONTLEFTMOTORREVERSEPIN, False)  
    GPIO.output(PinConstants.FRONTRIGHTMOTORFORWARDPIN, True)  
    GPIO.output(PinConstants.FRONTRIGHTMOTORREVERSEPIN, False)
    # Rear motors.
    GPIO.output(PinConstants.REARLEFTMOTORFORWARDPIN, True)  
    GPIO.output(PinConstants.REARLEFTMOTORREVERSEPIN, False)  
    GPIO.output(PinConstants.REARRIGHTMOTORFORWARDPIN, True)  
    GPIO.output(PinConstants.REARRIGHTMOTORREVERSEPIN, False)  
    sleep(Duration)
