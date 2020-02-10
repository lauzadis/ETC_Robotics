import socket
from inputs import devices, get_gamepad
from controller import Controller
import pyttsx3
import random

import subprocess

MAX_RPM = 200  # max value that we want to send to the motor
MAX_CONTROLLER_VALUE = 32768  # max value that the xbox controller reads
NEW_EVENT_THRESHOLD = 0.075  # percent delta to consider the incoming event a new event
DEADZONE_THRESHOLD = 0.10 # percent of the MAX_CONTROLLER_VALUE needed to consider outside of the deadzone

# NUC_IP = '192.168.1.73'
NUC_IP = '10.0.0.152'
NUC_PORT = 12345

key = {'ABS_Y': 'L', 
       'ABS_RY': 'R'
       }


def main():
    tts = pyttsx3.init()
    tts.setProperty('rate',150)

    motor_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    controller = Controller()
    print(controller.get_mode())

    previous_event = 0
    bytes_sent = 0


    while True:
        events = get_gamepad()        
        
        for event in events:
            command = controller.get_command(event)
            if command is not None:
                if command.decode() == 'C1':  # Create Camera Socket
                    motor_sock.sendto(command, (NUC_IP, NUC_PORT))
                    camera = subprocess.Popen('./server_cv.py')
                    controller.camera_feed = True

                elif command.decode() == 'C0':
                    motor_sock.sendto(command, (NUC_IP, NUC_PORT))
                    camera.terminate()
                    controller.camera_feed = False

                else:
                    print(command)
                    motor_sock.sendto(command, (NUC_IP, NUC_PORT))
if __name__ == '__main__':
    main()