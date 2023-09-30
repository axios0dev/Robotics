#!/usr/bin/env python3


from serial import Serial
from threading import Thread, Event 
from time import sleep

SerialConnection = Serial('/dev/ttyAMA0', 9600, timeout=1)



def ClearSerialBuffers():
    for iterations in range(0,100, 1):
        SerialConnection.reset_input_buffer()
        SerialConnection.reset_output_buffer()

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
                        
                print("Left val", LeftSensorData)
                print("Right val", RightSensorData)
                    
                    
            except UnicodeDecodeError:
                print("Serial Buffer Error")
                    
        sleep(0.02)  
            
def main():
    SensorThreadStateEvent = Event()
    SensorThreadStateEvent.set()
    
    Thread(target=SensorSerialRoutine, args=(SensorThreadStateEvent,)).start()
    
    
    sleep(2)
    print("unsetting thread state")
    SensorThreadStateEvent.clear()
    SerialConnection.write(b"OFF\n")
    SerialConnection.close() 
    
    
if __name__ == '__main__':
    main()
    
