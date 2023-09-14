#!/usr/bin/env python3
# This module contains the controller code for the dual independent LED,
# rear tail light and indicator cluster of the AxiosRoboticsRCv1 unit.
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Tail light Pin Setup.
# Left light cluster setup.
LeftBrakeLightPin = 11
LeftIndicatorPin = 9
GPIO.setup(LeftBrakeLightPin, GPIO.OUT)  
GPIO.setup(LeftIndicatorPin, GPIO.OUT)
# PWM config at 100Hz.
LeftBrakeLightPWM = GPIO.PWM(LeftBrakeLightPin, 100)
LeftIndicatorPWM = GPIO.PWM(LeftIndicatorPin, 100)
# Start PWM duty cycle at 0.
LeftBrakeLightPWM.start(0)
LeftIndicatorPWM.start(0)
# Right light cluster setup.
RightBrakeLightPin = 10
RightIndicatorPin = 6
GPIO.setup(RightBrakeLightPin, GPIO.OUT)
GPIO.setup(RightIndicatorPin, GPIO.OUT)
# PWM config at 100Hz.
RightBrakeLightPWM = GPIO.PWM(RightBrakeLightPin, 100)
RightIndicatorPWM = GPIO.PWM(RightIndicatorPin, 100)
# Start PWM duty cycle at 0.
RightBrakeLightPWM.start(0)
RightIndicatorPWM.start(0)


# Tail light cluster functions.
# Brake lights, brightness >= 0 && <= 100.
def LeftBrakeLightOn(brightness):
    LeftBrakeLightPWM.ChangeDutyCycle(brightness)


def RightBrakeLightOn(brightness):
    RightBrakeLightPWM.ChangeDutyCycle(brightness)

    
def BrakeLightsOff(side="ALL"):
    if(side == "LEFT"):
        LeftBrakeLightPWM.ChangeDutyCycle(0)    
    elif(side == "RIGHT"): 
        RightBrakeLightPWM.ChangeDutyCycle(0) 
    # Default case is to turn both lights off.    
    elif(side == "ALL"):
        LeftBrakeLightPWM.ChangeDutyCycle(0)
        RightBrakeLightPWM.ChangeDutyCycle(0)


# Indicator lights, brightness >= 0 && <= 100.
def LeftIndicatorOn(brightness):
    LeftIndicatorPWM.ChangeDutyCycle(brightness)


def RightIndicatorOn(brightness):
    RightIndicatorPWM.ChangeDutyCycle(brightness)

    
def IndicatorLightsOff(side="ALL"):
    if(side == "LEFT"):
        LeftIndicatorPWM.ChangeDutyCycle(0)    
    elif(side == "RIGHT"): 
        RightIndicatorPWM.ChangeDutyCycle(0) 
    # Default case is to turn both lights off.    
    elif(side == "ALL"):
        LeftIndicatorPWM.ChangeDutyCycle(0)
        RightIndicatorPWM.ChangeDutyCycle(0)    
