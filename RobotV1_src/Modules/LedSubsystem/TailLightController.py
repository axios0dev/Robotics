#!/usr/bin/env python3


# Tail Light Pin Setup
# Left Side
GPIO.setup(10, GPIO.OUT)  # Left Brake Light
GPIO.setup(9, GPIO.OUT)  # Left Indicator
# Right Side
GPIO.setup(11, GPIO.OUT)  # Right Brake Light
GPIO.setup(6, GPIO.OUT)  # Right Indicator