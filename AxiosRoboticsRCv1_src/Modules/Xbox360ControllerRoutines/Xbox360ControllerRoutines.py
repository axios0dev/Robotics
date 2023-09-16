#!/usr/bin/env python3
import os import call
import xbox
from Modules.CameraSubsystem import CameraController
from Modules.LedSubsystem import HeadlightController
from Modules.LedSubsystem import TaillightController

# Initialize the controller object.
Controller = xbox.Joystick()
# Global state flag variables.
# Rolling Burnout Control Variable
RBMode = 0
# Collsion Avoidance variable control
colstate = 0
colavd = 0
# RGB Headlight Control Varaible
RGB = 0
select = 0
# Handbreak Control Variable
hbrake = 0
# Camera Recording Control Variabl
rec = 0

CameraModuleUsed = False

def ControllerRoutines():
    # Global variable linkage.
    global CameraModuleUsed
    
    while True:
        # Live left and right trigger position values.
        LeftTrigger = Controller.LeftTriggerer()
        RightTrigger = Controller.rightTrigger()
        # Live joystick X position values.
        LeftStickXPos  = Controller.leftStick()[0]
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
            
        # Y button powers on the front ultrasonic distance sensor module and,
        # enables dual collision avoidance. 
        elif Controller.Y():
            if colstate == 1:
                colstate = 0
                # Turn Off Sensor Managment Module
                GPIO.output(promini, False)
                time.sleep(1)
            elif colstate == 0:
                colstate = 1
                # Turn On Sensor Managment Module
                GPIO.output(promini, True)
                time.sleep(1)
        # Prevent Collision Detected By Left Sensor
        elif GPIO.input(LeftalrtReg) == 1  and colstate == 1:
            # Tail Light setup
            leftbrake(100)
            rightbrake(0)
            leftind(100)
            rightind(100)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            rev(0.3)
        # Prevent Collision Detected By Right Sensor
        elif GPIO.input(RightalrtReg) == 1 and colstate == 1:
            # Tail Light setup
            leftbrake(0)
            rightbrake(100)
            leftind(100)
            rightind(100)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            rev(0.3)

            # Rolling Burnout Mode Toggle
           elif Controller.Guide():
            if RBMode == 0:
                RBMode = 1
                time.sleep(1)
            elif RBMode == 1:
                RBMode = 0
                time.sleep(1)

        # Rear Wheel Drive  Mode Handbreak Toggle
        elif Controller.A():
            if hbrake == 0:
                hbrake = 1
                time.sleep(1)
            elif hbrake == 1:
                hbrake = 0
                time.sleep(1)

        # Thumbsticks
        # Left ThumbStick X-Axis Turning
        elif LeftStickXPos < -0.4:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(100)
            rightind(0)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            turnLEFT(0.1)
            fwd(0.01)
        elif LeftStickXPos > 0.4:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(100)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            turnRIGHT(0.1)
            fwd(0.01)
            
        # Right ThumbStick X-Axis Pivoting (2 Speed)
        elif RightStickXPos <= -0.6 and RightStickXPos >= -1.0:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(100)
            rightind(0)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            pivotleft(0.1)
        elif RightStickXPos <= -0.2 and RightStickXPos >= -0.6:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(50)
            rightind(0)
            # Movment Functions
            frontspeed(50)
            backspeed(50)
            pivotleft(0.1)
        elif RightStickXPos >= 0.2 and RightStickXPos <= 0.6:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(50)
            # Movment Functions
            frontspeed(50)
            backspeed(50)
            pivotright(0.1)
        elif RightStickXPos > 0.6 and RightStickXPos <= 1.0:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(100)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            pivotright(0.1)
        # Triggers
        # Accelerate Trigger 
        # 4 Speed Rear Wheel Drive Mode (HandBreak ON)
        elif hbrake == 1 and RightTrigger > 0.1 and RightTrigger <= 0.25:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(0)
            backspeed(25)
            fwd(0.1)
        elif hbrake == 1 and RightTrigger > 0.25 and RightTrigger <= 0.50:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(0)
            backspeed(50)
            fwd(0.1)
        elif hbrake == 1 and RightTrigger > 0.50 and RightTrigger <= 0.75:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(0)
            backspeed(75)
            fwd(0.1)
        elif hbrake == 1 and RightTrigger > 0.75 and RightTrigger <= 1.0:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(0)
            backspeed(100)
            fwd(0.1)
        # Rolling Burnout(4 speed)
        elif RBMode == 1 and RightTrigger > 0.1 and RightTrigger <= 0.25:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(4)
            backspeed(25)
            fwd(0.1)
        elif RBMode == 1 and RightTrigger > 0.25 and RightTrigger <= 0.50:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(4)
            backspeed(50)
            fwd(0.1)
        elif RBMode == 1 and RightTrigger > 0.50 and RightTrigger <= 0.75:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(4)
            backspeed(75)
            fwd(0.1)
        elif RBMode == 1 and RightTrigger > 0.75 and RightTrigger <= 1.0:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(4)
            backspeed(100)
            fwd(0.1)

        # All Wheel Drive 2-Speed
        elif RightTrigger > 0.1 and RightTrigger <= 0.50:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(30)
            backspeed(30)
            fwd(0.1)
        elif RightTrigger > 0.50 and RightTrigger <= 1.0:
            # Tail Light setup
            leftbrake(0)
            rightbrake(0)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            fwd(0.1)

        # Reverse 2-Speed
        elif LeftTrigger > 0.1 and LeftTrigger <= 0.50:
            # Tail Light setup
            leftbrake(50)
            rightbrake(50)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(30)
            backspeed(30)
            rev(0.1)
        elif LeftTrigger > 0.50 and LeftTrigger <= 1.0:
            # Tail Light setup
            leftbrake(100)
            rightbrake(100)
            leftind(0)
            rightind(0)
            # Movment Functions
            frontspeed(100)
            backspeed(100)
            rev(0.1)            
        # AI Auto Pilot Override
        elif Controller.leftBumper() and colstate == 1:
            if colavd == 0:
                colavd = 1
                time.sleep(1)
                # Entrapment detect Variables
                leftcount = 0
                rightcount = 0
                while colavd == 1:
                    # Infinitely avoid collision desicison tree
                    # If entrament is detected reverse and turn 180 degres
                    if Controller.leftBumper():
                        stop(0.1)
                        colavd = 0
                        time.sleep(1)
                    elif leftcount == 2:
                        # Tail Light setup
                        leftbrake(0)
                        rightbrake(0)
                        leftind(100)
                        rightind(0)
                        # Movment Functions
                           frontspeed(100)
                        backspeed(100)
                        leftcount = 0
                        rev(0.4)
                        pivotleft(0.6)
                    elif rightcount == 2:
                        # Tail Light setup
                        leftbrake(0)
                        rightbrake(0)
                        leftind(0)
                        rightind(100)
                        # Movment Functions
                        frontspeed(100)
                        backspeed(100)
                        rightcount = 0
                        rev(0.4)
                        pivotright(0.6)
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
