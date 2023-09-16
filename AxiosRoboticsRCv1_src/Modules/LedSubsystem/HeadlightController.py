#!/usr/bin/env python3
# This modules contains the code to control the RBG LED headlights,
# of the AxiosRoboticsRCv1 unit.
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin definitions.
RedPin = 26
GreenPin = 13
BluePin = 19
# Pin Setup.
GPIO.setup(RedPin, GPIO.OUT)  # RED
GPIO.setup(GreenPin, GPIO.OUT)  # GREEN
GPIO.setup(BluePin, GPIO.OUT)  # BLUE


# RGB headlight base colour functions.
def RedLed(state):
    if (state == "ON"):
        GPIO.output(RedPin, True)
    elif (state == "OFF"):
        GPIO.output(RedPin, False)


def GreenLed(state):
    if (state == "ON"):
        GPIO.output(GreenPin, True)
    elif (state == "OFF"):
        GPIO.output(GreenPin, False)


def BlueLed(state):
    if (state == "ON"):
        GPIO.output(BluePin, True)
    elif (state == "OFF"):
        GPIO.output(BluePin, False)


# RGB headlight mixed colour functions.
def YellowLed(state):
    if (state == "ON"):
        RedLed("ON")
        GreenLed("ON")
    elif (state == "OFF"):
        RedLed("OFF")
        GreenLed("OFF")


def CyanLed(state):
    if (state == "ON"):
        GreenLed("ON")
        BlueLed("ON")
    elif (state == "OFF"):
        GreenLed("OFF")
        BlueLed("OFF")


def MagentaLed(state):
    if (state == "ON"):
        RedLed("ON")
        BlueLed("ON")
    elif (state == "OFF"):
        RedLed("OFF")
        BlueLed("OFF")


def WhiteLed(state):
    if (state == "ON"):
        RedLed("ON")
        BlueLed("ON")
        GreenLed("ON")
    elif (state == "OFF"):
        RedLed("OFF")
        BlueLed("OFF")
        GreenLed("OFF")


def OrangeLed(state):
    if (state == "ON"):
        RedLed("ON")
        YellowLed("ON")
    elif (state == "OFF"):
        RedLed("OFF")
        YellowLed("OFF")


# Function to disable all LED pins.        
def LedOff():
    RedLed("OFF")
    GreenLed("OFF")
    BlueLed("OFF")


# Function to select RBG led colour.
def RGBColorCycle(selection):
    # All leds pins are reset upon colour change, this ensures no unwanted colour mixing occurs.
    # Red Led.
    if selection == "RED":
        LedOff()
        OrangeLed("OFF")
        GreenLed("OFF")
        RedLed("ON")
    # Green Led.
    elif selection == "GREEN":
        LedOff()
        RedLed("OFF")
        BlueLed("OFF")
        GreenLed("ON")
    # Blue Led.
    elif selection == "BLUE":
        LedOff()
        GreenLed("OFF")
        YellowLed("OFF")
        BlueLed("ON")
    # Yellow Led.
    elif selection == "YELLOW":
        LedOff()
        BlueLed("OFF")
        CyanLed("OFF")
        YellowLed("ON")
    # Cyan Led.
    elif selection == "CYAN":
        LedOff()
        YellowLed("OFF")
        MagentaLed("OFF")
        CyanLed("ON")
    # Magenta Led.
    elif selection == "Magenta":
        LedOff()
        CyanLed("OFF")
        WhiteLed("OFF")
        MagentaLed("ON")
    # White Led.
    elif selection == "WHITE":
        LedOff()
        MagentaLed("OFF")
        OrangeLed("OFF")
        WhiteLed("ON")
    # Orange Led.
    elif selection == "ORANGE":
        LedOff()
        WhiteLed("OFF")
        RedLed("OFF")
        OrangeLed("ON")

