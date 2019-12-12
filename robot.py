#!/home/codetc/anaconda3/bin/python

###########################################
#  Name: robot.py                         #
#  Author: Matas Lauzadis                 #
#  Description: NASA 2020 Lunabotics Code #
###########################################

import socket # for sending data
import time  # for sleeping
import os
import sys
from roboteq import RoboteqDevice  # Motor Controller
from roboteq.roboteq_constants import _RWD, _G

if not os.geteuid() == 0:
    sys.exit('Only root can run this script')


#### 1) CONNECT TO THE ROBOTEQ DEVICES ####

# Either device_path works, I prefer /serial/by-id because
# it's easier to see that it's a Roboteq Controller by the name

# device_path = '/dev/serial/by-id/usb-Roboteq_Motor_Controller_MDC2XXX-if00'
device_path = '/dev/ttyACM0'

device = RoboteqDevice()
device.connect(device_path)

if(device.is_roboteq_connected):
    print('All connected!')
else:
    print('Failed to find Roboteq')
    raise KeyboardInterrupt

device.set_config(_RWD, 0)  # Disable RS232 Watchdog
time.sleep(0.1)


# #### 2) CREATE A UDP SERVER CONNECTION TO THE LAPTOP ####

UDP_IP = '10.0.0.148'
UDP_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Specify IPV6, UDP protocol
sock.bind((UDP_IP, UDP_PORT))  # double parenthesis to pass as tuple

# #### 3) RECEIVE DATA! :) ####
data = ''
while True and data != 'stop':
    data, addr = sock.recvfrom(1024) # Buffer size is 1024 bytes
    data=data.decode('UTF-8')
    print('received message:', data)

    data = data.split(' ')
    
    print(type(data[0]))
    print(type(data[1]))
    data[1] = int(data[1])

    if data[0] == 'forward':
        device.command_motor(_G, 1, data[1])
        time.sleep(2)
    elif data[0] == 'back':
        device.command_motor(_G, 1, data[1])
    

print('Received stop command!')
sock.close()