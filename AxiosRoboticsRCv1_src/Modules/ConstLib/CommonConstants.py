#!/usr/bin/env python3
# This library contains all of the common constant definitions
# that are used by several of the AxiosRoboticsRCv1 unit.

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
HEADLIGHTCOLOURS: Final = ["RED", "GREEN", "BLUE", "YELLOW", "CYAN", "Magenta", "WHITE", "ORANGE"]
HEADLIGHTCOLOURSLENGTH: Final[int] = len(HEADLIGHTCOLOURS)
# Default headlight colour on startup.
DEFAULTHEADLIGHTCOLOUR: Final[str] = "CYAN"

# RGB LED state selection constants.
LEDON: Final[str] = "ON"
LEDOFF: Final[str] = "OFF"
NEXTCOLOUR: Final[str] = "NEXT"
PREVCOLOUR: Final[str] = "PREV"
FIRSTCOLOURIDX: Final[int] = 0
LASTCOLOURIDX: Final[int] = HEADLIGHTCOLOURSLENGTH

# PWM duty cycle constants.
PWMTWENTYFIVEDUTY: Final[int] = 25
PWMFIFTYDUTY: Final[int] = 50
PWMSEVENTYFIVEDUTY: Final[int] = 75
PWMHUNDREDDUTY: Final[int] = 100

# Movement speed constants.
DEFAULTACTIONSPEED: Final[int] = 0.1
FRONTMOTORCRAWLSPEED: Final[int] = 7
LOWGEARSPEED: Final[int] = 30
ONEQTRSPEED: Final[int] = PWMTWENTYFIVEDUTY
HALFSPEED: Final[int] = PWMFIFTYDUTY
THREEQTRSPEED: Final[int] = PWMSEVENTYFIVEDUTY
FULLSPEED: Final[int] = PWMHUNDREDDUTY
