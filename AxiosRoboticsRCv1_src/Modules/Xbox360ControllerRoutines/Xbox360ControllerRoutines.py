#!/usr/bin/env python3
import os 
from typing import Final
from time import sleep
from Modules.Xbox360ControllerRoutines import Xbox360ControllerAPI
from Modules.Xbox360ControllerRoutines import Xbox360ControllerDebouncer
from Modules.CameraSubsystem import CameraController
from Modules.LedSubsystem import HeadlightController
from Modules.LedSubsystem import TailLightController
from Modules.MotorSubsystem import MotorController


import pydevd

# Initialize the controller object.
Controller = Xbox360ControllerAPI.Joystick()

LEFTJOYSTICKDEADZONE: Final[float] = 0.4
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

# Global state flag variables.
CameraModuleUsed = False
CollisionAvoidanceOn = False
RollingBurnoutModeEnabled = False
RearWheelDriveBurnoutEnabled = False
TwoSpeedModeEnabled = False
SelfDrivingAIActive = False


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
        CurrentRGBHeadlightColourSelected = HEADLIGHTCOLOURSLENGTH-1    
        
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


# This function stops the current drive trajectory when a collision is detected,
# stops the AxiosRobtocisRCv1 unit in its tracks. Alerts the operator which side the potential
# collision was detected on via the indicator LED and reverses the unit to create space
# between the unit and the object that was detected. At this point the user can regain control
# of the unit and can decide how to best proceed.
def AvoidCollision(side):
    # Stop all motors.
    MotorController.StopMotors()
    # Turn on the respective indicator to show which side the obstacle was detected on.
    TailLightController.IndicatorLightsOn(100, side)
    # Drive backwards for 0.3 seconds to avoid obstacle.
    MotorController.DriveBackwards(100, 0.3)
    # Turn off indicator after this routine has finished.
    TailLightController.IndicatorLightsOff(side)
    # Return back to the ControllerRoutines function.
    return 


# This function is used by the self driving AI routine, this is called when entrapment has been detected,
# this is designed to allow the AxiosRoboticsRCv1 unit to navigate itself out of a corner or crowded space.
def AvoidEntrapment(side):
    # Stop all motors.
    MotorController.StopMotors()
    # Turn on the respective indicator to show which side the obstacle was detected on.
    TailLightController.IndicatorLightsOn(100, side)
    # Drive backwards for 0.4 seconds to avoid obstacle.
    MotorController.DriveBackwards(100, 0.4)
    # Turn off indicator after this routine has finished.
    TailLightController.IndicatorLightsOff(side)
    # Turn 90 degrees and continue
    if(side == "LEFT"):
        MotorController.PivotLeft(100, 0.6)
    elif(side == "RIGHT"):
        MotorController.PivotRight(100, 0.6)
     # Return back to the ControllerRoutines function.
    return 


def AvoidObstacle(side):
    # Stop all motors.
    MotorController.StopMotors()
    # Turn on the respective indicator to show which side the obstacle was detected on.
    TailLightController.IndicatorLightsOn(100, side)
    # Drive backwards for 0.3 seconds to avoid obstacle.
    MotorController.DriveBackwards(50, 0.5)
    # Turn off indicator after this routine has finished.
    TailLightController.IndicatorLightsOff(side)
      # Turn briefly and continue
    if(side == "LEFT"):
        MotorController.TurnLeft(100, 0.6)
    elif(side == "RIGHT"):
        MotorController.TurnRight(100, 0.6)
    # Return back to the ControllerRoutines function.
    return 


# The AxiosRoboticsRCv1 unit will enter an infinite loop and will drive around,
# endlessly avoiding collisions and entrapment in corners.
def SelfDrivingAI():
    global SelfDrivingAIActive
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
        # If entrapment is detected by reverse and turn to navigate out of the corner.
        # Entrapment by left side.    
        elif (LeftSensorDetectionCount == DETECTIONSUNTILENTRAPMENT):
            AvoidEntrapment("LEFT")
            LeftSensorDetectionCount = 0
         # Entrapment by right side.       
        elif (RightSensorDetectionCount == DETECTIONSUNTILENTRAPMENT):
            AvoidEntrapment("RIGHT")
            RightSensorDetectionCount = 0 
        # Avoid all obstacles.    
        # Object detected on left side avoid obstacle.    
        elif (GPIO.input(LeftalrtAI) == 1):
            AvoidObstacle("LEFT")
            LeftSensorDetectionCount += 1
        # Object detected on right side avoid obstacle.    
        elif (GPIO.input(RightalrtAI) == 1):
            AvoidObstacle("RIGHT")
            RightSensorDetectionCount += 1   
        # Drive forwards at full speed if no objects are detected.    
        else:
            MotorController.DriveForwards(100, 0.1)
    # Return back to the ControllerRoutines function.
    return 

ControllerDebouncer = Xbox360ControllerDebouncer.Debouncer(Controller)
   
def StartControllerRoutines():
    # Global variable linkage.
    global CameraModuleUsed
    global CollisionAvoidanceOn
    global RollingBurnoutModeEnabled
    global RearWheelDriveBurnoutEnabled
    global SelfDrivingAIActive
    global TwoSpeedModeEnabled
    
    while True:
        
        ControllerDebouncer.CheckForButtonRelease()
        
        if (not RollingBurnoutModeEnabled) and (not RearWheelDriveBurnoutEnabled):
            TwoSpeedModeEnabled = True
            
        # Live left and right trigger position values.
        LeftTrigger = Controller.leftTrigger()
        RightTrigger = Controller.rightTrigger()
        # Live joystick X position values.
        LeftStickXPos = Controller.leftStick()[0]
        RightStickXPos = Controller.rightStick()[0]
        
        # Button action mapping tree.
        # Back button shuts down the unit.
        if Controller.Back() and (not ControllerDebouncer.ButtonBackPressed):
            
            ControllerDebouncer.SetButtonBackPressed()
        
            # Run the clean up tasks for the camera controller.
            if CameraModuleUsed:
                CameraController.ServerCleanUp()    
            # Turn off the head light module.
            HeadlightController.LedOff()
            # Turn off the tail light module.
            TailLightController.BrakeLightsOff()
            TailLightController.IndicatorLightsOff()
            Controller.close()
            sleep(1)
            # Shutdown the pi zero motherboard.
            #call("sudo shutdown now", shell=True)
            
            
        # Start button starts the live video feed from the camera controller.
        elif Controller.Start() and (not ControllerDebouncer.ButtonStartPressed):
            
            ControllerDebouncer.SetButtonStartPressed()
       
            if(not CameraModuleUsed):
                CameraModuleUsed = True
                
            CameraController.VideoStreamStart()
            
        # Y button powers on/off the front ultrasonic distance sensor module and,
        # enables/disables dual collision avoidance. 
        elif Controller.Y() and (not ControllerDebouncer.ButtonYPressed):
            
            ControllerDebouncer.SetButtonYPressed()
        
            # Turn on collision avoidance.
            if not CollisionAvoidanceOn:
                CollisionAvoidanceOn = True
                # Turn On Sensor Managment Module
                GPIO.output(promini, True)
                time.sleep(1)
            # Turn off collision avoidance.    
            elif(CollisionAvoidanceOn): 
                CollisionAvoidanceOn = False  
                # Turn Off Sensor Managment Module
                GPIO.output(promini, False)
                time.sleep(1)
        
        # Collision avoidance checks.
        elif CollisionAvoidanceOn:
            # Prevent Collision Detected By Left Sensor.
            if(GPIO.input(LeftalrtReg) == 1):
                AvoidCollision("LEFT")        
            # Prevent Collision Detected By Right Sensor
            elif (GPIO.input(RightalrtReg) == 1):
                AvoidCollision("RIGHT")  

        # Guide button activates rolling burnout easter egg mode.
        elif Controller.Guide() and (not ControllerDebouncer.ButtonGuidePressed):
            
            ControllerDebouncer.SetButtonGuidePressed()
            
            if (not RearWheelDriveBurnoutEnabled):
                if (not RollingBurnoutModeEnabled):
                    RollingBurnoutModeEnabled = True
                elif RollingBurnoutModeEnabled:
                    RollingBurnoutModeEnabled = False
                
        # A button activates/deactivates the rear wheel drive 4-speed burnout mode.
        elif Controller.A() and (not ControllerDebouncer.ButtonAPressed):
            
            ControllerDebouncer.SetButtonAPressed()
            
            if (not RollingBurnoutModeEnabled):
                if not RearWheelDriveBurnoutEnabled:
                    RearWheelDriveBurnoutEnabled = True
                elif RearWheelDriveBurnoutEnabled:
                    RearWheelDriveBurnoutEnabled = False

        # Thumbstick mapping logic.
        # Left thumbstick x-axis controls the left and right turn functionality.
        # Turn left.
        elif LeftStickXPos < -LEFTJOYSTICKDEADZONE:
            MotorController.TurnLeft(100, 0.1)
            # fwd(0.01)
        # Turn right.    
        elif LeftStickXPos > LEFTJOYSTICKDEADZONE:
            MotorController.TurnRight(100, 0.1)
            # fwd(0.01)
            
        # Right thumbstick x-axis controls the left and right pivoting functionality,
        # which supports 50% and 100% speed depending on how far the thumbstick is turned
        # in either direction.
        # Pivot left at half speed.         
        elif (RightStickXPos >= -RIGHTJOYSTICKHALFPOS) and (RightStickXPos <= -RIGHTJOYSTICKDEADZONE):
            MotorController.PivotLeft(50, 0.1)
        # Pivot left at full speed.
        elif RightStickXPos <= -RIGHTJOYSTICKHALFPOS:
            MotorController.PivotLeft(100, 0.1)
         # Pivot right at half speed.
        elif (RightStickXPos >= RIGHTJOYSTICKDEADZONE) and (RightStickXPos <= RIGHTJOYSTICKHALFPOS):
          MotorController.PivotRight(50, 0.1)
        # Pivot right at full speed.
        elif RightStickXPos > RIGHTJOYSTICKHALFPOS:
            MotorController.PivotRight(100, 0.1) 
            
        # Trigger mapping logic.
        # Left accelerate trigger logic.
        # Check for special drive mode overrides first. 
        # 4-Speed Rear Wheel Drive Mode.
        elif RearWheelDriveBurnoutEnabled:
            RearWheelDriveBurnout(RightTrigger)            
        # 4-speed rolling burnout easter egg drive mode.        
        elif RollingBurnoutModeEnabled:
            RollingBurnoutMode(RightTrigger)
            
        # 2-speed all wheel drive mode.
        # Low gear 30% throttle.
        elif TwoSpeedModeEnabled and ((RightTrigger > TRIGGERDEADZONE) and (RightTrigger <= TRIGGERHALFPRESSED)):
            MotorController.DriveForward(30, 0.1)
        # High gear full throttle.    
        elif TwoSpeedModeEnabled and ((RightTrigger > TRIGGERHALFPRESSED)):
            MotorController.DriveForward(100, 0.1)
                
        # Right brake/reverse trigger logic.        
        # Reverse 2-speed
        elif (LeftTrigger > TRIGGERDEADZONE) and (LeftTrigger <= TRIGGERHALFPRESSED):
            MotorController.DriveBackwards(30, 0.1)
        
        elif (LeftTrigger > TRIGGERHALFPRESSED):
            MotorController.DriveBackwards(100, 0.1)
                         
        # Left bumper activates the self driving mode.
        elif (Controller.leftBumper() and CollisionAvoidanceOn) and (not ControllerDebouncer.ButtonLBPressed):
            
            ControllerDebouncer.SetButtonLBPressed()
            SelfDrivingAI()
            
        # RGB Headlight Dpad Integration
        elif Controller.dpadUp():
            if (not RGBHeadLightOn):
                RGBHeadLightDPadRoutine("ON")
            elif RGBHeadLightOn:
                RGBHeadLightDPadRoutine("OFF")   
        # Cycle Back Through colours
        elif Controller.dpadLeft():
            RGBHeadLightDPadRoutine("PREV")
        # Cycle Forward Through colours
        elif Controller.dpadRight():
            RGBHeadLightDPadRoutine("NEXT")
               
        # Default Case For No Current Input
        else:
            MotorController.StopMotors()
           
