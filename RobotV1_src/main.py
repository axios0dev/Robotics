#!/usr/bin/env python3

from Modules.LedSubsystem import HeadlightController, TailLightController
from Modules.MotorController import MotorController
from time import sleep

def main():
   MotorController.StopMotors(1)
   MotorController.DriveForward(25, 3)
   MotorController.DriveForward(50, 3)
   MotorController.DriveForward(75, 3)
   MotorController.DriveForward(100, 3)
   MotorController.StopMotors(1)
 
 
    

if __name__ == "__main__":
    main()
    
        