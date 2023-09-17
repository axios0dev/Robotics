#!/usr/bin/env python3
import sys
import pydevd
from time import sleep
from Modules.Xbox360ControllerRoutines import Xbox360ControllerRoutines


#pydevd.settrace("192.168.1.101", port=5678)

def main():
   #pydevd.settrace()
   Xbox360ControllerRoutines.StartControllerRoutines()


   
if __name__ == "__main__":
    main()
        
