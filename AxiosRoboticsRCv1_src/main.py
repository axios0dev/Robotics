#!/usr/bin/env python3
import sys
import pydevd
from time import sleep
from Modules.CameraSubsystem import VideoController

pydevd.settrace("192.168.1.101", port=5678)


def main():
    print("Stream Started")
    VideoController.VideoStreamStart()
    sleep(5)
    print("Stopping video")
    VideoController.StopVideo()
    print("local record start")
    VideoController.StartLocalRecording()
    sleep(5)
    print("Stopping video")
    VideoController.StopVideo()
    print("Cleaning up server")
    VideoController.ServerCleanUp()


   
if __name__ == "__main__":
    main()
        
