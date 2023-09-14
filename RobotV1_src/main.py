#!/usr/bin/env python3

from Modules.LedSubsystem import HeadlightController, TailLightController
from time import sleep

def main():
    TailLightController.LeftBrakeLightOn(25)
    TailLightController.RightBrakeLightOn(25)
    sleep(3)
    TailLightController.LeftBrakeLightOn(50)
    TailLightController.RightBrakeLightOn(50)
    sleep(3)
    TailLightController.LeftBrakeLightOn(75)
    TailLightController.RightBrakeLightOn(75)
    sleep(3)
    TailLightController.LeftBrakeLightOn(100)
    TailLightController.RightBrakeLightOn(100)
    sleep(3)
    TailLightController.BrakeLightsOff()
    
    TailLightController.LeftIndicatorOn(25)
    TailLightController.RightIndicatorOn(25)
    sleep(3)
    TailLightController.LeftIndicatorOn(50)
    TailLightController.RightIndicatorOn(50)
    sleep(3)
    TailLightController.LeftIndicatorOn(75)
    TailLightController.RightIndicatorOn(75)
    sleep(3)
    TailLightController.LeftIndicatorOn(100)
    TailLightController.RightIndicatorOn(100)
    sleep(3)
    TailLightController.IndicatorLightsOff()
   
 
 
    

if __name__ == "__main__":
    main()
    
        