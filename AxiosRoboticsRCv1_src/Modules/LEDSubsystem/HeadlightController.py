#!/usr/bin/env python3
# This modules contains the code to control the RBG LED headlights
# of the AxiosRoboticsRCv1 unit.

# Python library imports.
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# AxiosRobtoticsRCv1 common library imports.
from Modules.ConstLib import CommonConstants
from Modules.ConstLib import PinConstants

# GPIO pin configuration.
GPIO.setup(PinConstants.REDLEDPIN, GPIO.OUT)  
GPIO.setup(PinConstants.GREENLEDPIN, GPIO.OUT)  
GPIO.setup(PinConstants.BLUELEDPIN, GPIO.OUT)  #


# RGB headlight base colour functions.
# Red led on/off.
def RedLED(RequestedState):
    if (RequestedState == CommonConstants.LED_ON):
        GPIO.output(PinConstants.REDLEDPIN, True)
    elif (RequestedState == CommonConstants.LED_OFF):
        GPIO.output(PinConstants.REDLEDPIN, False)


# Green led on/off.
def GreenLED(RequestedState):
    if (RequestedState == CommonConstants.LED_ON):
        GPIO.output(PinConstants.GREENLEDPIN, True)
    elif (RequestedState == CommonConstants.LED_OFF):
        GPIO.output(PinConstants.GREENLEDPIN, False)


# Blue led on/off.
def BlueLED(RequestedState):
    if (RequestedState == CommonConstants.LED_ON):
        GPIO.output(PinConstants.BLUELEDPIN, True)
    elif (RequestedState == CommonConstants.LED_OFF):
        GPIO.output(PinConstants.BLUELEDPIN, False)


# RGB headlight mixed colour functions.
# Yellow led on/off.
def YellowLED(RequestedState):
    if (RequestedState == CommonConstants.LED_ON):
        RedLED(CommonConstants.LED_ON)
        GreenLED(CommonConstants.LED_ON)
    elif (RequestedState == CommonConstants.LED_OFF):
        RedLED(CommonConstants.LED_OFF)
        GreenLED(CommonConstants.LED_OFF)


# Cyan led on/off.
def CyanLED(RequestedState):
    if (RequestedState == CommonConstants.LED_ON):
        GreenLED(CommonConstants.LED_ON)
        BlueLED(CommonConstants.LED_ON)
    elif (RequestedState == CommonConstants.LED_OFF):
        GreenLED(CommonConstants.LED_OFF)
        BlueLED(CommonConstants.LED_OFF)


# Magenta led on/off.
def MagentaLED(RequestedState):
    if (RequestedState == CommonConstants.LED_ON):
        RedLED(CommonConstants.LED_ON)
        BlueLED(CommonConstants.LED_ON)
    elif (RequestedState == CommonConstants.LED_OFF):
        RedLED(CommonConstants.LED_OFF)
        BlueLED(CommonConstants.LED_OFF)


# White led on/off.
def WhiteLED(RequestedState):
    if (RequestedState == CommonConstants.LED_ON):
        RedLED(CommonConstants.LED_ON)
        BlueLED(CommonConstants.LED_ON)
        GreenLED(CommonConstants.LED_ON)
    elif (RequestedState == CommonConstants.LED_OFF):
        RedLED(CommonConstants.LED_OFF)
        BlueLED(CommonConstants.LED_OFF)
        GreenLED(CommonConstants.LED_OFF)


# Orange led on/off.
def OrangeLED(RequestedState):
    if (RequestedState == CommonConstants.LED_ON):
        RedLED(CommonConstants.LED_ON)
        YellowLED(CommonConstants.LED_ON)
    elif (RequestedState == CommonConstants.LED_OFF):
        RedLED(CommonConstants.LED_OFF)
        YellowLED(CommonConstants.LED_OFF)


# Function to disable all LED pins.        
def LEDOff():
    RedLED(CommonConstants.LED_OFF)
    GreenLED(CommonConstants.LED_OFF)
    BlueLED(CommonConstants.LED_OFF)


# Function to select RBG LED colour.
def RGBColorCycle(RequestedColour):
    # All LEDs pins are reset upon colour change, this ensures no
    # unwanted colour mixing occurs.
    # Red LED.
    if (RequestedColour == CommonConstants.RED):
        LEDOff()
        RedLED(CommonConstants.LED_ON)
    # Green LED.
    elif (RequestedColour == CommonConstants.GREEN):
        LEDOff()
        GreenLED(CommonConstants.LED_ON)
    # Blue LED.
    elif (RequestedColour == CommonConstants.BLUE):
        LEDOff()
        BlueLED(CommonConstants.LED_ON)
    # Yellow LED.
    elif (RequestedColour == CommonConstants.YELLOW):
        LEDOff()
        YellowLED(CommonConstants.LED_ON)
    # Cyan LED.
    elif (RequestedColour == CommonConstants.CYAN):
        LEDOff()
        CyanLED(CommonConstants.LED_ON)
    # Magenta LED.
    elif (RequestedColour == CommonConstants.MAGENTA):
        LEDOff()
        MagentaLED(CommonConstants.LED_ON)
    # White LED.
    elif (RequestedColour == CommonConstants.WHITE):
        LEDOff()
        WhiteLED(CommonConstants.LED_ON)
    # Orange LED.
    elif (RequestedColour == CommonConstants.ORANGE):
        LEDOff()
        OrangeLED(CommonConstants.LED_ON)

