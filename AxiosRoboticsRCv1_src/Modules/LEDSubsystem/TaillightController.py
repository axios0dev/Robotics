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
LeftBrakelightPWM = GPIO.PWM(PinConstants.LEFTBRAKELIGHTPIN, CommonConstants.PWMFREQUENCY)
LeftIndicatorPWM = GPIO.PWM(PinConstants.LEFTINDICATORPIN, CommonConstants.PWMFREQUENCY)
# Start PWM duty cycle at 0.
LeftBrakelightPWM.start(CommonConstants.PWMNODUTY)
LeftIndicatorPWM.start(CommonConstants.PWMNODUTY)
# Right light cluster setup.
GPIO.setup(PinConstants.RIGHTBRAKELIGHTPIN, GPIO.OUT)
GPIO.setup(PinConstants.RIGHTINDICATORPIN, GPIO.OUT)
# PWM config at 100Hz.
RightBrakelightPWM = GPIO.PWM(PinConstants.RIGHTBRAKELIGHTPIN, CommonConstants.PWMFREQUENCY)
RightIndicatorPWM = GPIO.PWM(PinConstants.RIGHTINDICATORPIN, CommonConstants.PWMFREQUENCY)
# Start PWM duty cycle at 0.
RightBrakelightPWM.start(CommonConstants.PWMNODUTY)
RightIndicatorPWM.start(CommonConstants.PWMNODUTY)


# Tail light cluster functions.
# These functions toggle the brake lights on/off independently. 
# Request a side to turn on the brake lights on that respective side.
def BrakeLightsOn(RequestedBrightness, side=CommonConstants.BOTHSIDES):
    # Left side.
    if(side == CommonConstants.LEFTSIDE):
        LeftBrakelightPWM.ChangeDutyCycle(RequestedBrightness)    
    # Right side.
    elif(side == CommonConstants.RIGHTSIDE): 
        RightBrakelightPWM.ChangeDutyCycle(RequestedBrightness) 
    # Default case is to turn both lights on.    
    elif(side == CommonConstants.BOTHSIDES):
        LeftBrakelightPWM.ChangeDutyCycle(RequestedBrightness)
        RightBrakelightPWM.ChangeDutyCycle(RequestedBrightness)


# Request a side to turn off the brake lights on that respective side.          
def BrakeLightsOff(side=CommonConstants.BOTHSIDES):
    # Left side.
    if(side == CommonConstants.LEFTSIDE):
        LeftBrakelightPWM.ChangeDutyCycle(CommonConstants.PWMNODUTY)
    # Right side.        
    elif(side == CommonConstants.RIGHTSIDE): 
        RightBrakelightPWM.ChangeDutyCycle(CommonConstants.PWMNODUTY) 
    # Default case is to turn both lights off.    
    elif(side == CommonConstants.BOTHSIDES):
        LeftBrakelightPWM.ChangeDutyCycle(CommonConstants.PWMNODUTY)
        RightBrakelightPWM.ChangeDutyCycle(CommonConstants.PWMNODUTY)


# These functions toggle the Indicator lights on/off independently. 
# Request a side to turn on the indicator lights on that respective side.  
def IndicatorLightsOn(RequestedBrightness, side=CommonConstants.BOTHSIDES):
    # Left side.
    if(side == CommonConstants.LEFTSIDE):
        LeftIndicatorPWM.ChangeDutyCycle(RequestedBrightness) 
    # Right side.       
    elif(side == CommonConstants.RIGHTSIDE): 
        RightIndicatorPWM.ChangeDutyCycle(RequestedBrightness) 
    # Default case is to turn both lights on.    
    elif(side == CommonConstants.BOTHSIDES):
        LeftIndicatorPWM.ChangeDutyCycle(RequestedBrightness)
        RightIndicatorPWM.ChangeDutyCycle(RequestedBrightness) 


# Request a side to turn off the indicator lights on that respective side.            
def IndicatorLightsOff(side=CommonConstants.BOTHSIDES):
    # Left side.
    if(side == CommonConstants.LEFTSIDE):
        LeftIndicatorPWM.ChangeDutyCycle(CommonConstants.PWMNODUTY)    
    # Right side. 
    elif(side == CommonConstants.RIGHTSIDE): 
        RightIndicatorPWM.ChangeDutyCycle(CommonConstants.PWMNODUTY) 
    # Default case is to turn both lights off.    
    elif(side == CommonConstants.BOTHSIDES):
        LeftIndicatorPWM.ChangeDutyCycle(CommonConstants.PWMNODUTY)
        RightIndicatorPWM.ChangeDutyCycle(CommonConstants.PWMNODUTY)    


# This routine indicates that the AxiosRoboticsRCv1 unit is currently
# waiting for a VLC client to establish a TCP connection. The indicator
# lights flash off and on until a connection is established.
def SyncIndicators(WaitingForConnection):
    # These indicators will continue to cycle on and off until the 
    # threading event variable is unset once a TCP connection is established.
    while WaitingForConnection.is_set():
        IndicatorLightsOn(CommonConstants.FULLBRIGHTNESS)
        sleep(0.5)
        IndicatorLightsOff()
        sleep(0.5)
    
