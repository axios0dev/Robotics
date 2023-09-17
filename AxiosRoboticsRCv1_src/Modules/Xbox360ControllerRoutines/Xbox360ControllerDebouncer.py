#!/usr/bin/env python3
from Modules.Xbox360ControllerRoutines import Xbox360ControllerAPI

class Debouncer:
    
    LocalControllerObject = None
    
    def __init__(self,xboxcontroller):
        self.LocalControllerObject = xboxcontroller
        
    # Button state flags
    # A. B. X. Y.
    ButtonAPressed = False
    ButtonBPressed = False
    ButtonXPressed = False
    ButtonYPressed = False
    # Shoulder Buttons.
    ButtonRBPressed = False
    ButtonLBPressed = False
    # Start, back, guide buttons.
    ButtonGuidePressed = False
    ButtonStartPressed = False
    ButtonBackPressed = False
    # D-Pad buttons.
    DPadUpPressed = False
    DPadDownPressed = False
    DPadLeftPressed = False
    DPadRightPressed= False
    
    
    def CheckForButtonRelease(self):
        if(not self.LocalControllerObject.A()):
            self.ButtonAPressed = False
            
        if(not self.LocalControllerObject.B()):
            self.ButtonBPressed = False
            
        if(not self.LocalControllerObject.X()):
            self.ButtonXPressed = False
            
        if(not self.LocalControllerObject.Y()):
            self.ButtonYPressed = False
            
        if(not self.LocalControllerObject.rightBumper()):
            self.ButtonRBPressed = False
            
        if(not self.LocalControllerObject.leftBumper()):
            self.ButtonLBPressed = False
            
        if(not self.LocalControllerObject.Guide()):
            self.ButtonGuidePressed = False
            
        if(not self.LocalControllerObject.Start()):
            self.ButtonStartPressed = False   
            
        if(not self.LocalControllerObject.Back()):
            self.ButtonBackPressed = False
            print("back not pressed")          
            
            
            
    def SetButtonAPressed(self):
        self.ButtonAPressed = True
        
    def SetButtonBPressed(self):
        self.ButtonBPressed = True

    def SetButtonXPressed(self):
        self.ButtonXPressed = True   
             
    def SetButtonYPressed(self):
        self.ButtonYPressed = True   
        
    def SetButtonRBPressed(self):
        self.ButtonRBPressed = True  
         
    def SetButtonLBPressed(self):
        self.ButtonLBPressed = True  
        
    def SetButtonGuidePressed(self):
        self.ButtonGuidePressed = True  
    
    def SetButtonStartPressed(self):
        self.ButtonStartPressed = True  
        
    def SetButtonBackPressed(self):
        self.ButtonBackPressed = True      