#!/usr/bin/env python3
# This library contains all of the Pin constant definitions
# that are used by several of the AxiosRoboticsRCv1 unit functions.

# Python library imports.
from typing import Final

# RGB LED pin configuration.
RED_LED_PIN: Final[int] = 26
GREEN_LED_PIN: Final[int] = 13
BLUE_LED_PIN: Final[int] = 19

# Tail light cluster pin configuration.
LEFT_BRAKELIGHT_PIN: Final[int] = 11
LEFT_INDICATOR_PIN: Final[int] = 9
RIGHT_BRAKELIGHT_PIN: Final[int] = 10
RIGHT_INDICATOR_PIN: Final[int] = 6

# Front motor controller pin configuration.
FRONT_LEFT_MOTOR_FORWARD_PIN: Final[int] = 24
FRONT_LEFT_MOTOR_REVERSE_PIN: Final[int] = 23
FRONT_LEFT_MOTOR_SPEED_CONTROL_PIN: Final[int] = 14
# Front right motor.
FRONT_RIGHT_MOTOR_FORWARD_PIN: Final[int] = 25
FRONT_RIGHT_MOTOR_REVERSE_PIN: Final[int] = 12
FRONT_RIGHT_MOTOR_SPEED_CONTROL_PIN: Final[int] = 15

# Rear left motor.
REAR_LEFT_MOTOR_FORWARD_PIN: Final[int] = 27
REAR_LEFT_MOTOR_REVERSE_PIN: Final[int] = 22
REAR_LEFT_MOTOR_SPEED_CONTROL_PIN: Final[int] = 0
# Rear right motor.
REAR_RIGHT_MOTOR_FORWARD_PIN: Final[int] = 18
REAR_RIGHT_MOTOR_REVERSE_PIN: Final[int] = 17
REAR_RIGHT_MOTOR_SPEED_CONTROL_PIN: Final[int] = 5
