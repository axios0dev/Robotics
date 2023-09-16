#Remote Eclipse IDE Initialisation
#import sys;
#import pydevd;pydevd.settrace('192.168.1.251', port=5678)
#print("test remote ide run")

#Sensor Detection System
import RPi.GPIO as GPIO
import time 
#Arduino Pro Mini Power On/Off Pin
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Arduino setup
promini = 8
LeftalrtReg = 21
LeftalrtAI = 16
RightalrtReg = 20
RightalrtAI = 1

GPIO.setup(promini, GPIO.OUT)
GPIO.setup(LeftalrtReg, GPIO.IN)
GPIO.setup(LeftalrtAI, GPIO.IN)
GPIO.setup(RightalrtReg, GPIO.IN)
GPIO.setup(RightalrtAI, GPIO.IN)


#Power On
while True:
    GPIO.output(promini, True)
    if GPIO.input(LeftalrtReg) == 1:
        print("left object detected(Reg-Dist)")
    elif GPIO.input(LeftalrtAI) == 1:  
          print("left object detected(AI-Dist)")
    elif GPIO.input(RightalrtReg) == 1:  
        print("Right object detected(Reg-Dist)")
    elif GPIO.input(RightalrtAI) == 1: 
        print("Right object detected(AI-Dist)")   