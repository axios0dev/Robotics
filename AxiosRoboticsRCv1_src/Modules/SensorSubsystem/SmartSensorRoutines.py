#!/usr/bin/env python3
# This module contains all of the smart sensor routines which consists of functions
# to avoid collisions with objects detected by the front sensor module and also a function
# which facilitates a self driving AI mode.

# Python library imports.
from typing import Final
# AxiosRobtoticsRCv1 submodule and common library imports.
from Modules.ConstLib import CommonConstants
from Modules.MotorSubsystem import MotorController
from Modules.LEDSubsystem import TaillightController
from Modules.Xbox360ControllerRoutines import Xbox360ControllerAPI


# This function stops the current drive trajectory when a collision is detected,
# stops the AxiosRobtocisRCv1 unit in its tracks. Alerts the operator which side the potential
# collision was detected on via the indicator LED and reverses the unit to create space
# between the unit and the object that was detected. At this point the user can regain control
# of the unit and can decide how to best proceed.
def AvoidCollision(Side):
    # Stop all motors.
    MotorController.StopMotors()
    # Turn on the respective indicator to show which side the obstacle was detected on.
    TaillightController.IndicatorLightsOn(CommonConstants.FULLBRIGHTNESS, Side)
    # Drive backwards for 0.3 seconds to avoid obstacle.
    MotorController.DriveBackwards(CommonConstants.FULLSPEED, 0.3)
    # Turn off indicator after this routine has finished.
    TaillightController.IndicatorLightsOff(Side)
    # Return back to the ControllerRoutines function.
    return 


# This function is used by the self driving AI routine, this is called when entrapment has been detected,
# this is designed to allow the AxiosRoboticsRCv1 unit to navigate itself out of a corner or crowded space.
def AvoidEntrapment(Side):
    # Stop all motors.
    MotorController.StopMotors()
    # Turn on the respective indicator to show which side the obstacle was detected on.
    TaillightController.IndicatorLightsOn(CommonConstants.FULLBRIGHTNESS, Side)
    # Drive backwards for 0.4 seconds to avoid obstacle.
    MotorController.DriveBackwards(CommonConstants.FULLSPEED, 0.4)
    # Turn off indicator after this routine has finished.
    TaillightController.IndicatorLightsOff(Side)
    # Turn 90 degrees and continue
    if(side == CommonConstants.LEFTSIDE):
        MotorController.PivotLeft(CommonConstants.FULLSPEED, 0.6)
    elif(side == CommonConstants.RIGHTSIDE):
        MotorController.PivotRight(CommonConstants.FULLSPEED, 0.6)
     # Return back to the ControllerRoutines function.
    return 


# This function is called by the self driving AI routine when an obstacle is detected.
# This will halt the unit, turn on the indicator corresponding to the side that the obstacle
# was detected, then it will turn to avoid the obstacle and continue.
def AvoidObstacle(Side):
    # Stop all motors.
    MotorController.StopMotors()
    # Turn on the respective indicator to show which side the obstacle was detected on.
    TaillightController.IndicatorLightsOn(CommonConstants.FULLBRIGHTNESS, Side)
    # Drive backwards for 0.3 seconds to avoid obstacle.
    MotorController.DriveBackwards(CommonConstants.HALFSPEED, 0.5)
    # Turn off indicator after this routine has finished.
    TaillightController.IndicatorLightsOff(Side)
      # Turn briefly and continue
    if(side == CommonConstants.LEFTSIDE):
        MotorController.TurnLeft(CommonConstants.FULLSPEED, 0.6)
    elif(side == CommonConstants.RIGHTSIDE):
        MotorController.TurnRight(CommonConstants.FULLSPEED, 0.6)
    # Return back to the ControllerRoutines function.
    return 


DETECTIONSUNTILENTRAPMENT: Final[int] = 3


# The AxiosRoboticsRCv1 unit will enter an infinite loop and will drive around,
# endlessly avoiding collisions and entrapment in corners.
def SelfDrivingAI(Controller):
    SelfDrivingAIActive = True
    # Entrapment detection variables.
    LeftSensorDetectionCount = 0
    RightSensorDetectionCount = 0
    while SelfDrivingAIActive:
        # Left bumper exists this self driving mode loop and returns.
        # to normal operation.
        if Controller.leftBumper():
            MotorController.StopMotors()
            SelfDrivingAIActive = False
            return    
        # If entrapment is detected by reverse and turn to navigate out of the corner.
        # Entrapment by left side.    
        elif (LeftSensorDetectionCount == DETECTIONSUNTILENTRAPMENT):
            AvoidEntrapment(CommonConstants.LEFTSIDE)
            LeftSensorDetectionCount = 0
         # Entrapment by right side.       
        elif (RightSensorDetectionCount == DETECTIONSUNTILENTRAPMENT):
            AvoidEntrapment(CommonConstants.RIGHTSIDE)
            RightSensorDetectionCount = 0 
        # Avoid all obstacles.    
        # Object detected on left side avoid obstacle.    
        elif (GPIO.input(LeftalrtAI) == 1):
            AvoidObstacle(CommonConstants.LEFTSIDE)
            LeftSensorDetectionCount += 1
        # Object detected on right side avoid obstacle.    
        elif (GPIO.input(RightalrtAI) == 1):
            AvoidObstacle(CommonConstants.RIGHTSIDE)
            RightSensorDetectionCount += 1   
        # Drive forwards at full speed if no objects are detected.    
        else:
            MotorController.DriveForwards(CommonConstants.FULLSPEED, CommonConstants.DEFAULTACTIONDURATION)
    # Return back to the ControllerRoutines function.
    return 

