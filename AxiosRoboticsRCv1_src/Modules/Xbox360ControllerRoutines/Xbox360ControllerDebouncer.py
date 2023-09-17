#!/usr/bin/env python3
from Modules.Xbox360ControllerRoutines import Xbox360ControllerAPI

class Debouncer:
    
    LocalControllerObject = None
    
    def __init__(self,xboxcontroller):
        self.LocalControllerObject = xboxcontroller
        
    # Button state flags
    ButtonAPressed = False
    ButtonBPressed = False
    ButtonXPressed = False
    ButtonYPressed = False
    ButtonRBPressed = False
    ButtonLBPressed = False
    ButtonGuidePressed = False
    ButtonStartPressed = False
    ButtonBackPressed = False
    DPadUpPressed = False
    DPadDownPressed = False
    DPadLeftPressed = False
    DPadRightPressed= False
    
    
    def CheckForButtonRelease(self):
        if(not ControllerObject.Back()):
            self.ButtonAPressed = False
    
    def SetButtonAPressed(self):
        self.ButtonAPressed = True
        
    
    
    