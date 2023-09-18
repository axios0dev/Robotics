#!/usr/bin/env python3
# This module contains a debouncer class which is designed to be used with the Xbox360ControllerAPI.
# This class keeps track of each button state to ensure when a button is pressed and held it is only
# registered as one action by the AxiosRobtoicsRCv1 unit. 
from Modules.Xbox360ControllerRoutines import Xbox360ControllerAPI


class Debouncer:
    # Local variable to store controller object passed by constructor.
    LocalControllerObject = None

    # Class constructor that takes an Xbox controller object.
    def __init__(self, xboxcontroller):
        self.LocalControllerObject = xboxcontroller
        
    # Button state flags
    # A, B, X, Y.
    ButtonAPressed = False
    ButtonBPressed = False
    ButtonXPressed = False
    ButtonYPressed = False
    #  RB, LB shoulder buttons.
    ButtonRBPressed = False
    ButtonLBPressed = False
    # Start, back, guide buttons.
    ButtonGuidePressed = False
    ButtonStartPressed = False
    ButtonBackPressed = False
    # Dpad buttons.
    DpadUpPressed = False
    DpadDownPressed = False
    DpadLeftPressed = False
    DpadRightPressed = False
    
    # This function is called at the start of the Xbox360ControllerRoutines.StartControllerRoutines()
    # loop to check if previously pressed buttons have been released and resets the appropriate state flags.
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
            
        if(not self.LocalControllerObject.dpadUp()):
            self.DpadUpPressed = False
            
        if(not self.LocalControllerObject.dpadDown()):
            self.DpadDownPressed = False

        if(not self.LocalControllerObject.dpadLeft()):
            self.DpadLeftPressed = False 
            
        if(not self.LocalControllerObject.dpadRight()):
            self.DpadRightPressed = False 
                          
    # These functions are to be called whenever a button is pressed and the corresponding action is performed
    # on the AxiosRoboticsRCv1 unit.        
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
        
    def SetButtonDpadUpPressed(self):
        self.DpadUpPressed = True   
        
    def SetButtonDpadDownPressed(self):
        self.DpadDownPressed = True  
        
    def SetButtonDpadLeftPressed(self):
        self.DpadLeftPressed = True      
      
    def SetButtonDpadRightPressed(self):
        self.DpadRightPressed = True                    
