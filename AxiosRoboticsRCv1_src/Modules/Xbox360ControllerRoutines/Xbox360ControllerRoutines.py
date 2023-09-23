#!/usr/bin/env python3

import RPi.GPIO as GPIO
from os import system 
from typing import Final
from time import sleep


from Modules.CameraSubsystem import CameraController
from Modules.LedSubsystem import HeadlightController
from Modules.LedSubsystem import TailLightController
from Modules.MotorSubsystem import MotorController
from Modules.SensorSubsystem import SmartSensorRoutines



RIGHTJOYSTICKDEADZONE: Final[float] = 0.2
RIGHTJOYSTICKHALFPOS: Final[float] = 0.6
TRIGGERDEADZONE: Final[float] = 0.2
TRIGGERQTRPRESSED: Final[float] = 0.25
TRIGGERHALFPRESSED: Final[float] = 0.50
TRIGGERTHREEQTRPRESSED: Final[float] = 0.75
TRIGGERFULLPRESSED: Final[int] = 1


DETECTIONSUNTILENTRAPMENT: Final[int] = 3

HEADLIGHTCOLOURS: Final = ["RED", "GREEN", "BLUE", "YELLOW", "CYAN", "Magenta", "WHITE", "ORANGE"]
HEADLIGHTCOLOURSLENGTH: Final[int] = len(HEADLIGHTCOLOURS)

# Default headlight colour on startup.
DEFAULTHEADLIGHTCOLOUR: Final[str] = "CYAN"


CurrentRGBHeadlightColourSelected = HEADLIGHTCOLOURS.index(DEFAULTHEADLIGHTCOLOUR)
# Turn on the RGB headlights at their currently set default colour.
HeadlightController.RGBColorCycle(HEADLIGHTCOLOURS[CurrentRGBHeadlightColourSelected])
RGBHeadLightOn = True



def RGBHeadLightDPadRoutine(state):
    global RGBHeadLightOn
    global CurrentRGBHeadlightColourSelected
    
    if(state == "OFF"):
        HeadlightController.LedOff()
        RGBHeadLightOn = False
        # Return back to the ControllerRoutines function.
        return 
    elif(state == "ON"):
        RGBHeadLightOn = True
        HeadlightController.RGBColorCycle(HEADLIGHTCOLOURS[CurrentRGBHeadlightColourSelected])
        # Return back to the ControllerRoutines function.
        return   
    
    if(state == "NEXT"):
        Selection = 1
    elif(state == "PREV"):
        Selection = -1 
         
    if((CurrentRGBHeadlightColourSelected + Selection) < 0):
        CurrentRGBHeadlightColourSelected = HEADLIGHTCOLOURSLENGTH - 1    
        
    # Check if the selection is beyond the last colour avalible, then wrap around back to the first.    
    elif((CurrentRGBHeadlightColourSelected + Selection) >= HEADLIGHTCOLOURSLENGTH):
        CurrentRGBHeadlightColourSelected = 0
              
    else: 
        CurrentRGBHeadlightColourSelected = (CurrentRGBHeadlightColourSelected + Selection)
        
    print("new colour")
    print(HEADLIGHTCOLOURS[CurrentRGBHeadlightColourSelected])
        
    HeadlightController.RGBColorCycle(HEADLIGHTCOLOURS[CurrentRGBHeadlightColourSelected])
    # Return back to the ControllerRoutines function.
    return   

       
# This function creates digital 4-speed PWM rear wheel drive transmission and disables the front
# two motors so that the AxiosRoboticsRCv1 unit can perform a variable speed standing
# burnout.  
def RearWheelDriveBurnout(RightTriggerVal):
    # Return back to the ControllerRoutines function if the accelerate trigger is not depressed.
    if(RightTriggerVal <= TRIGGERDEADZONE):
        # Stop all motors.
        MotorController.StopMotors()
        return
    
    # First gear 25% throttle.
    elif(RightTriggerVal > TRIGGERDEADZONE) and (RightTriggerVal <= TRIGGERQTRPRESSED):
        MotorController.Burnout(25, 0.1)
    # Second gear 50% throttle.
    elif (RightTriggerVal > TRIGGERQTRPRESSED) and (RightTriggerVal <= TRIGGERHALFPRESSED):
        MotorController.Burnout(50, 0.1)
    # Third gear 75% throttle.
    elif (RightTriggerVal > TRIGGERHALFPRESSED) and (RightTriggerVal <= TRIGGERTHREEQTRPRESSED):
        MotorController.Burnout(75, 0.1)
    # Fourth gear full throttle.
    elif (RightTriggerVal > TRIGGERTHREEQTRPRESSED):
        MotorController.Burnout(100, 0.1)
    # Return back to the ControllerRoutines function.
    return     


FRONTMOTORCRAWLSPEED: Final[int] = 7


# This function creates digital 4-speed PWM rear wheel drive transmission and reduces the front
# two motors to a crawling speed so that the AxiosRoboticsRCv1 unit can perform a rolling burnout
# moving forward slowly while the rear wheels have 4-speed independent control.
# This function is an easter egg which is activated by pressing the Xbox logo button on the 360 controller.
def RollingBurnoutMode(RightTriggerVal):
    
     # Return back to the ControllerRoutines function if the accelerate trigger is not depressed.
    if(RightTriggerVal <= TRIGGERDEADZONE):
        # Stop all motors.
        MotorController.StopMotors()
        return
    
    # First gear 25% throttle.
    if (RightTriggerVal > TRIGGERDEADZONE) and (RightTriggerVal <= TRIGGERQTRPRESSED):
        MotorController.RollingBurnout(FRONTMOTORCRAWLSPEED, 25, 0.1)
    # Second gear 50% throttle.
    elif (RightTriggerVal > TRIGGERQTRPRESSED) and (RightTriggerVal <= TRIGGERHALFPRESSED):
        MotorController.RollingBurnout(FRONTMOTORCRAWLSPEED, 50, 0.1)
    # Third gear 75% throttle.    
    elif (RightTriggerVal > TRIGGERHALFPRESSED) and (RightTriggerVal <= TRIGGERTHREEQTRPRESSED):
        MotorController.RollingBurnout(FRONTMOTORCRAWLSPEED, 75, 0.1)
    # Fourth gear full throttle.    
    elif (RightTriggerVal > TRIGGERTHREEQTRPRESSED):
        MotorController.RollingBurnout(FRONTMOTORCRAWLSPEED, 100, 0.1)
    # Return back to the ControllerRoutines function.
    return      



def TwoSpeedAWDMode(RightTriggerVal):
    # Return back to the ControllerRoutines function if the accelerate trigger is not depressed.
    if(RightTriggerVal <= TRIGGERDEADZONE):
        # Stop all motors.
        MotorController.StopMotors()
        return
      
    # 2-speed all wheel drive mode.
    # Low gear 30% throttle.
    if (RightTriggerVal > TRIGGERDEADZONE) and (RightTriggerVal <= TRIGGERHALFPRESSED):
        MotorController.DriveForward(30, 0.1)
    # High gear full throttle.    
    elif (RightTriggerVal > TRIGGERHALFPRESSED):
            MotorController.DriveForward(100, 0.1)       
            
def CleanUpAndPowerDown(CameraModuleUsed):
    
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
    if (RightStickXPos <= -RIGHTJOYSTICKDEADZONE) and (RightStickXPos >= -RIGHTJOYSTICKHALFPOS):
        MotorController.PivotLeft(50, 0.1)
    # Pivot left at full speed.
    elif (RightStickXPos <= -RIGHTJOYSTICKHALFPOS):
        MotorController.PivotLeft(100, 0.1)
    # Pivot right at half speed.
    elif (RightStickXPos >= RIGHTJOYSTICKDEADZONE) and (RightStickXPos <= RIGHTJOYSTICKHALFPOS):
        MotorController.PivotRight(50, 0.1)
        # Pivot right at full speed.
    elif (RightStickXPos > RIGHTJOYSTICKHALFPOS):
        MotorController.PivotRight(100, 0.1) 
     
    return    
        