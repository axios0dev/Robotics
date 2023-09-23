



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


DETECTIONSUNTILENTRAPMENT: Final[int] = 3

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

