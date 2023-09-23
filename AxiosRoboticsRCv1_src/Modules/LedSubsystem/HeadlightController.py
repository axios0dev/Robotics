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
    if (RequestedState == CommonConstants.LEDON):
        GPIO.output(PinConstants.REDLEDPIN, True)
    elif (RequestedState == CommonConstants.LEDOFF):
        GPIO.output(PinConstants.REDLEDPIN, False)


# Green led on/off.
def GreenLED(RequestedState):
    if (RequestedState == CommonConstants.LEDON):
        GPIO.output(PinConstants.GREENLEDPIN, True)
    elif (RequestedState == CommonConstants.LEDOFF):
        GPIO.output(PinConstants.GREENLEDPIN, False)


# Blue led on/off.
def BlueLED(RequestedState):
    if (RequestedState == CommonConstants.LEDON):
        GPIO.output(PinConstants.BLUELEDPIN, True)
    elif (RequestedState == CommonConstants.LEDOFF):
        GPIO.output(PinConstants.BLUELEDPIN, False)


# RGB headlight mixed colour functions.
# Yellow led on/off.
def YellowLED(RequestedState):
    if (RequestedState == CommonConstants.LEDON):
        RedLED(CommonConstants.LEDON)
        GreenLED(CommonConstants.LEDON)
    elif (RequestedState == CommonConstants.LEDOFF):
        RedLED(CommonConstants.LEDOFF)
        GreenLED(CommonConstants.LEDOFF)


# Cyan led on/off.
def CyanLED(RequestedState):
    if (RequestedState == CommonConstants.LEDON):
        GreenLED(CommonConstants.LEDON)
        BlueLED(CommonConstants.LEDON)
    elif (RequestedState == CommonConstants.LEDOFF):
        GreenLED(CommonConstants.LEDOFF)
        BlueLED(CommonConstants.LEDOFF)


# Magenta led on/off.
def MagentaLED(RequestedState):
    if (RequestedState == CommonConstants.LEDON):
        RedLED(CommonConstants.LEDON)
        BlueLED(CommonConstants.LEDON)
    elif (RequestedState == CommonConstants.LEDOFF):
        RedLED(CommonConstants.LEDOFF)
        BlueLED(CommonConstants.LEDOFF)


# White led on/off.
def WhiteLED(RequestedState):
    if (RequestedState == CommonConstants.LEDON):
        RedLED(CommonConstants.LEDON)
        BlueLED(CommonConstants.LEDON)
        GreenLED(CommonConstants.LEDON)
    elif (RequestedState == CommonConstants.LEDOFF):
        RedLED(CommonConstants.LEDOFF)
        BlueLED(CommonConstants.LEDOFF)
        GreenLED(CommonConstants.LEDOFF)


# Orange led on/off.
def OrangeLED(RequestedState):
    if (RequestedState == CommonConstants.LEDON):
        RedLED(CommonConstants.LEDON)
        YellowLED(CommonConstants.LEDON)
    elif (RequestedState == CommonConstants.LEDOFF):
        RedLED(CommonConstants.LEDOFF)
        YellowLED(CommonConstants.LEDOFF)


# Function to disable all LED pins.        
def LedOff():
    RedLED(CommonConstants.LEDOFF)
    GreenLED(CommonConstants.LEDOFF)
    BlueLED(CommonConstants.LEDOFF)


# Function to select RBG LED colour.
def RGBColorCycle(RequestedColour):
    # All LEDs pins are reset upon colour change, this ensures no
    # unwanted colour mixing occurs.
    # Red LED.
    if (RequestedColour == CommonConstants.RED):
        LedOff()
        RedLED(CommonConstants.LEDON)
    # Green LED.
    elif (RequestedColour == CommonConstants.GREEN):
        LedOff()
        GreenLED(CommonConstants.LEDON)
    # Blue LED.
    elif (RequestedColour == CommonConstants.BLUE):
        LedOff()
        BlueLED(CommonConstants.LEDON)
    # Yellow LED.
    elif (RequestedColour == CommonConstants.YELLOW):
        LedOff()
        YellowLED(CommonConstants.LEDON)
    # Cyan LED.
    elif (RequestedColour == CommonConstants.CYAN):
        LedOff()
        CyanLED(CommonConstants.LEDON)
    # Magenta LED.
    elif (RequestedColour == CommonConstants.MAGENTA):
        LedOff()
        MagentaLED(CommonConstants.LEDON)
    # White LED.
    elif (RequestedColour == CommonConstants.WHITE):
        LedOff()
        WhiteLED(CommonConstants.LEDON)
    # Orange LED.
    elif (RequestedColour == CommonConstants.ORANGE):
        LedOff()
        OrangeLED(CommonConstants.LEDON)

