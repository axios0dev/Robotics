#!/usr/bin/env python3
import sys
import pydevd
from time import sleep
from Modules.MotorSubsystem import MotorController

pydevd.settrace("192.168.1.101", port=5678)


def main():
   MotorController.DriveForward(100, 15)


   
if __name__ == "__main__":
    main()
        
