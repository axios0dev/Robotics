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

        
# This function should be called when before shutting down the AxiosRoboticsRCv1 unit to close the serial
# connection to the sensor module.        
def CleanupSerialConnection():
    SerialConnection.close()   


# Constant definition of the detection distance and debouncer detection threshold time.
DETECTION_DISTANCE: Final[int] = 15
DEBOUNCE_TIME_MS: Final[int] = 150
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
                    # Capture this as the last detection time.
                    self.RightSensorLastDetectionTime = datetime.now()
                    print("right snensor debounce detection")
        # If not object is within the detection threshold unset the last detection time.         
        else:
            self.RightSensorLastDetectionTime = None   


# This routine contains the functionality to send the ‘ON’ command to the front sensor module and receives the
# readings sent out from the module back over the serial connection. Once the module receives the ‘ON’ command
# over the serial connection, the module will continue to report the readings from each sensor until this routine
# is stopped at which point the clean up functionality is run which sends the ‘OFF’ command to the module.
# A thread safe event is passed to this function to keep this routine running in a separate thread.
def SensorSerialRoutine(SensorThreadState):
    # Create an instance of the SensorDetectionDebouncer() class,
    # this is used to filter out false detections on from the sensor module.
    SensorDebouncer = SensorDetectionDebouncer()
    # Call the serial buffer clear function to ensure that both the input and output buffer of
    # the UART serial connection is empty before the monitoring routine starts. 
    ClearSerialBuffers()
    # Send the ON command to the sensor module.
    SerialConnection.write(b"ON\n")   
    # Sleep for 15ms to ensure the ON command is received before beginning serial monitoring.
    sleep(0.015)
    
    # Keep this routine running while the thread event is set, stop this routine and run the clean up
    # section once this is unset.
    while SensorThreadState.is_set():
        # Check if any serial data has been received and is waiting to be read from the buffer.
        if (SerialConnection.in_waiting > 0):
            # This try catch block will handle any errors encountered when the data read from the serial
            # buffer is not the expected data type or is garbled.
            try:
                # Read the string serial data and strip out the line terminator character.
                SensorSerialData = SerialConnection.readline().decode('utf-8').rstrip()
                # This is the initial msg that is expected from the sensor module once it has received the 
                # 'ON' command indicating the modules sensor reading reporting routine is starting.
                if(SensorSerialData == "Starting sensor reading routine..."):
                    # Print the msg to the terminal and continue to the next loop iteration.
                    print(SensorSerialData)
                    continue
                # This case will read the keyed sensor data into a string and perform string processing 
                # to parse out each sensors individual distance value into an int.
                else:
                    # Split the keyed data into a left and right value, split at the ',' delimiter.    
                    LeftSensorData, RightSensorData = SensorSerialData.split(",")
                    # Strip out the L: and R: key and store the raw sensor reading value.
                    LeftSensorData = int(LeftSensorData.strip("L:"))
                    RightSensorData = int(RightSensorData.strip("R:"))
                    # Call the sensor debouncer reading validation check to parse out false detections and 
                    # report all valid detections via the thread event flags.    
                    SensorDebouncer.CheckForValidDetection(LeftSensorData, RightSensorData)        
            # Catch the serial buffer data type decode error. 
            except UnicodeDecodeError:
                print("Serial buffer data error detected.")
        # Sleep for 50ms to limit the rate of serial link readings, this limits CPU usage for this routine.
        # The sensor module firmware reports sensor distance readings every 100ms so a reading rate of the serial
        # link of 50ms is plenty to ensure this routine keeps up with the sensor module data.             
        sleep(0.05)  
    # This is the final cleanup logic to turn off the sensor module.    
    print("Stopping sensor reading routine...")  
    SerialConnection.write(b"OFF\n")
    CleanupSerialConnection()
        
            
def main():
    SensorThreadStateEvent = Event()
    SensorThreadStateEvent.set()
    
    Thread(target=SensorSerialRoutine, args=(SensorThreadStateEvent,)).start()
     
    sleep(100)
    print("unsetting thread state")
    SensorThreadStateEvent.clear()
    
    
if __name__ == '__main__':
    main()
    
