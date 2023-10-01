#!/usr/bin/env python3
# This library contains all of the common constant definitions
# that are used by several of the AxiosRoboticsRCv1 unit modules.

# Python library imports.
from typing import Final

# Xbox 360 controller joystick and trigger constants.
LEFT_JOYSTICK_DEADZONE: Final[float] = 0.4
RIGHT_JOYSTICK_DEADZONE: Final[float] = 0.2
RIGHT_JOYSTICK_HALFPOS: Final[float] = 0.6
TRIGGER_DEADZONE: Final[float] = 0.2
TRIGGER_QTR_PRESSED: Final[float] = 0.25
TRIGGER_HALF_PRESSED: Final[float] = 0.50
TRIGGER_THREE_QTR_PRESSED: Final[float] = 0.75

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
HEADLIGHT_COLOURS: Final = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE, ORANGE]
HEADLIGHT_COLOURS_LENGTH: Final[int] = len(HEADLIGHTCOLOURS)
# Default headlight colour on startup.
DEFAULT_HEADLIGHT_COLOUR: Final[str] = CYAN

# RGB LED state selection constants.
LED_ON: Final[str] = "ON"
LED_OFF: Final[str] = "OFF"
NEXT_COLOUR: Final[str] = "NEXT"
PREV_COLOUR: Final[str] = "PREV"
FIRST_COLOUR_IDX: Final[int] = 0
LAST_COLOUR_IDX: Final[int] = HEADLIGHT_COLOURS_LENGTH

# Independent physical unit side definitions.
BOTH_SIDES: Final[str]= "BOTH"
LEFT_SIDE: Final[str]= "LEFT"
RIGHT_SIDE: Final[str]= "RIGHT"

# PWM duty cycle constants.
PWM_NO_DUTY: Final[int] = 0
PWM_TWENTY_FIVE_DUTY: Final[int] = 25
PWM_FIFTY_DUTY: Final[int] = 50
PWM_SEVENTY_FIVE_DUTY: Final[int] = 75
PWM_HUNDRED_DUTY: Final[int] = 100
# PWM frequency.
PWM_FREQUENCY: Final[int] = 100

# Movement speed constants.
DEFAULT_ACTION_DURATION: Final[int] = 0.1
LOW_GEAR_SPEED: Final[int] = 30
ONE_QTR_SPEED: Final[int] = PWM_TWENTY_FIVE_DUTY
HALF_SPEED: Final[int] = PWM_FIFTY_DUTY
THREE_QTR_SPEED: Final[int] = PWM_SEVENTY_FIVE_DUTY
FULL_SPEED: Final[int] = PWM_HUNDRED_DUTY

# LED brightness constant definitions.
FULL_BRIGHTNESS: Final[int] = PWM_HUNDRED_DUTY

