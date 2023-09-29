#!/usr/bin/env python3
from serial import Serial 
from time import sleep

SerialConnection = Serial('/dev/ttyAMA0', 9600, timeout=1)



def ClearSerialBuffers():
    for iterations in range(0,100, 1):
        SerialConnection.reset_input_buffer()
        SerialConnection.reset_output_buffer()

def main():
    
    ClearSerialBuffers()
    SerialConnection.write(b"ON\n")   
    
    sleep(1)
    
    try:
        while True:
            sleep(0.02)
            
            if (SerialConnection.in_waiting > 0):
                try:
                    line = SerialConnection.readline().decode('utf-8').rstrip()
                    print(line)
                    
                except UnicodeDecodeError:
                    print("Buffer Data Error")
                       
        
     
    except KeyboardInterrupt:
            print("closting serial connection")
            SerialConnection.write(b"OFF\n")   
            SerialConnection.close() 


if __name__ == '__main__':
    main()
    
