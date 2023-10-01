#!/usr/bin/env python3
# This module contains the Xbox 360 controller subroutines for the AxiosRoboticsRCv1 unit.

# Python library imports.
import RPi.GPIO as GPIO
from time import sleep
from os import system 
# AxiosRobtoticsRCv1 submodule and common library imports.
from Modules.CameraSubsystem import CameraController
from Modules.ConstLib import CommonConstants
from Modules.LEDSubsystem import HeadlightController
from Modules.MotorSubsystem import MotorController
from Modules.LEDSubsystem import TaillightController
from Modules.Xbox360ControllerRoutines import Xbox360ControllerAPI
from Modules.Xbox360ControllerRoutines import Xbox360ControllerMainRoutine

# This variable holds the index of the currently selected RGB headlight colour.
CurrentRGBHeadlightColour = CommonConstants.HEADLIGHT_COLOURS.index(CommonConstants.DEFAULT_HEADLIGHT_COLOUR)


# This subroutine takes in a requested state for the RGB headlight modules and performs the requested action, 
# either turning the lights on/off or cycles through the colours. 
def RGBHeadlightDpadRoutine(NextState):
    # Current and next selection variables.
    global CurrentRGBHeadlightColour
    selection = None
    
    # Turn off the RGB headlights.
    if(NextState == CommonConstants.LED_OFF):
        HeadlightController.LEDOff()
        Xbox360ControllerMainRoutine.RGBHeadLightOn = False
        # Return back to the ControllerRoutines function.
        return
    # Turn on the RGB headlights. 
    elif(NextState == CommonConstants.LED_ON):
        Xbox360ControllerMainRoutine.RGBHeadLightOn = True
        HeadlightController.RGBColorCycle(CommonConstants.HEADLIGHT_COLOURS[CurrentRGBHeadlightColour])
        # Return back to the ControllerRoutines function.
        return   
    
    # Change the RGB headlights to the next available colour. 
    if(NextState == CommonConstants.NEXT_COLOUR):
        Selection = 1
    # Change the RGB headlights to the previous available colour.     
    elif(NextState == CommonConstants.PREV_COLOUR):
        Selection = -1 
         
    # Check if the selection is beyond the first colour avalible, then wrap around back to the last. 
    if((CurrentRGBHeadlightColour + Selection) < CommonConstants.FIRST_COLOUR_IDX):
        CurrentRGBHeadlightColour = CommonConstants.LAST_COLOUR_IDX - 1    
    # Check if the selection is beyond the last colour avalible, then wrap around back to the first.    
    elif((CurrentRGBHeadlightColour + Selection) >= CommonConstants.LAST_COLOUR_IDX):
        CurrentRGBHeadlightColour = CommonConstants.FIRST_COLOUR_IDX
    # If no wrap around is detected select the next colour as requested.          
    else: 
        CurrentRGBHeadlightColour = (CurrentRGBHeadlightColour + Selection)
        
    # Change headlights to the selected colour.     
    HeadlightController.RGBColorCycle(CommonConstants.HEADLIGHT_COLOURS[CurrentRGBHeadlightColour])
    # Return back to the ControllerRoutines function.
    return   

       
# This function creates a digital 4-speed PWM rear wheel drive transmission and disables the front
# two motors so that the AxiosRoboticsRCv1 unit can perform a variable speed standing burnout.  
def RearWheelDriveBurnout(RightTriggerVal):
    # Return back to the ControllerRoutines function if the accelerate trigger is not depressed.
    if(RightTriggerVal <= CommonConstants.TRIGGER_DEADZONE):
        # Stop all motors.
        MotorController.StopMotors()
        return
    
    # First gear 25% throttle.
    elif(RightTriggerVal > CommonConstants.TRIGGER_DEADZONE) and (RightTriggerVal <= CommonConstants.TRIGGER_QTR_PRESSED):
        MotorController.Burnout(CommonConstants.ONE_QTR_SPEED, CommonConstants.DEFAULT_ACTION_DURATION)
    # Second gear 50% throttle.
    elif (RightTriggerVal > CommonConstants.TRIGGER_QTR_PRESSED) and (RightTriggerVal <= CommonConstants.TRIGGER_HALF_PRESSED):
        MotorController.Burnout(CommonConstants.HALF_SPEED, CommonConstants.DEFAULT_ACTION_DURATION)
    # Third gear 75% throttle.
    elif (RightTriggerVal > CommonConstants.TRIGGER_HALF_PRESSED) and (RightTriggerVal <= CommonConstants.TRIGGER_THREE_QTR_PRESSED):
        MotorController.Burnout(CommonConstants.THREE_QTR_SPEED, CommonConstants.DEFAULT_ACTION_DURATION)
    # Fourth gear full throttle.
    elif (RightTriggerVal > CommonConstants.TRIGGER_THREE_QTR_PRESSED):
        MotorController.Burnout(CommonConstants.FULL_SPEED, CommonConstants.DEFAULT_ACTION_DURATION)
    # Return back to the ControllerRoutines function.
    return     


# Constant speed modifier definition.
FRONT_MOTOR_CRAWL_SPEED: Final[int] = 7


# This function creates a digital 4-speed PWM rear wheel drive transmission and reduces the front
# two motors to a crawling speed so that the AxiosRoboticsRCv1 unit can perform a rolling burnout,
# moving forward slowly while the rear wheels have 4-speed independent control.
# This function is an easter egg which is activated by pressing the Xbox logo button on the 360 controller.
def RollingBurnoutMode(RightTriggerVal):
     # Return back to the ControllerRoutines function if the accelerate trigger is not depressed.
    if(RightTriggerVal <= CommonConstants.TRIGGER_DEADZONE):
        # Stop all motors.
        MotorController.StopMotors()
        return
    
    # First gear 25% throttle.
    if (RightTriggerVal > CommonConstants.TRIGGER_DEADZONE) and (RightTriggerVal <= CommonConstants.TRIGGER_QTR_PRESSED):
        MotorController.RollingBurnout(FRONT_MOTOR_CRAWL_SPEED, CommonConstants.ONE_QTR_SPEED, CommonConstants.DEFAULT_ACTION_DURATION)
    # Second gear 50% throttle.
    elif (RightTriggerVal > CommonConstants.TRIGGER_QTR_PRESSED) and (RightTriggerVal <= CommonConstants.TRIGGER_HALF_PRESSED):
        MotorController.RollingBurnout(FRONT_MOTOR_CRAWL_SPEED, CommonConstants.HALF_SPEED, CommonConstants.DEFAULT_ACTION_DURATION)
    # Third gear 75% throttle.    
    elif (RightTriggerVal > CommonConstants.TRIGGER_HALF_PRESSED) and (RightTriggerVal <= CommonConstants.TRIGGER_THREE_QTR_PRESSED):
        MotorController.RollingBurnout(FRONT_MOTOR_CRAWL_SPEED, CommonConstants.THREE_QTR_SPEED, CommonConstants.DEFAULT_ACTION_DURATION)
    # Fourth gear full throttle.    
    elif (RightTriggerVal > CommonConstants.TRIGGER_THREE_QTR_PRESSED):
        MotorController.RollingBurnout(FRONT_MOTOR_CRAWL_SPEED, CommonConstants.FULL_SPEED, CommonConstants.DEFAULT_ACTION_DURATION)
    # Return back to the ControllerRoutines function.
    return      


# This is the default driving mode for the AxiosRoboticsRCv1 unit, this creates a 2-speed high/low gear transmission.
def TwoSpeedAWDMode(RightTriggerVal):
    # Return back to the ControllerRoutines function if the accelerate trigger is not depressed.
    if(RightTriggerVal <= CommonConstants.TRIGGER_DEADZONE):
        # Stop all motors.
        MotorController.StopMotors()
        return
      
    # 2-speed all wheel drive mode.
    # Low gear 30% throttle.
    if (RightTriggerVal > CommonConstants.TRIGGER_DEADZONE) and (RightTriggerVal <= CommonConstants.TRIGGER_HALF_PRESSED):
        MotorController.DriveForward(30, CommonConstants.DEFAULT_ACTION_DURATION)
    # High gear full throttle.    
    elif (RightTriggerVal > CommonConstants.TRIGGER_HALF_PRESSED):
            MotorController.DriveForward(CommonConstants.FULL_SPEED, CommonConstants.DEFAULT_ACTION_DURATION)       


# This function performs a graceful clean up and shutdown of the AxiosRobtoticsRCv1 unit.         
def CleanUpAndPowerDown(CameraModuleUsed, Controller):
    # Run the clean up tasks for the camera controller if it was used during operation.
    if (CameraModuleUsed):
        CameraController.ServerCleanUp()   
         
    # Turn off the RGB headlight module.
    HeadlightController.LEDOff()
    # Turn off the tail light module.
    TaillightController.BrakeLightsOff()
    TaillightController.IndicatorLightsOff()
    # Perform GPIO pin cleanup.
    GPIO.cleanup()
    # Kill the controller API background processes.       
    Controller.close()          
    # Shutdown the pi zero motherboard.
    # system('systemctl poweroff')
    # Wait for the shutdown to commence.        
    sleep(3)

    
# This function maps the controllers right joystick to the pivot functionality of the AxiosRobtoticsRCv1 unit.    
def PivotRoutine(RightStickXPos):
    # Right thumbstick x-axis controls the left and right pivoting functionality, which supports 50% and 
    # 100% speed depending on how far the thumbstick is moved in either direction.
    # Pivot left at half speed.    
    if (RightStickXPos <= -CommonConstants.RIGHT_JOYSTICK_DEADZONE) and (RightStickXPos >= -CommonConstants.RIGHT_JOYSTICK_HALFPOS):
        MotorController.PivotLeft(CommonConstants.HALF_SPEED, CommonConstants.DEFAULT_ACTION_DURATION)
    # Pivot left at full speed.
    elif (RightStickXPos <= -CommonConstants.RIGHT_JOYSTICK_HALFPOS):
        MotorController.PivotLeft(CommonConstants.FULL_SPEED, CommonConstants.DEFAULT_ACTION_DURATION)
    # Pivot right at half speed.
    elif (RightStickXPos >= CommonConstants.RIGHT_JOYSTICK_DEADZONE) and (RightStickXPos <= CommonConstants.RIGHT_JOYSTICK_HALFPOS):
        MotorController.PivotRight(CommonConstants.HALF_SPEED, CommonConstants.DEFAULT_ACTION_DURATION)
        # Pivot right at full speed.
    elif (RightStickXPos > CommonConstants.RIGHT_JOYSTICK_HALFPOS):
        MotorController.PivotRight(CommonConstants.FULL_SPEED, CommonConstants.DEFAULT_ACTION_DURATION) 
    # Return back to the ControllerRoutines function.
    return    
        
