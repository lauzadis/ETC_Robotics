from xinput import *
import ctypes
import sys
import time
from operator import itemgetter, attrgetter
from itertools import count, starmap
from pyglet import event

from pyfirmata import Arduino, util

import socket


class Controller:
    def __init__(self):
        self.mode = 'DRIVE'

    def __str__(self):
        return 'MODE: ' + str(self.mode)

    def set_mode(self, mode):
        self.mode = mode

    def get_mode(self):
        return self.mode



def translate_button(number):
    buttons = ['PLACEHOLDER', 'DPAD_UP', 'DPAD_DOWN', 'DPAD_LEFT', 'DPAD_RIGHT', 'START', 'SELECT', 'LEFT_STICK',
               'RIGHT_STICK', 'LEFT_BUMPER', 'RIGHT_BUMPER', 'N/A (11)', 'N/A (12)', 'A', 'B', 'X', 'Y']
    return buttons[number]


def process_input(input, object):
    # Left joystick: Y values: Move forward, backward
    # Right joystick: X values: Rotate left, right
    # Input will be a tuple, joystick and value, or button and value

    type, id, value = input
    # type = input[0]
    # id = input[1]
    # value = input[2]

    if type is 'button' and value is 1:
        ###########
        # BUTTONS #
        ###########
        button_name = translate_button(id)
            # DIG MODES
        if button_name is 'DPAD_UP':  # If button 3 is pressed
            if object.get_mode() is not 'DIG':
                object.set_mode('DIG')
                print('Switched to Dig Mode')
        elif button_name is 'DPAD_DOWN':
            if object.get_mode() is not 'DRIVE':
                object.set_mode('DRIVE')
                print('Switched to Drive Mode')

            # Decipher Button Presses
        return button_name

    if type is 'axis':
        # Max and Min values for the joystick's X and Y values.
        # If the joystick is above this value, it will automatically be set to 0.5 or -0.5.

        MAX_Y_VAL = 0.45
        MIN_Y_VAL = -0.45
        MAX_X_VAL = 0.45
        MIN_X_VAL = -0.45

        if id is 'l_thumb_y':  # If it's the left joystick, we only want the y-values
            if value > MAX_Y_VAL:
                value = 0.5
            elif value < MIN_Y_VAL:
                value = -0.5
            print(type, id, value)

        elif id is 'r_thumb_x':  # Right joystick -> x-value
            if value > MAX_X_VAL:
                value = 0.5
            elif value < MIN_X_VAL:
                value = -0.5
            print(type, id, value)


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
