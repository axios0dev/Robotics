#!/usr/bin/env python3

from Modules.LedSubsystem import HeadlightController
from time import sleep

def main():
    #tbd
    HeadlightController.RGBcolorcycle("RED")
    print("RED")
    sleep(5)
    
    HeadlightController.RGBcolorcycle("GREEN")
    print("GREEN")
    sleep(5)
    
    HeadlightController.RGBcolorcycle("BLUE")
    print("BLUE")
    sleep(5)
    
    HeadlightController.RGBcolorcycle("YELLOW")
    print("YELLOW")
    sleep(5)
    
    HeadlightController.RGBcolorcycle("CYAN")
    print("CYAN")
    sleep(5)
    
    HeadlightController.RGBcolorcycle("Magenta")
    print("Magenta")
    sleep(5)
    
    HeadlightController.RGBcolorcycle("WHITE")
    print("WHITE")
    sleep(5)
    
    HeadlightController.RGBcolorcycle("ORANGE")
    print("ORANGE")
    sleep(5)
    

if __name__ == "__main__":
    main()
    
        