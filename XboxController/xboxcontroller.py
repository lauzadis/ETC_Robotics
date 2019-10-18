from xinput import *
import ctypes
import sys
import time
from operator import itemgetter, attrgetter
from itertools import count, starmap
from pyglet import event

from pyfirmata import Arduino, util


def controller():
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
        process_input(('button', button, pressed))


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

        process_input(('axis', axis, value))

    while True:
        j.dispatch_events()
        time.sleep(0.01)


def process_input(input):
    # Left joystick: Y values: Move forward, backward
    # Right joystick: X values: Rotate left, right
    # Input will be a tuple, joystick and value, or button and value
    # print(input)
    if input[0] is 'button':
        print(input)

        if input[1] == 3 and input[2] == 1:
            print('Dig Mode')
        elif input[1] == 2 and input[2] == 1:
            print('Drive Mode')

    if input[0] is 'axis':
        value = input[2]

        max_value_joystick = 0.475
        min_value_joystick = -0.475

        if -0.1 < value < 0.1:
            pass
        # elif value > max_value:
        #     print('Max Value')
        #     # Send full power to motor
        #
        # elif value < min_value:
        #     print('Min Value')
            # Send full power to motor

        #Otherwise, scale the value


#
# def bluetooth(id):
#     bd_addr =
#     sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#     sock.connect((bd_addr, port))
#     print
#     'Connected'


if __name__ == '__main__':
    controller()