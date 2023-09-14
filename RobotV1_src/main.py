#!/usr/bin/env python3

from Modules.LedSubsystem import HeadlightController
from time import sleep

def main():
    #tbd
    HeadlightController.RGBcolorcycle("RED")
    print("RED")
    sleep(3)
    HeadlightController.LedOff()
    
    HeadlightController.RGBcolorcycle("GREEN")
    print("GREEN")
    sleep(3)
    HeadlightController.LedOff()
    
    HeadlightController.RGBcolorcycle("BLUE")
    print("BLUE")
    sleep(3)
    HeadlightController.LedOff()
    
    HeadlightController.RGBcolorcycle("YELLOW")
    print("YELLOW")
    sleep(3)
    HeadlightController.LedOff()
    
    HeadlightController.RGBcolorcycle("CYAN")
    print("CYAN")
    sleep(3)
    HeadlightController.LedOff()
    
    HeadlightController.RGBcolorcycle("Magenta")
    print("Magenta")
    sleep(3)
    HeadlightController.LedOff()
    
    HeadlightController.RGBcolorcycle("WHITE")
    print("WHITE")
    sleep(3)
    HeadlightController.LedOff()
    
    HeadlightController.RGBcolorcycle("ORANGE")
    print("ORANGE")
    sleep(3)
    HeadlightController.LedOff()
    

if __name__ == "__main__":
    main()
    
        