from xinput import *
import ctypes
import sys
import time
from operator import itemgetter, attrgetter
from itertools import count, starmap
from pyglet import event

from pyfirmata import Arduino, util

class Controller:
    def __init__(self):
        self.mode = 'DRIVE'

    def __str__(self):
        return 'MODE: ' + str(self.mode)

    def set_mode(self, mode):
        self.mode = mode

    def get_mode(self):
        return self.mode


# def controller():
#     joysticks = XInputJoystick.enumerate_devices()
#     device_numbers = list(map(attrgetter('device_number'), joysticks))
#
#     print('found %d devices: %s' % (len(joysticks), device_numbers))
#
#     if not joysticks:
#         sys.exit(0)
#
#     j = joysticks[0]
#     print('using %d' % j.device_number)
#
#     battery = j.get_battery_information()
#     print(battery)
#
#     @j.event
#     def on_button(button, pressed):
#         # print('button', button, pressed)
#         process_input(('button', button, pressed))
#
#
#     @j.event
#     def on_axis(axis, value):
#         left_speed = 0
#         right_speed = 0
#
#         # print('axis', axis, value)
#         if axis == "left_trigger":
#             left_speed = value
#         elif axis == "right_trigger":
#             right_speed = value
#         j.set_vibration(left_speed, right_speed)
#
#         process_input(('axis', axis, value))
#
#     while True:
#         j.dispatch_events()
#         time.sleep(0.01)


def process_input(input, object):
    # Left joystick: Y values: Move forward, backward
    # Right joystick: X values: Rotate left, right
    # Input will be a tuple, joystick and value, or button and value
    # print(input)

    # print(input, object.get_mode())
    if input[0] is 'button':
        if input[1] == 3:
            object.set_mode('DIG')
        elif input[1] == 2:
            object.set_mode('DRIVE')

    if input[0] is 'axis':

        MAX_Y_VAL = 0.475
        MIN_Y_VAL = -0.475
        MAX_X_VAL = 0.475
        MIN_X_VAL = -0.475

        if input[1] is 'l_thumb_y':  # If it's the left joystick, we only want the y-values
            if not MIN_Y_VAL < input[2] < MAX_Y_VAL:
                print('Y: Max or Min')
        elif input[1] is 'r_thumb_x':  # Right joystick -> x values
            if not MIN_X_VAL < input[2] < MIN_X_VAL:
                print('X: Max or Min')






#
# def bluetooth(id):
#     bd_addr =
#     sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#     sock.connect((bd_addr, port))
#     print
#     'Connected'


if __name__ == '__main__':
    controller = Controller()

    joysticks = XInputJoystick.enumerate_devices()
    device_numbers = list(map(attrgetter('device_number'), joysticks))

    print('found %d devices: %s' % (len(joysticks), device_numbers))

    if not joysticks:
        sys.exit(0)

    j = joysticks[0]
    print('using %d' % j.device_number)

    battery = j.get_battery_information()
    print(battery)


    @j.event
    def on_button(button, pressed):
        # print('button', button, pressed)
        process_input(('button', button, pressed), controller)


    @j.event
    def on_axis(axis, value):
        left_speed = 0
        right_speed = 0

        # print('axis', axis, value)
        if axis == "left_trigger":
            left_speed = value
        elif axis == "right_trigger":
            right_speed = value
        j.set_vibration(left_speed, right_speed)

        process_input(('axis', axis, value), controller)


    while True:
        j.dispatch_events()
        time.sleep(0.01)
