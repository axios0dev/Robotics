#!/usr/bin/env python3
# This module contains the code to create a socket server and establish a TCP,
# connection to a VLC client for live viewing of the video feed from the camera,
# on top of the AxiosRoboticsRCv1 unit.
# To establish a connection to this server open the following network stream on a,
# VLC client on a computer connected to the same local network as the AxiosRoboticsRCv1 unit.
# tcp/h264://ip_address_of_unit:8000/
import socket
import picamera
from time import sleep

# Camera Setup
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = (24)
sleep(2)

# TCP socket server setup. 
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
connection = server_socket.accept()[0].makefile('wb')
# State flag to keep track of when the camera module resource is in use,
# by this controller.
CameraCurrentlyRecording = False

# Start streaming over the TCP connection file descriptor.
def VideoStreamStart():
    global CameraCurrentlyRecording
    if(CameraCurrentlyRecording == False):
        camera.start_recording(connection, format='h264')
        CameraCurrentlyRecording = True

# Stop the video feed from the camera module.        
def StopVideo():
    global CameraCurrentlyRecording
    if(CameraCurrentlyRecording == True):
        camera.stop_recording()
        CameraCurrentlyRecording = False

# This function needs to be called before exiting the program to,
# close the active TCP connection and socket server.        
def ServerCleanUp():
    # Close Streaming Socket Server
    connection.close()
    server_socket.close()

# This function is to be used to create a video recording to local,
# storage on the AxiosRoboticsRCv1 unit.            
def StartLocalRecording():
    global CameraCurrentlyRecording
    if(CameraCurrentlyRecording == False):
        camera.start_recording('CameraLocalCapture/AxiosRoboticsRCv1_VisionCameraLocal.h264')
        CameraCurrentlyRecording = True 
