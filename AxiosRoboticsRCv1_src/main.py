#!/usr/bin/env python3
import sys
import pydevd
from time import sleep
from Modules.Xbox360ControllerRoutines import Xbox360ControllerMainRoutine


#pydevd.settrace("192.168.1.101", port=5678)

def main():
   #pydevd.settrace()
   Xbox360ControllerMainRoutine.StartControllerRoutine()


   
if __name__ == "__main__":
    main()
        
