#!/usr/bin/env python3

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

RedPin = 26
GreenPin = 13
BluePin = 19

# RBG Headlight Pin Setup
GPIO.setup(RedPin, GPIO.OUT)  # RED
GPIO.setup(GreenPin, GPIO.OUT)  # GREEN
GPIO.setup(BluePin, GPIO.OUT)  # BLUE

# RGB Headlight Colours
# RGB  COLOUR FUNCTIONS/COMBINATIONS
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
        
def LedOff():
    RedLed("OFF")
    GreenLed("OFF")
    BlueLed("OFF")
    
            


# Program To Cycle RGB Headlight Colours On 360 Controller D-Pad
def RGBcolorcycle(selection):
    # All Led States Account For Both The Next And Prevous Led Colour And Disables Them
    # Red Led
    if selection == "RED":
        OrangeLed("OFF")
        GreenLed("OFF")
        RedLed("ON")
    # Green Led
    elif selection == "GREEN":
        RedLed("OFF")
        BlueLed("OFF")
        GreenLed("ON")
    # Blue Led
    elif selection == "BLUE":
        GreenLed("OFF")
        YellowLed("OFF")
        BlueLed("ON")
    # Yellow Led
    elif selection == "YELLOW":
        BlueLed("OFF")
        CyanLed("OFF")
        YellowLed("ON")
    # Cyan Led
    elif selection == "CYAN":
        YellowLed("OFF")
        MagentaLed("OFF")
        CyanLed("ON")
    # Magenta Led
    elif selection == "Magenta":
        CyanLed("OFF")
        WhiteLed("OFF")
        MagentaLed("ON")
    # White Led
    elif selection == "WHITE":
        MagentaLed("OFF")
        OrangeLed("OFF")
        WhiteLed("ON")
    # Orange Led
    elif selection == "ORANGE":
        WhiteLed("OFF")
        RedLed("OFF")
        OrangeLed("ON")



