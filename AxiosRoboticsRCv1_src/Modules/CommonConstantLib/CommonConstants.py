#!/usr/bin/env python3
from typing import Final

LEFTJOYSTICKDEADZONE: Final[float] = 0.4
RIGHTJOYSTICKDEADZONE: Final[float] = 0.2
RIGHTJOYSTICKHALFPOS: Final[float] = 0.6
TRIGGERDEADZONE: Final[float] = 0.2
TRIGGERQTRPRESSED: Final[float] = 0.25
TRIGGERHALFPRESSED: Final[float] = 0.50
TRIGGERTHREEQTRPRESSED: Final[float] = 0.75


HEADLIGHTCOLOURS: Final = ["RED", "GREEN", "BLUE", "YELLOW", "CYAN", "Magenta", "WHITE", "ORANGE"]
HEADLIGHTCOLOURSLENGTH: Final[int] = len(HEADLIGHTCOLOURS)
# Default headlight colour on startup.
DEFAULTHEADLIGHTCOLOUR: Final[str] = "CYAN"


LEDON: Final[str] = "ON"
LEDOFF: Final[str] = "OFF"
NEXTCOLOUR : Final[str] = "NEXT"
PREVCOLOUR : Final[str] = "PREV"
FIRSTCOLOURIDX : Final[int] = 0
LASTCOLOURIDX : Final[int] = HEADLIGHTCOLOURSLENGTH

PWMTWENTYFIVEDUTY: Final[int] = 25
PWMFIFTYDUTY: Final[int] = 50
PWMSEVENTYFIVEDUTY: Final[int] = 75
PWMHUNDREDDUTY: Final[int] = 100



DEFAULTACTIONSPEED: Final[int] = 0.1
FRONTMOTORCRAWLSPEED: Final[int] = 7
ONEQTRSPEED: Final[int] = PWMTWENTYFIVEDUTY
HALFSPEED: Final[int] = PWMFIFTYDUTY
THREEQTRSPEED: Final[int] = PWMSEVENTYFIVEDUTY
FULLSPEED: Final[int] = PWMHUNDREDDUTY