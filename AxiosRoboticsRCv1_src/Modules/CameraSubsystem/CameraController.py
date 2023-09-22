#!/usr/bin/env python3
# This module contains the code to create a socket server and establish a TCP,
# connection to a VLC client for live viewing of the video feed from the camera,
# on top of the AxiosRoboticsRCv1 unit.
# To establish a connection to this server open the following network stream on a,
# VLC client on a computer connected to the same local network as the AxiosRoboticsRCv1 unit.
# tcp/h264://ip_address_of_unit:8000/

# Python library imports.
from socket import socket
from  picamera import PiCamera
from threading import Thread, Event
from time import sleep
# AxiosRoboticsRCv1 unit modules.
from Modules.LedSubsystem import TailLightController

# PiCamera instance and parameter setup.
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = (24)
sleep(2)
# State flag to keep track of when the camera module resource is in use
# by this controller.
CameraCurrentlyRecording = False


# TCP socket server state flag and server variables.
StreamServerOnline = False
server_socket = None
connection = None

# This function...
def StreamServerStart():
    global StreamServerOnline
    global server_socket
    global connection
    
    # TCP socket server setup. 
    server_socket = socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)
    
    WaitingForTCPConnection = Event()
    WaitingForTCPConnection.set()
     # call thread here
    Thread(target=TailLightController.SyncIndicators, args=(WaitingForTCPConnection,)).start()
    
    connection = server_socket.accept()[0].makefile('wb')
    WaitingForTCPConnection.clear()
    
    StreamServerOnline = True
    
    
# Start streaming over the TCP connection file descriptor.
def VideoStreamStart():
    global CameraCurrentlyRecording
    global StreamServerOnline
    global connection
    
    if (not StreamServerOnline):
        StreamServerStart()
        
    if(not CameraCurrentlyRecording):
        camera.start_recording(connection, format='h264')
        CameraCurrentlyRecording = True
    # If this is called while a the video feed is active stop the video feed.    
    elif(CameraCurrentlyRecording):
        StopVideo()


# Stop the video feed from the camera module.        
def StopVideo():
    global CameraCurrentlyRecording
    if(CameraCurrentlyRecording == True):
        camera.stop_recording()
        CameraCurrentlyRecording = False


# This function needs to be called before exiting the program to,
# close the active TCP connection and socket server.        
def ServerCleanUp():
    global CameraCurrentlyRecording
    global StreamServerOnline
    global server_socket
    global connection
    
    if(CameraCurrentlyRecording):
        camera.stop_recording()
        CameraCurrentlyRecording = False
        
    if(StreamServerOnline):    
        # Close Streaming Socket Server
        connection.close()
        server_socket.close()
        StreamServerOnline = False
        sleep(1)


# This function is to be used to create a video recording to local,
# storage on the AxiosRoboticsRCv1 unit.            
def StartLocalRecording():
    global CameraCurrentlyRecording
    if(CameraCurrentlyRecording == False):
        camera.start_recording('CameraLocalCapture/AxiosRoboticsRCv1_VisionCameraLocal.h264')
        CameraCurrentlyRecording = True 
