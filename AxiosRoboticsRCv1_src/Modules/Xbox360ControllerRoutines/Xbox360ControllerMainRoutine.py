#!/usr/bin/env python3

import RPi.GPIO as GPIO


from time import sleep


from Modules.Xbox360ControllerRoutines import Xbox360ControllerAPI
from Modules.Xbox360ControllerRoutines import Xbox360ControllerDebouncer

from Modules.CameraSubsystem import CameraController
from Modules.LedSubsystem import HeadlightController
from Modules.MotorSubsystem import MotorController
from Modules.SensorSubsystem import SmartSensorRoutines
from Modules.CommonConstantLib import CommonConstants
from Modules.Xbox360ControllerRoutines import Xbox360ControllerRoutines

# Initialize the controller object.
Controller = Xbox360ControllerAPI.Joystick()

ControllerDebouncer = Xbox360ControllerDebouncer.Debouncer(Controller)

global RGBHeadLightOn

def StartControllerRoutine():
    
    global RGBHeadLightOn

    CameraModuleUsed = False
    CollisionAvoidanceOn = False
    RollingBurnoutModeEnabled = False
    RearWheelDriveBurnoutEnabled = False
    TwoSpeedModeEnabled = True
    SelfDrivingAIActive = False
    
    # Turn on the RGB headlights at their currently set default colour.
    HeadlightController.RGBColorCycle(CommonConstants.DEFAULTHEADLIGHTCOLOUR)
    RGBHeadLightOn = True
    
    while True:
        
        ControllerDebouncer.CheckForButtonRelease()
        
        if (not RollingBurnoutModeEnabled) and (not RearWheelDriveBurnoutEnabled) and (not TwoSpeedModeEnabled):
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
        
            Xbox360ControllerRoutines.CleanUpAndPowerDown(CameraModuleUsed,Controller)
            
        
        elif Controller.B() and (not ControllerDebouncer.ButtonBPressed):
            
            
            ControllerDebouncer.SetButtonBPressed()
            
            EmergencyStopActive = True
    
            while (EmergencyStopActive):
            
                MotorController.StopMotors()
                
                if(not Controller.B()):
                    EmergencyStopActive = False
              
                  
        # Start button starts the live video feed from the camera controller.
        elif Controller.Start() and (not ControllerDebouncer.ButtonStartPressed):
            
            ControllerDebouncer.SetButtonStartPressed()
       
            if(not CameraModuleUsed):
                CameraModuleUsed = True
                
            CameraController.VideoStreamStart()
            
        # Y button powers on/off the front ultrasonic distance sensor module and,
        # enables/disables dual collision avoidance. 
        
        elif Controller.leftBumper() and (not ControllerDebouncer.ButtonLBPressed):
            
            ControllerDebouncer.SetButtonLBPressed()
        
            # Turn on collision avoidance.
            if (not CollisionAvoidanceOn):
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
                
        # Left bumper activates the self driving mode.
        elif (Controller.rightBumper() and CollisionAvoidanceOn) and (not ControllerDebouncer.ButtonRBPressed):
            
            ControllerDebouncer.SetButtonRBPressed()
                          
          # RGB Headlight Dpad Integration
        elif Controller.dpadUp() and (not ControllerDebouncer.DpadUpPressed):
            
            ControllerDebouncer.SetButtonDpadUpPressed()
            
            if (not RGBHeadLightOn):
                Xbox360ControllerRoutines.RGBHeadLightDPadRoutine(CommonConstants.LEDON, )
            elif RGBHeadLightOn:
                Xbox360ControllerRoutines.RGBHeadLightDPadRoutine(CommonConstants.LEDOFF)   
        # Cycle Back Through colours
        elif Controller.dpadLeft() and (not ControllerDebouncer.DpadLeftPressed):
            
            ControllerDebouncer.SetButtonDpadLeftPressed()
           
            Xbox360ControllerRoutines.RGBHeadLightDPadRoutine(CommonConstants.PREVCOLOUR)
            
        # Cycle Forward Through colours
        elif Controller.dpadRight() and (not ControllerDebouncer.DpadRightPressed):
            
            ControllerDebouncer.SetButtonDpadRightPressed()
      
            Xbox360ControllerRoutines.RGBHeadLightDPadRoutine(CommonConstants.NEXTCOLOUR)
                       
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
                    
                    
        # Collision avoidance checks.
        elif CollisionAvoidanceOn:
            # Prevent Collision Detected By Left Sensor.
            if(GPIO.input(LeftalrtReg) == 1):
                SmartSensorRoutines.AvoidCollision("LEFT")        
            # Prevent Collision Detected By Right Sensor
            elif (GPIO.input(RightalrtReg) == 1):
                SmartSensorRoutines.AvoidCollision("RIGHT")             
                    
        # Thumbstick mapping logic.
        # Left thumbstick x-axis controls the left and right turn functionality.
        # Turn left.
        elif LeftStickXPos < -CommonConstants.LEFTJOYSTICKDEADZONE:
            MotorController.TurnLeft(CommonConstants.FULLSPEED, CommonConstants.DEFAULTACTIONSPEED)
            # fwd(0.01)
        # Turn right.    
        elif LeftStickXPos > CommonConstants.LEFTJOYSTICKDEADZONE:
            MotorController.TurnRight(CommonConstants.FULLSPEED, CommonConstants.DEFAULTACTIONSPEED)
            # fwd(0.01)
            
        
        elif (RightStickXPos <= -CommonConstants.RIGHTJOYSTICKDEADZONE) or (RightStickXPos >= CommonConstants.RIGHTJOYSTICKDEADZONE):
            Xbox360ControllerRoutines.PivotRoutine(RightStickXPos)    
     
     
     
        # Right brake/reverse trigger logic.        
        # Reverse 2-speed
        elif (LeftTrigger > CommonConstants.TRIGGERDEADZONE) and (LeftTrigger <= CommonConstants.TRIGGERHALFPRESSED):
            MotorController.DriveBackwards(CommonConstants.LOWGEARSPEED, CommonConstants.DEFAULTACTIONSPEED)
        
        elif (LeftTrigger > CommonConstants.TRIGGERHALFPRESSED):
            MotorController.DriveBackwards(CommonConstants.FULLSPEED, CommonConstants.DEFAULTACTIONSPEED)
                            
        # Trigger mapping logic.
        # Left accelerate trigger logic.
        # Check for special drive mode overrides first. 
        # 4-Speed Rear Wheel Drive Mode.
        elif RearWheelDriveBurnoutEnabled:
            Xbox360ControllerRoutines.RearWheelDriveBurnout(RightTrigger)            
        # 4-speed rolling burnout easter egg drive mode.        
        elif RollingBurnoutModeEnabled:
            Xbox360ControllerRoutines.RollingBurnoutMode(RightTrigger)
            
        # 2-speed all wheel drive mode.
        # Low gear 30% throttle.
        elif TwoSpeedModeEnabled:
            Xbox360ControllerRoutines.TwoSpeedAWDMode(RightTrigger)
        