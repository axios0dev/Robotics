#!/usr/bin/env python3
# This module contains the code to create a socket server and establish a TCP,
# connection to a VLC client for live viewing of the video feed from the camera,
# on top of the AxiosRoboticsRCv1 unit.
# To establish a connection to this server open the following network stream on a,
# VLC client on a computer connected to the same local network as the AxiosRoboticsRCv1 unit.
# tcp/h264://ip_address_of_unit:8000/

# Python library imports.
from  picamera import PiCamera
from socket import socket
from time import sleep
from threading import Thread, Event
# AxiosRoboticsRCv1 unit modules.
from Modules.LedSubsystem import TailLightController

# PiCamera object instantiation and parameter setup.
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = (24)
sleep(2)

# State flag to keep track of when the camera module resource is in use
# by this controller.
CameraCurrentlyRecording = False
# TCP socket server state flag and server variables.
StreamServerOnline = False
ServerSocket = None
TCPConnection = None


# This function creates a socket server and establishes a TCP connection to a VLC client
# on the same local network as the AxiosRoboticsRCv1 unit.
def StreamServerStart():
    # Global variable linkage.
    global StreamServerOnline
    global ServerSocket
    global TCPConnection
    
    # TCP socket server setup. 
    ServerSocket = socket()
    ServerSocket.bind(('0.0.0.0', 8000))
    ServerSocket.listen(0)
    
    # While waiting for a VLC client connection to be established, spawn a second thread 
    # and run the sync light subroutine so the operator can easily tell when the unit is 
    # waiting for a connection.
    # Create an event flag to determine when to terminate the second thread.
    WaitingForTCPConnection = Event()
    WaitingForTCPConnection.set()
    # Start the SyncIndicators subroutine while waiting for the TCP connection.
    Thread(target=TailLightController.SyncIndicators, args=(WaitingForTCPConnection,)).start()
    # Wait for and establish a TCP connection with a VLC client.
    TCPConnection = ServerSocket.accept()[0].makefile('wb')
    # Clear the event state once the connection is established, this terminates the SyncIndicator thread.
    WaitingForTCPConnection.clear()
    # Set the server online state.
    StreamServerOnline = True
    
    
# Start streaming live video from the AxiosRoboticsRCv1 unit over the TCP
# connection file descriptor.
def VideoStreamStart():
    # Global variable linkage.
    global CameraCurrentlyRecording
    global StreamServerOnline
    global TCPConnection
    
    # If the TCP socket server has not been started start the server and establish
    # a client connection.
    if (not StreamServerOnline):
        StreamServerStart()
     
    # Start streaming video over the established TCP connection.    
    if(not CameraCurrentlyRecording):
        camera.start_recording(TCPConnection, format='h264')
        CameraCurrentlyRecording = True
    # If this is called while a the video feed is active stop the video feed.    
    elif(CameraCurrentlyRecording):
        StopVideo()


# Stop the video feed from the camera module.        
def StopVideo():
    # Global variable linkage.
    global CameraCurrentlyRecording
    # Check if the camera is currently in use
    # and if so stop recording.
    if(CameraCurrentlyRecording == True):
        camera.stop_recording()
        CameraCurrentlyRecording = False


# This function needs to be called before exiting the program to
# close the active TCP connection and socket server.        
def ServerCleanUp():
    # Global variable linkage.
    global CameraCurrentlyRecording
    global StreamServerOnline
    global ServerSocket
    global TCPConnection
    
    # If the camera is currently active stop recording.
    if(CameraCurrentlyRecording):
        camera.stop_recording()
        CameraCurrentlyRecording = False
    
    # If the TCP socket server is active clean up the connection
    # and the server.    
    if(StreamServerOnline): 
        # Close Streaming Socket Server and active TCP connection.
        TCPConnection.close()
        ServerSocket.close()
        StreamServerOnline = False
        sleep(1)


# This function is to be used to capture a video recording to local
# storage on the AxiosRoboticsRCv1 unit.            
def StartLocalRecording():
    # Global variable linkage.
    global CameraCurrentlyRecording
    # Check to ensure the camera is not currently recording then
    # start recording to local storage.
    if(CameraCurrentlyRecording == False):
        camera.start_recording('CameraLocalCapture/AxiosRoboticsRCv1_VisionCameraLocal.h264')
        CameraCurrentlyRecording = True 
