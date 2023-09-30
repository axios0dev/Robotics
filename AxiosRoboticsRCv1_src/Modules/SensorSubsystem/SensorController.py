#!/usr/bin/env python3
# This module contains the controller code for the ultrasonic distance sensor module that is used
# for collision avoidance and self driving AI functionality of the AxiosRoboticsRCv1 unit.

# Python library imports.
from datetime import datetime
from serial import Serial
from threading import Thread, Event 
from time import sleep
from typing import Final

# Serial connection instantiation and parameter setup, this is used to communicate with the sensor module.
SerialConnection = Serial('/dev/ttyAMA0', 9600, timeout=1)


# This function clears both the serial connection input and output buffer, performing any iterations to
# ensure all buffered data is cleared out prior to starting sensor monitoring. 
def ClearSerialBuffers():
    # Perform 100 iterations of the buffer clearing routine to ensure all data remaining in the buffer of
    # the link is cleared.  
    for iterations in range(0, 100, 1):
        SerialConnection.reset_input_buffer()
        SerialConnection.reset_output_buffer()


# Constant definition of the detection distance and debouncer detection threshold time.
DETECTION_DISTANCE: Final[int] = 15
DEBOUNCE_TIME_MS: Final[int] = 300
# Global thread safe flags which are set when an object has been detected on a respective
# sensor after the debouncer class has verified the detection. 
LeftSensorDetection = Event()
RightSensorDetection = Event()


# This class contains the functionality to filter out false detections on the left and right sensor of
# the AxiosRoboticsRCv1 sensor module. Sometimes when an object or obstacle is on an angle to the sensors
# and not front on, the sensors report a distance value less than the threshold. However on subsequent readings
# within the same second this false detection is not reported. So a filtering function is used to only report a
# valid detection if the sensor has measured an object closer than the detection threshold for more than the
# defined DEBOUNCE_TIME_MS.
class SensorDetectionDebouncer:
    # Variables to store the last time an object was detected in a distance less than the threshold.
    LeftSensorLastDetectionTime = None
    RightSensorLastDetectionTime = None
    
    # This function validates and reports objects or obstacles that are detected by the AxiosRoboticsRCv1 units
    # front sensors, after a debounce routine has been satisfied.
    def CheckForValidDetection(self, LeftSensorMeasurement, RightSensorMeasurement):
        # Check if the left sensor measurement is less than the detection distance.
        if(LeftSensorMeasurement < DETECTION_DISTANCE):
            # If this is the first detection since the last time this was called capture the time.
            if(self.LeftSensorLastDetectionTime == None):
                self.LeftSensorLastDetectionTime = datetime.now()
            # If this is not the first detection since the last time this method was called then run a comparison
            # to see if this is a valid detection and if so set the left sensor detection flag.
            else:
                # Calculate the time difference since last detection.
                LeftSensorDelta = (datetime.now() - self.LeftSensorLastDetectionTime)
                # Convert the difference into ms and compare against the DEBOUNCE_TIME_MS threshold.
                if(LeftSensorDelta.total_seconds() * 1000 > DEBOUNCE_TIME_MS):
                    # Set the thread safe detection flag to notify the other routines of the detection so it can
                    # be handled accordingly. 
                    LeftSensorDetection.set()
                    # Capture this as the last detection time.
                    self.LeftSensorLastDetectionTime = datetime.now()
                    print("left snensor debounce detection")          
        # If not object is within the detection threshold unset the last detection time.        
        else:
            self.LeftSensorLastDetectionTime = None   
         
        # Check if the left sensor measurement is less than the detection distance. 
        if(RightSensorMeasurement < DETECTION_DISTANCE):
            # If this is the first detection since the last time this was called capture the time.
            if (self.RightSensorLastDetectionTime == None):
                self.RightSensorLastDetectionTime = datetime.now()
            # If this is not the first detection since the last time this method was called then run a comparison
            # to see if this is a valid detection and if so set the right sensor detection flag.
            else:
                # Calculate the time difference since last detection.
                RightSensorDelta = (datetime.now() - self.RightSensorLastDetectionTime)
                # Convert the difference into ms and compare against the DEBOUNCE_TIME_MS threshold.
                if(RightSensorDelta.total_seconds() * 1000 > DEBOUNCE_TIME_MS):
                    # Set the thread safe detection flag to notify the other routines of the detection so it can
                    # be handled accordingly. 
                    RightSensorDetection.set()
                    self.RightSensorLastDetectionTime = datetime.now()
                    print("right snensor debounce detection")
        # If not object is within the detection threshold unset the last detection time.         
        else:
            self.RightSensorLastDetectionTime = None   
    

def SensorSerialRoutine(SensorThreadState):
    
    SensorDebouncer = SensorDetectionDebouncer()
    
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
                    
                LeftSensorData, RightSensorData = SensorSerialData.split(",")
                LeftSensorData = int(LeftSensorData.strip("L:"))
                RightSensorData = int(RightSensorData.strip("R:"))
                        
                SensorDetectionDebouncer.CheckForValidDetection(SensorDetectionDebouncer, LeftSensorData, RightSensorData)        
          
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
    
