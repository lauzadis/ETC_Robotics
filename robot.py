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
import subprocess



# #### 2) CREATE A UDP SERVER CONNECTION TO THE LAPTOP ####

UDP_IP = ''
UDP_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Specify IPV6, UDP protocol
sock.bind((UDP_IP, UDP_PORT))  # double parenthesis to pass as tuple

# #### 3) RECEIVE DATA ####
while True:
    data, addr = sock.recvfrom(1024)
    data = data.decode('UTF-8')
    print(data)
    if data == 'C1':
        print(os.path.join(os.getcwd(), 'camera_robot.py'))
        camera = subprocess.Popen([sys.executable, os.path.join(os.getcwd(), 'camera_robot.py')])
    elif data == 'C0':
        camera.terminate()
    
sock.close()