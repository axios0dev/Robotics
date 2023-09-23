#!/usr/bin/env python3
# This module contains the main controller routine that calls the Xbox 360 controller sub
# routines and underlying functions that operate the entire AxiosRobtoticsRCv1 unit.

# AxiosRobtoticsRCv1 submodule and common library imports.
from Modules.CameraSubsystem import CameraController
from Modules.ConstLib import CommonConstants
from Modules.LEDSubsystem import HeadlightController
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
    while (True):
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
            # Estop activated.
            EmergencyStopActive = True
            while (EmergencyStopActive):
                MotorController.StopMotors()
                # Deactivate estop once B button is released.
                if(not Controller.B()):
                    EmergencyStopActive = False
          
        # Start button pressed - starts the live video feed from the camera controller.
        elif Controller.Start() and (not ControllerDebouncer.ButtonStartPressed):
            # Set the debouncer button state to pressed. 
            ControllerDebouncer.SetButtonStartPressed()
            # Set the camera module usage flag to ensure that the camera controller module is
            # cleaned up correctly if it has been used. 
            if(not CameraModuleUsed):
                CameraModuleUsed = True
            # Start the live feed.
            CameraController.VideoStreamStart()
            
        # LB button pressed - Turns on the sensor subsystem module and enables collision 
        # avoidance overrides.
        elif Controller.leftBumper() and (not ControllerDebouncer.ButtonLBPressed):
            # Set the debouncer button state to pressed.
            ControllerDebouncer.SetButtonLBPressed()
            # Turn on collision avoidance state flag and sensor subsystem module..
            if (not CollisionAvoidanceOn):
                CollisionAvoidanceOn = True
            # Turn off collision avoidance.    
            elif(CollisionAvoidanceOn): 
                CollisionAvoidanceOn = False  
             
        # RB button pressed - Activates the self driving AI mode.
        elif (Controller.rightBumper() and CollisionAvoidanceOn) and (not ControllerDebouncer.ButtonRBPressed):
            # Set the debouncer button state to pressed.
            ControllerDebouncer.SetButtonRBPressed()
                          
        # Dpad up pressed - Toggles the RGB headlights off and on.
        elif Controller.dpadUp() and (not ControllerDebouncer.DpadUpPressed):
            # Set the debouncer button state to pressed.
            ControllerDebouncer.SetButtonDpadUpPressed()
            # Turn on RGB headlights.
            if (not RGBHeadLightOn):
                Xbox360ControllerRoutines.RGBHeadlightDpadRoutine(CommonConstants.LEDON)
            # Turn on RGB headlights.
            elif (RGBHeadLightOn):
                Xbox360ControllerRoutines.RGBHeadlightDpadRoutine(CommonConstants.LEDOFF)   
                
        # Dpad left pressed - Cycles back through RGB headlight colour set.
        elif Controller.dpadLeft() and (not ControllerDebouncer.DpadLeftPressed):
            # Set the debouncer button state to pressed.
            ControllerDebouncer.SetButtonDpadLeftPressed()
            # Cycle back through colours.
            Xbox360ControllerRoutines.RGBHeadlightDpadRoutine(CommonConstants.PREVCOLOUR)
            
        # Dpad right pressed - Cycles forward through RGB headlight colour set.
        elif Controller.dpadRight() and (not ControllerDebouncer.DpadRightPressed):
            # Set the debouncer button state to pressed.
            ControllerDebouncer.SetButtonDpadRightPressed()
             # Cycle forward through colours.
            Xbox360ControllerRoutines.RGBHeadlightDpadRoutine(CommonConstants.NEXTCOLOUR)
                                        
        # Guide button pressed - Activates/deactivates the rolling burnout easter egg mode.
        elif Controller.Guide() and (not ControllerDebouncer.ButtonGuidePressed):
            # Set the debouncer button state to pressed.
            ControllerDebouncer.SetButtonGuidePressed()
            # Ensure the conflicting rear wheel burnout mode is not enabled, these
            # two modes are mutually exclusive. 
            if (not RearWheelDriveBurnoutEnabled):
                # Toggle rolling burnout mode on/off.
                if (not RollingBurnoutModeEnabled):
                    RollingBurnoutModeEnabled = True
                    # Disable the standard two speed mode.
                    TwoSpeedModeEnabled = False
                elif (RollingBurnoutModeEnabled):
                    RollingBurnoutModeEnabled = False
                    # Enable the standard two speed mode.
                    TwoSpeedModeEnabled = True
                
        # A button pressed -  Activates/deactivates the rear wheel drive 4-speed burnout mode.
        elif Controller.A() and (not ControllerDebouncer.ButtonAPressed):
            # Set the debouncer button state to pressed.
            ControllerDebouncer.SetButtonAPressed()
            # Ensure the conflicting rolling burnout mode is not enabled, these
            # two modes are mutually exclusive. 
            if (not RollingBurnoutModeEnabled):
                # Toggle 4-speed rear wheel burnout mode on/off.
                if (not RearWheelDriveBurnoutEnabled):
                    RearWheelDriveBurnoutEnabled = True
                    # Disable the standard two speed mode.
                    TwoSpeedModeEnabled = False
                elif (RearWheelDriveBurnoutEnabled):
                    RearWheelDriveBurnoutEnabled = False
                    # Enable the standard two speed mode.
                    TwoSpeedModeEnabled = True
                    
        # Collision override flag set - Performs collision avoidance routine.
        elif CollisionAvoidanceOn:
            """if(GPIO.input(LeftalrtReg) == 1):
                SmartSensorRoutines.AvoidCollision("LEFT")        
            # Prevent Collision Detected By Right Sensor
            elif (GPIO.input(RightalrtReg) == 1):
                SmartSensorRoutines.AvoidCollision("RIGHT") """            
                    
        # Thumbstick mapping logic.
        # Left thumbstick x-axis controls the left and right turn functionality.
        # Turn left.
        elif (LeftStickXPos < -CommonConstants.LEFTJOYSTICKDEADZONE):
            MotorController.TurnLeft(CommonConstants.FULLSPEED, CommonConstants.DEFAULTACTIONSPEED)
        # Turn right.    
        elif (LeftStickXPos > CommonConstants.LEFTJOYSTICKDEADZONE):
            MotorController.TurnRight(CommonConstants.FULLSPEED, CommonConstants.DEFAULTACTIONSPEED)
        
        # Right thumbstick pivot logic.
        # If the right thumbstick is moved perform the pivot functionality.
        elif (RightStickXPos <= -CommonConstants.RIGHTJOYSTICKDEADZONE) or (RightStickXPos >= CommonConstants.RIGHTJOYSTICKDEADZONE):
            Xbox360ControllerRoutines.PivotRoutine(RightStickXPos)    
     
        # Trigger mapping logic.
        # Right trigger pressed - Performs the reverse trigger functionality.        
        # Reverse 2-speed, reverse at 30% speed if the trigger is half depressed.
        elif (LeftTrigger > CommonConstants.TRIGGERDEADZONE) and (LeftTrigger <= CommonConstants.TRIGGERHALFPRESSED):
            MotorController.DriveBackwards(CommonConstants.LOWGEARSPEED, CommonConstants.DEFAULTACTIONSPEED)
        # Reverse at 100$ speed if the trigger is overhalf way depressed.
        elif (LeftTrigger > CommonConstants.TRIGGERHALFPRESSED):
            MotorController.DriveBackwards(CommonConstants.FULLSPEED, CommonConstants.DEFAULTACTIONSPEED)
                        
        # Left trigger pressed - Accelerate trigger logic performed depending on current drive mode.
        # Check for special drive mode overrides first. 
        # 4-Speed Rear Wheel Drive Mode.
        elif RearWheelDriveBurnoutEnabled:
            Xbox360ControllerRoutines.RearWheelDriveBurnout(RightTrigger)     
                   
        # 4-speed rolling burnout easter egg drive mode.        
        elif RollingBurnoutModeEnabled:
            Xbox360ControllerRoutines.RollingBurnoutMode(RightTrigger)
            
        # 2-speed all wheel drive mode.
        elif TwoSpeedModeEnabled:
            Xbox360ControllerRoutines.TwoSpeedAWDMode(RightTrigger)
        
