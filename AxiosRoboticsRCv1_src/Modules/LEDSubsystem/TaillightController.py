#!/usr/bin/env python3
# This module contains the controller code for the dual independent LED
# rear tail light and indicator cluster of the AxiosRoboticsRCv1 unit.

# Python library imports.
from Modules.ConstLib import CommonConstants
from Modules.ConstLib import PinConstants
import RPi.GPIO as GPIO
from time import sleep

# Tail light GPIO configuration.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Left light cluster setup.
GPIO.setup(PinConstants.LEFTBRAKELIGHTPIN, GPIO.OUT)  
GPIO.setup(PinConstants.LEFTINDICATORPIN, GPIO.OUT)
# PWM config at 100Hz.
LeftBrakelightPWM = GPIO.PWM(PinConstants.LEFTBRAKELIGHTPIN, CommonConstants.PWM_FREQUENCY)
LeftIndicatorPWM = GPIO.PWM(PinConstants.LEFTINDICATORPIN, CommonConstants.PWM_FREQUENCY)
# Start PWM duty cycle at 0.
LeftBrakelightPWM.start(CommonConstants.PWM_NO_DUTY)
LeftIndicatorPWM.start(CommonConstants.PWM_NO_DUTY)
# Right light cluster setup.
GPIO.setup(PinConstants.RIGHTBRAKELIGHTPIN, GPIO.OUT)
GPIO.setup(PinConstants.RIGHTINDICATORPIN, GPIO.OUT)
# PWM config at 100Hz.
RightBrakelightPWM = GPIO.PWM(PinConstants.RIGHTBRAKELIGHTPIN, CommonConstants.PWM_FREQUENCY)
RightIndicatorPWM = GPIO.PWM(PinConstants.RIGHTINDICATORPIN, CommonConstants.PWM_FREQUENCY)
# Start PWM duty cycle at 0.
RightBrakelightPWM.start(CommonConstants.PWM_NO_DUTY)
RightIndicatorPWM.start(CommonConstants.PWM_NO_DUTY)


# Tail light cluster functions.
# These functions toggle the brake lights on/off independently. 
# Request a side to turn on the brake lights on that respective side.
def BrakeLightsOn(RequestedBrightness, side=CommonConstants.BOTH_SIDES):
    # Left side.
    if(side == CommonConstants.LEFT_SIDE):
        LeftBrakelightPWM.ChangeDutyCycle(RequestedBrightness)    
    # Right side.
    elif(side == CommonConstants.RIGHT_SIDE): 
        RightBrakelightPWM.ChangeDutyCycle(RequestedBrightness) 
    # Default case is to turn both lights on.    
    elif(side == CommonConstants.BOTH_SIDES):
        LeftBrakelightPWM.ChangeDutyCycle(RequestedBrightness)
        RightBrakelightPWM.ChangeDutyCycle(RequestedBrightness)


# Request a side to turn off the brake lights on that respective side.          
def BrakeLightsOff(side=CommonConstants.BOTH_SIDES):
    # Left side.
    if(side == CommonConstants.LEFT_SIDE):
        LeftBrakelightPWM.ChangeDutyCycle(CommonConstants.PWM_NO_DUTY)
    # Right side.        
    elif(side == CommonConstants.RIGHT_SIDE): 
        RightBrakelightPWM.ChangeDutyCycle(CommonConstants.PWM_NO_DUTY) 
    # Default case is to turn both lights off.    
    elif(side == CommonConstants.BOTH_SIDES):
        LeftBrakelightPWM.ChangeDutyCycle(CommonConstants.PWM_NO_DUTY)
        RightBrakelightPWM.ChangeDutyCycle(CommonConstants.PWM_NO_DUTY)


# These functions toggle the Indicator lights on/off independently. 
# Request a side to turn on the indicator lights on that respective side.  
def IndicatorLightsOn(RequestedBrightness, side=CommonConstants.BOTH_SIDES):
    # Left side.
    if(side == CommonConstants.LEFT_SIDE):
        LeftIndicatorPWM.ChangeDutyCycle(RequestedBrightness) 
    # Right side.       
    elif(side == CommonConstants.RIGHT_SIDE): 
        RightIndicatorPWM.ChangeDutyCycle(RequestedBrightness) 
    # Default case is to turn both lights on.    
    elif(side == CommonConstants.BOTH_SIDES):
        LeftIndicatorPWM.ChangeDutyCycle(RequestedBrightness)
        RightIndicatorPWM.ChangeDutyCycle(RequestedBrightness) 


# Request a side to turn off the indicator lights on that respective side.            
def IndicatorLightsOff(side=CommonConstants.BOTH_SIDES):
    # Left side.
    if(side == CommonConstants.LEFT_SIDE):
        LeftIndicatorPWM.ChangeDutyCycle(CommonConstants.PWM_NO_DUTY)    
    # Right side. 
    elif(side == CommonConstants.RIGHT_SIDE): 
        RightIndicatorPWM.ChangeDutyCycle(CommonConstants.PWM_NO_DUTY) 
    # Default case is to turn both lights off.    
    elif(side == CommonConstants.BOTH_SIDES):
        LeftIndicatorPWM.ChangeDutyCycle(CommonConstants.PWM_NO_DUTY)
        RightIndicatorPWM.ChangeDutyCycle(CommonConstants.PWM_NO_DUTY)    


# This routine indicates that the AxiosRoboticsRCv1 unit is currently
# waiting for a VLC client to establish a TCP connection. The indicator
# lights flash off and on until a connection is established.
def SyncIndicators(WaitingForConnection):
    # These indicators will continue to cycle on and off until the 
    # threading event variable is unset once a TCP connection is established.
    while WaitingForConnection.is_set():
        IndicatorLightsOn(CommonConstants.FULL_BRIGHTNESS)
        sleep(0.5)
        IndicatorLightsOff()
        sleep(0.5)
    
