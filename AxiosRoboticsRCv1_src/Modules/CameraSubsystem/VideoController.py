#!/usr/bin/env python3
import socket
import picamera
from time import sleep

# Camera Setup
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = (24)
# camera.start_preview()
sleep(2)

# Streaming Socket Server Setup
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
connection = server_socket.accept()[0].makefile('wb')

CameraCurrentlyRecording = False

def VideoStreamStart():
    if(CameraCurrentlyRecording == False):
        camera.start_recording(connection, format='h264')
        CameraCurrentlyRecording = True

        
def StopVideo():
    if(CameraCurrentlyRecording == True):
        camera.stop_recording()
        CameraCurrentlyRecording = False

        
def ServerCleanUp():
    # Close Streaming Socket Server
    connection.close()
    server_socket.close()

            
def StartLocalRecording():
    if(CameraCurrentlyRecording == False):
        camera.start_recording()
        CameraCurrentlyRecording = True 
