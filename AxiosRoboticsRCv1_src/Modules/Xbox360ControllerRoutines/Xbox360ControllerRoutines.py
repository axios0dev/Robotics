#!/usr/bin/env python3
# This module contains the Xbox 360 controller subroutines for the AxiosRoboticsRCv1 unit.

# Python library imports.
import RPi.GPIO as GPIO
from time import sleep
from os import system 
# AxiosRobtoticsRCv1 submodule and common library imports.
from Modules.CameraSubsystem import CameraController
from Modules.ConstLib import CommonConstants
from Modules.LedSubsystem import HeadlightController
from Modules.MotorSubsystem import MotorController
from Modules.LedSubsystem import TaillightController
from Modules.Xbox360ControllerRoutines import Xbox360ControllerAPI
from Modules.Xbox360ControllerRoutines import Xbox360ControllerMainRoutine

# This variable holds the index of the currently selected RGB headlight colour.
CurrentRGBHeadlightColour = CommonConstants.HEADLIGHTCOLOURS.index(CommonConstants.DEFAULTHEADLIGHTCOLOUR)


# This subroutine takes in a requested state for the RGB headlight modules and performs the requested action, 
# either turning the lights on/off or cycles through the colours. 
def RGBHeadlightDpadRoutine(NextState):
    # Current and next selection variables.
    global CurrentRGBHeadlightColour
    selection = None
    
    # Turn off the RGB headlights.
    if(NextState == CommonConstants.LEDOFF):
        HeadlightController.LedOff()
        Xbox360ControllerMainRoutine.RGBHeadLightOn = False
        # Return back to the ControllerRoutines function.
        return
    # Turn on the RGB headlights. 
    elif(NextState == CommonConstants.LEDON):
        Xbox360ControllerMainRoutine.RGBHeadLightOn = True
        HeadlightController.RGBColorCycle(CommonConstants.HEADLIGHTCOLOURS[CurrentRGBHeadlightColour])
        # Return back to the ControllerRoutines function.
        return   
    
    # Change the RGB headlights to the next available colour. 
    if(NextState == CommonConstants.NEXTCOLOUR):
        Selection = 1
    # Change the RGB headlights to the previous available colour.     
    elif(NextState == CommonConstants.PREVCOLOUR):
        Selection = -1 
         
    # Check if the selection is beyond the first colour avalible, then wrap around back to the last. 
    if((CurrentRGBHeadlightColour + Selection) < CommonConstants.FIRSTCOLOURIDX):
        CurrentRGBHeadlightColour = CommonConstants.LASTCOLOURIDX - 1    
    # Check if the selection is beyond the last colour avalible, then wrap around back to the first.    
    elif((CurrentRGBHeadlightColour + Selection) >= CommonConstants.LASTCOLOURIDX):
        CurrentRGBHeadlightColour = CommonConstants.FIRSTCOLOURIDX
    # If no wrap around is detected select the next colour as requested.          
    else: 
        CurrentRGBHeadlightColour = (CurrentRGBHeadlightColour + Selection)
        
    # Change headlights to the selected colour.     
    HeadlightController.RGBColorCycle(CommonConstants.HEADLIGHTCOLOURS[CurrentRGBHeadlightColour])
    # Return back to the ControllerRoutines function.
    return   

       
# This function creates a digital 4-speed PWM rear wheel drive transmission and disables the front
# two motors so that the AxiosRoboticsRCv1 unit can perform a variable speed standing burnout.  
def RearWheelDriveBurnout(RightTriggerVal):
    # Return back to the ControllerRoutines function if the accelerate trigger is not depressed.
    if(RightTriggerVal <= CommonConstants.TRIGGERDEADZONE):
        # Stop all motors.
        MotorController.StopMotors()
        return
    
    # First gear 25% throttle.
    elif(RightTriggerVal > CommonConstants.TRIGGERDEADZONE) and (RightTriggerVal <= CommonConstants.TRIGGERQTRPRESSED):
        MotorController.Burnout(CommonConstants.ONEQTRSPEED, CommonConstants.DEFAULTACTIONSPEED)
    # Second gear 50% throttle.
    elif (RightTriggerVal > CommonConstants.TRIGGERQTRPRESSED) and (RightTriggerVal <= CommonConstants.TRIGGERHALFPRESSED):
        MotorController.Burnout(CommonConstants.HALFSPEED, CommonConstants.DEFAULTACTIONSPEED)
    # Third gear 75% throttle.
    elif (RightTriggerVal > CommonConstants.TRIGGERHALFPRESSED) and (RightTriggerVal <= CommonConstants.TRIGGERTHREEQTRPRESSED):
        MotorController.Burnout(CommonConstants.THREEQTRSPEED, CommonConstants.DEFAULTACTIONSPEED)
    # Fourth gear full throttle.
    elif (RightTriggerVal > CommonConstants.TRIGGERTHREEQTRPRESSED):
        MotorController.Burnout(CommonConstants.FULLSPEED, CommonConstants.DEFAULTACTIONSPEED)
    # Return back to the ControllerRoutines function.
    return     


# This function creates a digital 4-speed PWM rear wheel drive transmission and reduces the front
# two motors to a crawling speed so that the AxiosRoboticsRCv1 unit can perform a rolling burnout,
# moving forward slowly while the rear wheels have 4-speed independent control.
# This function is an easter egg which is activated by pressing the Xbox logo button on the 360 controller.
def RollingBurnoutMode(RightTriggerVal):
     # Return back to the ControllerRoutines function if the accelerate trigger is not depressed.
    if(RightTriggerVal <= CommonConstants.TRIGGERDEADZONE):
        # Stop all motors.
        MotorController.StopMotors()
        return
    
    # First gear 25% throttle.
    if (RightTriggerVal > CommonConstants.TRIGGERDEADZONE) and (RightTriggerVal <= CommonConstants.TRIGGERQTRPRESSED):
        MotorController.RollingBurnout(CommonConstants.FRONTMOTORCRAWLSPEED, CommonConstants.ONEQTRSPEED, CommonConstants.DEFAULTACTIONSPEED)
    # Second gear 50% throttle.
    elif (RightTriggerVal > CommonConstants.TRIGGERQTRPRESSED) and (RightTriggerVal <= CommonConstants.TRIGGERHALFPRESSED):
        MotorController.RollingBurnout(CommonConstants.FRONTMOTORCRAWLSPEED, CommonConstants.HALFSPEED, CommonConstants.DEFAULTACTIONSPEED)
    # Third gear 75% throttle.    
    elif (RightTriggerVal > CommonConstants.TRIGGERHALFPRESSED) and (RightTriggerVal <= CommonConstants.TRIGGERTHREEQTRPRESSED):
        MotorController.RollingBurnout(CommonConstants.FRONTMOTORCRAWLSPEED, CommonConstants.THREEQTRSPEED, CommonConstants.DEFAULTACTIONSPEED)
    # Fourth gear full throttle.    
    elif (RightTriggerVal > CommonConstants.TRIGGERTHREEQTRPRESSED):
        MotorController.RollingBurnout(CommonConstants.FRONTMOTORCRAWLSPEED, CommonConstants.FULLSPEED, CommonConstants.DEFAULTACTIONSPEED)
    # Return back to the ControllerRoutines function.
    return      


# This is the default driving mode for the AxiosRoboticsRCv1 unit, this creates a 2-speed high/low gear transmission.
def TwoSpeedAWDMode(RightTriggerVal):
    # Return back to the ControllerRoutines function if the accelerate trigger is not depressed.
    if(RightTriggerVal <= CommonConstants.TRIGGERDEADZONE):
        # Stop all motors.
        MotorController.StopMotors()
        return
      
    # 2-speed all wheel drive mode.
    # Low gear 30% throttle.
    if (RightTriggerVal > CommonConstants.TRIGGERDEADZONE) and (RightTriggerVal <= CommonConstants.TRIGGERHALFPRESSED):
        MotorController.DriveForward(30, CommonConstants.DEFAULTACTIONSPEED)
    # High gear full throttle.    
    elif (RightTriggerVal > CommonConstants.TRIGGERHALFPRESSED):
            MotorController.DriveForward(CommonConstants.FULLSPEED, CommonConstants.DEFAULTACTIONSPEED)       


# This function performs a graceful clean up and shutdown of the AxiosRobtoticsRCv1 unit.         
def CleanUpAndPowerDown(CameraModuleUsed, Controller):
    # Run the clean up tasks for the camera controller if it was used during operation.
    if (CameraModuleUsed):
        CameraController.ServerCleanUp()   
         
    # Turn off the RGB headlight module.
    HeadlightController.LedOff()
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
    if (RightStickXPos <= -CommonConstants.RIGHTJOYSTICKDEADZONE) and (RightStickXPos >= -CommonConstants.RIGHTJOYSTICKHALFPOS):
        MotorController.PivotLeft(CommonConstants.HALFSPEED, CommonConstants.DEFAULTACTIONSPEED)
    # Pivot left at full speed.
    elif (RightStickXPos <= -CommonConstants.RIGHTJOYSTICKHALFPOS):
        MotorController.PivotLeft(CommonConstants.FULLSPEED, CommonConstants.DEFAULTACTIONSPEED)
    # Pivot right at half speed.
    elif (RightStickXPos >= CommonConstants.RIGHTJOYSTICKDEADZONE) and (RightStickXPos <= CommonConstants.RIGHTJOYSTICKHALFPOS):
        MotorController.PivotRight(CommonConstants.HALFSPEED, CommonConstants.DEFAULTACTIONSPEED)
        # Pivot right at full speed.
    elif (RightStickXPos > CommonConstants.RIGHTJOYSTICKHALFPOS):
        MotorController.PivotRight(CommonConstants.FULLSPEED, CommonConstants.DEFAULTACTIONSPEED) 
    # Return back to the ControllerRoutines function.
    return    
        
