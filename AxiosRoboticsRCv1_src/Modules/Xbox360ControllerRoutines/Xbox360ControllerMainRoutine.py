#!/usr/bin/env python3
# This module contains the main controller routine that calls the Xbox 360 controller sub
# routines and underlying functions that operate the entire AxiosRobtoticsRCv1 unit.

# AxiosRobtoticsRCv1 submodule and common library imports.
from Modules.CameraSubsystem import CameraController
from Modules.CommonConstantLib import CommonConstants
from Modules.LedSubsystem import HeadlightController
from Modules.MotorSubsystem import MotorController
from Modules.SensorSubsystem import SmartSensorRoutines
from Modules.Xbox360ControllerRoutines import Xbox360ControllerAPI
from Modules.Xbox360ControllerRoutines import Xbox360ControllerDebouncer
from Modules.Xbox360ControllerRoutines import Xbox360ControllerRoutines

# Construct and initialise the Xbox 360 controller object, this will poll live readings of
# the button and joystick states for the Xbox controller.
Controller = Xbox360ControllerAPI.Joystick()
# Construct an Xbox 360 controller debouncer object which will be used to keep track of held
# button states to limit the actions called from each button press.
ControllerDebouncer = Xbox360ControllerDebouncer.Debouncer(Controller)
# This global variable is used to keep track of when the RGB LEDs are on, this is also used by
# the Xbox 360 controller sub routines to assess the LED state.
global RGBHeadLightOn

# This function starts the main controller routine, once started the AxiosRoboticsRCv1 unit is
# considered online and active. To shutdown the unit the back button on the Xbox 360 controller
# is to be pressed which will perform a graceful shutdown cleaning up all subsystem states, GPIO
# pin states and finally shutting down the raspberry pi zero main board.
def StartControllerRoutine():
    # Driving mode and submodule state flags.
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
    
    # This infinite loop unifies all of the underlying functionality of the Xbox 360 controller
    # mapping routines and submodule functions. 
    while True:
        # Check if any previously pressed buttons have been released and if so reset their state,
        # else keep track of the fact that the button is still held down as to not trigger the
        # same action associated with that button twice. 
        ControllerDebouncer.CheckForButtonRelease()
        
        # Get the latest controller trigger and joystick values.
        LeftTrigger = Controller.leftTrigger()
        RightTrigger = Controller.rightTrigger()
        LeftStickXPos = Controller.leftStick()[0]
        RightStickXPos = Controller.rightStick()[0]
        
        # This is the decision tree for all of the button actions that are available via the Xbox
        # 360 controller interface. 
        
        # Back button pressed - Performs a graceful shutdown and clean-up of the AxiosRoboticsRCv1
        # unit.
        if Controller.Back() and (not ControllerDebouncer.ButtonBackPressed): 
            # Set the debouncer button state to pressed. 
            ControllerDebouncer.SetButtonBackPressed()
            # Shutdown and clean-up unit.
            Xbox360ControllerRoutines.CleanUpAndPowerDown(CameraModuleUsed, Controller)
        
        # B button pressed - Activates emergency e-stop and brings the unit to a halt.
        elif Controller.B() and (not ControllerDebouncer.ButtonBPressed):
             # Set the debouncer button state to pressed. 
            ControllerDebouncer.SetButtonBPressed()
            # Estop activated..
            EmergencyStopActive = True
            while (EmergencyStopActive):
                MotorController.StopMotors()
                # Deactivate estop once B button is released.
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
                # GPIO.output(promini, True)
                # time.sleep(1)
            # Turn off collision avoidance.    
            elif(CollisionAvoidanceOn): 
                CollisionAvoidanceOn = False  
                # Turn Off Sensor Managment Module
                # GPIO.output(promini, False)
                # time.sleep(1)
                
        # Left bumper activates the self driving mode.
        elif (Controller.rightBumper() and CollisionAvoidanceOn) and (not ControllerDebouncer.ButtonRBPressed):
            
            ControllerDebouncer.SetButtonRBPressed()
                          
          # RGB Headlight Dpad Integration
        elif Controller.dpadUp() and (not ControllerDebouncer.DpadUpPressed):
            
            ControllerDebouncer.SetButtonDpadUpPressed()
            
            if (not RGBHeadLightOn):
                Xbox360ControllerRoutines.RGBHeadLightDPadRoutine(CommonConstants.LEDON,)
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
                    TwoSpeedModeEnabled = False
                elif RollingBurnoutModeEnabled:
                    RollingBurnoutModeEnabled = False
                    TwoSpeedModeEnabled = True
                
        # A button activates/deactivates the rear wheel drive 4-speed burnout mode.
        elif Controller.A() and (not ControllerDebouncer.ButtonAPressed):
            
            ControllerDebouncer.SetButtonAPressed()
            
            if (not RollingBurnoutModeEnabled):
                if not RearWheelDriveBurnoutEnabled:
                    RearWheelDriveBurnoutEnabled = True
                    TwoSpeedModeEnabled = False
                elif RearWheelDriveBurnoutEnabled:
                    RearWheelDriveBurnoutEnabled = False
                    TwoSpeedModeEnabled = True
                    
        # Collision avoidance checks.
        elif CollisionAvoidanceOn:
            # Prevent Collision Detected By Left Sensor.
            """if(GPIO.input(LeftalrtReg) == 1):
                SmartSensorRoutines.AvoidCollision("LEFT")        
            # Prevent Collision Detected By Right Sensor
            elif (GPIO.input(RightalrtReg) == 1):
                SmartSensorRoutines.AvoidCollision("RIGHT") """            
                    
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
        
