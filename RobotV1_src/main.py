#!/usr/bin/env python3

from Modules.LedSubsystem import HeadlightController, TailLightController
from Modules.MotorController import MotorController
from time import sleep

def main():
   MotorController.Burnout(25, 3)
   MotorController.Burnout(50, 3)
   MotorController.Burnout(75, 3)
   MotorController.Burnout(100, 3)
   
 
 
    

if __name__ == "__main__":
    main()
    
        