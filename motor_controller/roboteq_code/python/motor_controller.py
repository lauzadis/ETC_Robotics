import time  # for sleeping

from roboteq import RoboteqDevice
from roboteq.roboteq_constants import _MMOD, _G, _RWD, _MXMD, _MXRPM


# def connect(port, baudrate=115200, attempts=10):
#     attempt = 1
#     device = RoboteqDevice()
#
#     if not device.connect(port, baudrate):
#         while not device.connect(port, baudrate):
#             print('Attempt:', attempt)
#             attempt += 1
#             if attempt > attempts:
#                 print('Connection Timed Out')
#                 return -1
#             time.sleep(1)
#
#     return device
# device = connect('/dev/ttyS0')

device = RoboteqDevice()
device.connect('/dev/ttyACM0/')