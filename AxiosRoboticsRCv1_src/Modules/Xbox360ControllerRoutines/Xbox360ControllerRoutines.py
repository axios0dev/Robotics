#!/usr/bin/env python3
from os import call
from typing import Final
import xbox
from Modules.CameraSubsystem import CameraController
from Modules.LedSubsystem import HeadlightController
from Modules.LedSubsystem import TaillightController
from Modules.MotorSubystem import MotorController
# Initialize the controller object.
Controller = xbox.Joystick()

LEFTJOYSTICKDEADZONE: Final[float] = 0.4
RIGHTJOYSTICKDEADZONE: Final[float] = 0.2
RIGHTJOYSTICKHALFPOS: Final[float] = 0.6
TRIGGERDEADZONE: Final[float] = 0.1
TRIGGERQTRPRESSED: Final[float] = 0.25
TRIGGERHALFPRESSED: Final[float] = 0.50
TRIGGERTHREEQTRPRESSED: Final[float] = 0.75
TRIGGERFULLPRESSED: Final[int] = 1
DETECTIONSUNTILENTRAPMENT: Final[int] = 3

# Global state flag variables.
CameraModuleUsed = False
CollisionAvoidanceOn = False
RollingBurnoutModeEnabled = False
RearWheelDriveBurnoutEnabled = False
SelfDrivingAIActive = False


# This function stops the current drive trajectory when a collision is detected,
# stops the AxiosRobtocisRCv1 unit in its tracks. Alerts the operator which side the potential
# collision was detected on via the indicator LED and reverses the unit to create space
# between the unit and the object that was detected. At this point the user can regain control
# of the unit and can decide how to best proceed.
def AvoidCollision(side):
    # Stop all motors.
    MotorController.StopMotors()
    # Turn on left indicator to show which side the obstacle was detected on.
    TaillightController.IndicatorLightsOn(100, side)
    # Drive backwards for 0.3 seconds to avoid obstacle.
    MotorController.DriveBackwards(100, 0.3)
    # Turn off indicator after this routine has finished.
    TaillightController.IndicatorLightsOff(side)
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
        # If entrapment is detected by the left sensor, reverse and turn left to,
        # navigate out of the corner.    
        elif (LeftSensorDetectionCount == DETECTIONSUNTILENTRAPMENT):
            # Stop all motors.
            MotorController.StopMotors()
            # Turn on the left indicator to show which side the obstacle was detected on.
            TaillightController.IndicatorLightsOn(100, "LEFT")
            # Drive backwards for 0.4 seconds to avoid obstacle.
            MotorController.DriveBackwards(100, 0.4)
            # Turn left briefly and continue.
            MotorController.TurnLeft(100, 0.6)
            # Turn off indicator after this routine has finished.
            TaillightController.IndicatorLightsOff("LEFT")
            LeftSensorDetectionCount = 0
           
        # If entrapment is detected by the right sensor, reverse and turn right to,
        # navigate out of the corner.      
        elif (RightSensorDetectionCount == DETECTIONSUNTILENTRAPMENT):
            # Stop all motors.
            MotorController.StopMotors()
            # Turn on the right indicator to show which side the obstacle was detected on.
            TaillightController.IndicatorLightsOn(100, "RIGHT")
            # Drive backwards for 0.4 seconds to avoid obstacle.
            MotorController.DriveBackwards(100, 0.4)
            # Turn right briefly and continue.
            MotorController.TurnRight(100, 0.6)
            # Turn off indicator after this routine has finished.
            TaillightController.IndicatorLightsOff("RIGHT")
            RightSensorDetectionCount = 0
            
        # Object detected on left side, avoid obstacle.    
        elif GPIO.input(LeftalrtAI) == 1:
                        # Tail Light setup
                        leftbrake(100)
                        rightbrake(0)
                        leftind(100)
                        rightind(100)
                        # Movment Functions
                        frontspeed(50)
                        backspeed(50)
                        rightcount = 0
                        leftcount += 1
                        rev(0.5)
                        pivotleft(0.3)    
            
            
            
            
            
        elif GPIO.input(RightalrtAI) == 1:
            
            
            
            
            
            
            
                        # Tail Light setup
                        leftbrake(0)
                        rightbrake(100)
                        leftind(100)
                        rightind(100)
                        # Movment Functions
                        frontspeed(50)
                        backspeed(50)
                        leftcount = 0
                        rightcount += 1
                        rev(0.5)
                        pivotright(0.3)
                        
                        
                        
                  
                    else:
                        # Tail Light setup
                        leftbrake(0)
                        rightbrake(0)
                        leftind(0)
                        rightind(0)
                        # Movment Functions
                        frontspeed(100)
                        backspeed(100)
                        fwd(0.1)


def ControllerRoutines():
    # Global variable linkage.
    global CameraModuleUsed
    global CollisionAvoidanceOn
    global RollingBurnoutModeEnabled
    global RearWheelDriveBurnoutEnabled
    global SelfDrivingAIActive
    
    while True:
        # Live left and right trigger position values.
        LeftTrigger = Controller.LeftTriggerer()
        RightTrigger = Controller.rightTrigger()
        # Live joystick X position values.
        LeftStickXPos = Controller.leftStick()[0]
        RightStickXPos = Controller.rightStick()[0]
        
        # Button action mapping tree.
        # Back button shuts down the unit.
        if Controller.Back():
            # Run the clean up tasks for the camera controller.
            if CameraModuleUsed:
                CameraController.ServerCleanUp()    
            # Turn off the head light module.
            HeadlightController.LedOff()
            # Turn off the tail light module.
            TaillightController.BrakeLightsOff()
            TaillightController.IndicatorLightsOff()
            # Shutdown the pi zero motherboard.
            call("sudo nohup shutdown -h now", shell=True)
            
        # Start button starts the live video feed from the camera controller.
        elif Controller.Start():
            CameraModuleUsed = True
            CameraController.VideoStreamStart()
            
        # Y button powers on/off the front ultrasonic distance sensor module and,
        # enables/disables dual collision avoidance. 
        elif Controller.Y():
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
        # Prevent Collision Detected By Left Sensor.
        elif CollisionAvoidanceOn:
            if(GPIO.input(LeftalrtReg) == 1):
         
                    
            # Prevent Collision Detected By Right Sensor
            elif (GPIO.input(RightalrtReg) == 1):
                # Stop all motors.
                MotorController.StopMotors()
                # Turn on right indicator to show which side the obstacle was detected on.
                TaillightController.IndicatorLightsOn(100, "RIGHT")
                # Drive backwards for 0.3 seconds to avoid obstacle.
                MotorController.DriveBackwards(100, 0.3)
                # Turn off indicator after this routine has finished.
                TaillightController.IndicatorLightsOff("RIGHT")

        # Guide button activates rolling burnout easter egg mode.
        elif Controller.Guide():
            if not RollingBurnoutModeEnabled:
                RollingBurnoutModeEnabled = True
            elif RollingBurnoutModeEnabled:
                RollingBurnoutModeEnabled = False
                
        # A button activates/deactivates the rear wheel drive 4-speed burnout mode.
        elif Controller.A():
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
             # First gear 25% throttle.
            if(RightTrigger > TRIGGERDEADZONE) and (RightTrigger <= TRIGGERQTRPRESSED):
                MotorController.Burnout(0, 25, 0.1)
            # Second gear 50% throttle.
            elif (RightTrigger > TRIGGERQTRPRESSED) and (RightTrigger <= TRIGGERHALFPRESSED):
                MotorController.Burnout(0, 50, 0.1)
            # Third gear 75% throttle.
            elif (RightTrigger > TRIGGERHALFPRESSED) and (RightTrigger <= TRIGGERTHREEQTRPRESSED):
                MotorController.Burnout(0, 75, 0.1)
            # Fourth gear full throttle.
            elif (RightTrigger > TRIGGERTHREEQTRPRESSED):
                MotorController.Burnout(0, 100, 0.1)
                
        # 4-speed rolling burnout easter egg drive mode.        
        elif RollingBurnoutModeEnabled:
            # First gear 25% throttle.
            if (RightTrigger > TRIGGERDEADZONE) and (RightTrigger <= TRIGGERQTRPRESSED):
                MotorController.Burnout(4, 25, 0.1)
            # Second gear 50% throttle.
            elif (RightTrigger > TRIGGERQTRPRESSED) and (RightTrigger <= TRIGGERHALFPRESSED):
                MotorController.Burnout(4, 50, 0.1)
            # Third gear 75% throttle.    
            elif (RightTrigger > TRIGGERHALFPRESSED) and (RightTrigger <= TRIGGERTHREEQTRPRESSED):
                MotorController.Burnout(4, 75, 0.1)
            # Fourth gear full throttle.    
            elif (RightTrigger > TRIGGERTHREEQTRPRESSED):
                MotorController.Burnout(4, 75, 0.1)
        
        # 2-speed all wheel drive mode.
        elif (not RearWheelDriveBurnoutEnabled) and (not RollingBurnoutModeEnabled):
            # Low gear 30% throttle.
            if (RightTrigger > TRIGGERDEADZONE) and (RightTrigger <= TRIGGERHALFPRESSED):
                MotorController.DriveForward(30, 0.1)
            # High gear full throttle.    
            elif (RightTrigger > TRIGGERHALFPRESSED):
                MotorController.DriveForward(100, 0.1)
                 
        # Right brake/reverse trigger logic.        
        # Reverse 2-speed
        elif (LeftTrigger > TRIGGERDEADZONE) and (LeftTrigger <= TRIGGERHALFPRESSED):
                MotorController.DriveBackwards(30, 0.1)
        
        elif (LeftTrigger > TRIGGERHALFPRESSED):
            MotorController.DriveBackwards(100, 0.1)
                         
        # Left bumper activates the self driving mode.
        elif Controller.leftBumper() and CollisionAvoidanceOn:

        # RGB Headlight Dpad Integration
        elif Controller.dpadUp():
            if RGB == 0:
                RGB = 1
                select = 1
                RGBcolorcycle(select)
                time.sleep(1)
            elif RGB == 1:
                RGB = 0
                redLED("OFF")
                greenLED("OFF")
                blueLED("OFF")
                time.sleep(1)
                # Cycle Back Through colours
            elif Controller.dpadLeft():
                if select > 1:
                    select -= 1
                    RGBcolorcycle(select)
                    time.sleep(1)
                elif select == 1:
                    select = 8
                    RGBcolorcycle(select)
                    time.sleep(1)
            # Cycle Forward Through colours
            elif Controller.dpadRight():
                if select < 8:
                    select += 1
                    RGBcolorcycle(select)
                    time.sleep(1)
                elif select == 8:
                    select = 1
                    RGBcolorcycle(select)
                    time.sleep(1)
        # Default Case For No Current Input
        else:
            # Tail Light setup
            leftbrake(100)
            rightbrake(100)
            leftind(0)
            rightind(0)
            # Movment Functions
            stop(0.1)
