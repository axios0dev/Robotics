#!/usr/bin/env python3

from Modules.LedSubsystem import HeadlightController, TailLightController
from Modules.MotorController import MotorController
from Modules.CameraSubsystem import VideoController
from time import sleep

def main():
    print("Stream Started")
    VideoController.VideoStreamStart()
    sleep(5)
    print("Stopping video")
    VideoController.StopVideo()
    print("Cleaning up server")
    VideoController.ServerCleanUp()
    
    
   
if __name__ == "__main__":
    main()
    
        