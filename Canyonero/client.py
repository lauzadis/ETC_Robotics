import socket
from inputs import devices, get_gamepad
from controller import Controller
import time
import inputs
import numpy as np

DEBUG = True

MAX_RPM = 7500
MAX_CONTROLLER_VALUE = 32768
UDP_IP = '192.168.1.73'
UDP_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
controller = Controller()
print(controller.get_mode())


previous_event = inputs.InputEvent(device=None, event_info={'ev_type':'Absolute', 'state':0,'timestamp':1580619544.768838,'code':'ABS_Y'})
# print('Previous Event', previous_event.state)

while True:
    events = get_gamepad()        
    
    for event in events:
        if event.code == 'ABS_Y' or 'ABS_RY':
            
            if -5000 < event.state < 5000:
                event.state = 0
                        
            if np.isclose(event.state, previous_event.state, rtol=0.1, atol=0.1):
                # print('same event')
                break
            # else:
                # print('Previous:', previous_event.state, 'New:', event.state)

            
            scaled_state = event.state / MAX_CONTROLLER_VALUE * MAX_RPM   # scale down the input

            if event.code == 'ABS_Y':  # Left Joystick
                data = ('left ' + str(scaled_state)).encode()
            elif event.code == 'ABS_RY':  # Right Joystick
                data = ('right ' + str(scaled_state)).encode()

            print(data)
            sock.sendto(data, (UDP_IP, UDP_PORT))
            previous_event = event

    




