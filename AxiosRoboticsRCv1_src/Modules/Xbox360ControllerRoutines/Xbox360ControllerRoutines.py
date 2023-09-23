#!/usr/bin/env python3

import RPi.GPIO as GPIO
from os import system 
from typing import Final
from time import sleep


from Modules.CameraSubsystem import CameraController
from Modules.LedSubsystem import HeadlightController
from Modules.LedSubsystem import TailLightController
from Modules.MotorSubsystem import MotorController
from Modules.ConstLib import CommonConstants
from Modules.Xbox360ControllerRoutines import Xbox360ControllerMainRoutine
from Modules.Xbox360ControllerRoutines import Xbox360ControllerAPI


CurrentRGBHeadlightColour =  CommonConstants.HEADLIGHTCOLOURS.index(CommonConstants.DEFAULTHEADLIGHTCOLOUR)

def RGBHeadLightDPadRoutine(NextState):
    global CurrentRGBHeadlightColour
    selection = None
    
    if(NextState == CommonConstants.LEDOFF):
        HeadlightController.LedOff()
        Xbox360ControllerMainRoutine.RGBHeadLightOn = False
        # Return back to the ControllerRoutines function.
        return 
    elif(NextState == CommonConstants.LEDON):
        Xbox360ControllerMainRoutine.RGBHeadLightOn = True
        HeadlightController.RGBColorCycle(CommonConstants.HEADLIGHTCOLOURS[CurrentRGBHeadlightColour])
        # Return back to the ControllerRoutines function.
        return   
    
    if(NextState == CommonConstants.NEXTCOLOUR):
        Selection = 1
    elif(NextState == CommonConstants.PREVCOLOUR):
        Selection = -1 
         
    if((CurrentRGBHeadlightColour + Selection) < CommonConstants.FIRSTCOLOURIDX):
        CurrentRGBHeadlightColour = CommonConstants.LASTCOLOURIDX - 1    
        
    # Check if the selection is beyond the last colour avalible, then wrap around back to the first.    
    elif((CurrentRGBHeadlightColour + Selection) >= CommonConstants.LASTCOLOURIDX):
        CurrentRGBHeadlightColour = CommonConstants.FIRSTCOLOURIDX
              
    else: 
        CurrentRGBHeadlightColour = (CurrentRGBHeadlightColour + Selection)
        
    print("new colour")
    print(CommonConstants.HEADLIGHTCOLOURS[CurrentRGBHeadlightColour])
        
    HeadlightController.RGBColorCycle(CommonConstants.HEADLIGHTCOLOURS[CurrentRGBHeadlightColour])
    # Return back to the ControllerRoutines function.
    return   

       
# This function creates digital 4-speed PWM rear wheel drive transmission and disables the front
# two motors so that the AxiosRoboticsRCv1 unit can perform a variable speed standing
# burnout.  
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


# This function creates digital 4-speed PWM rear wheel drive transmission and reduces the front
# two motors to a crawling speed so that the AxiosRoboticsRCv1 unit can perform a rolling burnout
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
            
def CleanUpAndPowerDown(CameraModuleUsed,Controller):
    
    CameraModuleUsed
    # Run the clean up tasks for the camera controller.
    if (CameraModuleUsed):
        CameraController.ServerCleanUp()   
         
    # Turn off the head light module.
    HeadlightController.LedOff()
    # Turn off the tail light module.
    TailLightController.BrakeLightsOff()
    TailLightController.IndicatorLightsOff()
    GPIO.cleanup()
            
    Controller.close()
                
    # Shutdown the pi zero motherboard.
    #system('systemctl poweroff')
      
    # Wait for the shutdown to commence.        
    sleep(3)
    
    
def PivotRoutine(RightStickXPos):
    # Right thumbstick x-axis controls the left and right pivoting functionality,
    # which supports 50% and 100% speed depending on how far the thumbstick is turned
    # in either direction.
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
     
    return    
        