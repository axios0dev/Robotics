#!/usr/bin/env python3
# This library contains all of the common constant definitions
# that are used by several of the AxiosRoboticsRCv1 unit modules.

# Python library imports.
from typing import Final

# Xbox 360 controller joystick and trigger constants.
LEFTJOYSTICKDEADZONE: Final[float] = 0.4
RIGHTJOYSTICKDEADZONE: Final[float] = 0.2
RIGHTJOYSTICKHALFPOS: Final[float] = 0.6
TRIGGERDEADZONE: Final[float] = 0.2
TRIGGERQTRPRESSED: Final[float] = 0.25
TRIGGERHALFPRESSED: Final[float] = 0.50
TRIGGERTHREEQTRPRESSED: Final[float] = 0.75

# RGB Headlight colour constants.
RED: Final[str] = "RED"
GREEN: Final[str] = "GREEN"
BLUE: Final[str] = "BLUE"
YELLOW: Final[str] = "YELLOW"
CYAN: Final[str] = "CYAN"
MAGENTA: Final[str] = "MAGENTA"
WHITE: Final[str] = "WHITE"
ORANGE: Final[str] = "ORANGE"
# Constant array of headlights colours to cycle.
HEADLIGHTCOLOURS: Final = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE, ORANGE]
HEADLIGHTCOLOURSLENGTH: Final[int] = len(HEADLIGHTCOLOURS)
# Default headlight colour on startup.
DEFAULTHEADLIGHTCOLOUR: Final[str] = CYAN

# RGB LED state selection constants.
LEDON: Final[str] = "ON"
LEDOFF: Final[str] = "OFF"
NEXTCOLOUR: Final[str] = "NEXT"
PREVCOLOUR: Final[str] = "PREV"
FIRSTCOLOURIDX: Final[int] = 0
LASTCOLOURIDX: Final[int] = HEADLIGHTCOLOURSLENGTH

# Independent physical unit side definitions.
BOTHSIDES: Final[str]= "BOTH"
LEFTSIDE: Final[str]= "LEFT"
RIGHTSIDE: Final[str]= "RIGHT"

# PWM duty cycle constants.
PWMNODUTY: Final[int] = 0
PWMTWENTYFIVEDUTY: Final[int] = 25
PWMFIFTYDUTY: Final[int] = 50
PWMSEVENTYFIVEDUTY: Final[int] = 75
PWMHUNDREDDUTY: Final[int] = 100
# PWM frequency.
PWMFREQUENCY: Final[int] = 100

# Movement speed constants.
DEFAULTACTIONSPEED: Final[int] = 0.1
FRONTMOTORCRAWLSPEED: Final[int] = 7
LOWGEARSPEED: Final[int] = 30
ONEQTRSPEED: Final[int] = PWMTWENTYFIVEDUTY
HALFSPEED: Final[int] = PWMFIFTYDUTY
THREEQTRSPEED: Final[int] = PWMSEVENTYFIVEDUTY
FULLSPEED: Final[int] = PWMHUNDREDDUTY

# LED brightness constant definitions.
FULLBRIGHTNESS: Final[int] = PWMHUNDREDDUTY

