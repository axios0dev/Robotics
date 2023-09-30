#!/usr/bin/env python3


from serial import Serial
from threading import Thread, Event 
from time import sleep

SerialConnection = Serial('/dev/ttyAMA0', 9600, timeout=1)



def ClearSerialBuffers():
    for iterations in range(0,100, 1):
        SerialConnection.reset_input_buffer()
        SerialConnection.reset_output_buffer()

def SensorControllerRoutine(SensorThreadState):
    
    ClearSerialBuffers()
    SerialConnection.write(b"ON\n")   
    
    sleep(0.05)
    
    try:
        while SensorThreadState.is_set():
               
            if (SerialConnection.in_waiting > 0):
                try:
                    SensorSerialData = SerialConnection.readline().decode('utf-8').rstrip()
                    LeftSensorData,RightSensorData = SensorSerialData.split(",")
                    LeftSensorData = int(LeftSensorData.strip("L:"))
                    RightSensorData = int(RightSensorData.strip("R:"))
                    
                    
                    print("Left val", LeftSensorData)
                    print("Right val", RightSensorData)
                    
                    
                except UnicodeDecodeError:
                    print("Serial Buffer Error")
                    
            sleep(0.02)  
            
             
     
    except KeyboardInterrupt:
            print("closting serial connection")
            SerialConnection.write(b"OFF\n")   
            SerialConnection.close() 


def main():
    SensorThreadStateEvent = Event()
    SensorThreadStateEvent.set()
    
    Thread(target=SensorControllerRoutine, args=(SensorThreadStateEvent,)).start()
    
    
    sleep(10)
    print("unsetting thread state")
    #SensorThreadStateEvent.clear()
    
    
    
    

if __name__ == '__main__':
    main()
    
