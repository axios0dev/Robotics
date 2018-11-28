#!/bin/bash
cd home/pi/Documents/python
sudo python bluetoothkbd.py
@reboot sleep 20 && /bin/echo -e 'connect 00:00:00:00:2A:7D \n' | bluetoothct1

