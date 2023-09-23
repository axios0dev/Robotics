#!/usr/bin/env python3
# This library contains all of the Pin constant definitions
# that are used by several of the AxiosRoboticsRCv1 unit functions.

# Python library imports.
from typing import Final

# RGB LED pin configuration.
REDLEDPIN: Final[int] = 26
GREENLEDPIN: Final[int] = 13
BLUELEDPIN: Final[int] = 19

# Tail light cluster pin configuration.
LEFTBRAKELIGHTPIN: Final[int] = 11
LEFTINDICATORPIN: Final[int] = 9
RIGHTBRAKELIGHTPIN: Final[int] = 10
RIGHTINDICATORPIN: Final[int] = 6

# Front motor controller pin configuration.
FRONTLEFTMOTORFORWARDPIN: Final[int] = 24
FRONTLEFTMOTORREVERSEPIN: Final[int] = 23
FRONTLEFTMOTORSPEEDCONTROLPIN: Final[int] = 14
# Front right motor.
FRONTRIGHTMOTORFORWARDPIN: Final[int] = 25
FRONTRIGHTMOTORREVERSEPIN: Final[int] = 12
FRONTRIGHTMOTORSPEEDCONTROLPIN: Final[int] = 15

# Rear left motor.
REARLEFTMOTORFORWARDPIN: Final[int] = 27
REARLEFTMOTORREVERSEPIN: Final[int] = 22
REARLEFTMOTORSPEEDCONTROLPIN: Final[int] = 0
# Rear right motor.
REARRIGHTMOTORFORWARDPIN: Final[int] = 18
REARRIGHTMOTORREVERSEPIN: Final[int] = 17
REARRIGHTMOTORSPEEDCONTROLPIN: Final[int] = 5
