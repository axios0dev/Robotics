#!/usr/bin/env python3

from datetime import datetime
from serial import Serial
from threading import Thread, Event 
from time import sleep
from typing import Final

SerialConnection = Serial('/dev/ttyAMA0', 9600, timeout=1)

def ClearSerialBuffers():
    for iterations in range(0,100, 1):
        SerialConnection.reset_input_buffer()
        SerialConnection.reset_output_buffer()




DETECTION_DISTANCE: Final[int] = 15
DEBOUNCE_TIME_MS: Final[int] = 300

LeftSensorDetection = Event()
RightSensorDetection = Event()


LeftSensorLastDetectionTime = None
RightSensorLastDetectionTime = None



def SensorDetectionDebouncer(LeftSensorMeasurement, RightSensorMeasurement):
    global LeftSensorLastDetectionTime
    global RightSensorLastDetectionTime
    
    if(LeftSensorMeasurement < DETECTION_DISTANCE):
        if(LeftSensorLastDetectionTime == None):
            LeftSensorLastDetectionTime = datetime.now()
        else:
            LeftSensorDelta =  (datetime.now() - LeftSensorLastDetectionTime)
            if(LeftSensorDelta.total_seconds() * 1000 > DEBOUNCE_TIME_MS):
                LeftSensorDetection.set()
                LeftSensorLastDetectionTime = datetime.now()
                print("left snensor debounce detection")
                
    else:
        LeftSensorLastDetectionTime  = None   
        
            
         
    if(RightSensorMeasurement < DETECTION_DISTANCE):
        if (RightSensorLastDetectionTime == None):
            RightSensorLastDetectionTime = datetime.now()
        else:
            RightSensorDelta =  (datetime.now() - RightSensorLastDetectionTime)
            if(RightSensorDelta.total_seconds() * 1000 > DEBOUNCE_TIME_MS):
                RightSensorDetection.set()
                RightSensorLastDetectionTime = datetime.now()
                print("right snensor debounce detection")
               
    else:
        RightSensorLastDetectionTime  = None   
    
    

def SensorSerialRoutine(SensorThreadState):
    
    ClearSerialBuffers()
    SerialConnection.write(b"ON\n")   
    
    sleep(0.05)
    
    while SensorThreadState.is_set():
        if (SerialConnection.in_waiting > 0):
            try:
                SensorSerialData = SerialConnection.readline().decode('utf-8').rstrip()
                if(SensorSerialData == "Starting sensor reading routine..."):
                    print(SensorSerialData)
                    continue
                    
                LeftSensorData,RightSensorData = SensorSerialData.split(",")
                LeftSensorData = int(LeftSensorData.strip("L:"))
                RightSensorData = int(RightSensorData.strip("R:"))
                        
                SensorDetectionDebouncer(LeftSensorData, RightSensorData)        
          
            except UnicodeDecodeError:
                print("Serial buffer data error detected.")
                    
        sleep(0.02)  
        
    print("cleaning up thread")  
    SerialConnection.write(b"OFF\n")
    SerialConnection.close()
    
        
            
def main():
    SensorThreadStateEvent = Event()
    SensorThreadStateEvent.set()
    
    Thread(target=SensorSerialRoutine, args=(SensorThreadStateEvent,)).start()
     
    sleep(100)
    print("unsetting thread state")
    SensorThreadStateEvent.clear()
     
    
    
if __name__ == '__main__':
    main()
    
