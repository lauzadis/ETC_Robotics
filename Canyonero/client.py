import socket
from inputs import devices, get_gamepad
from controller import Controller

MAX_RPM = 200  # max value that we want to send to the motor
MAX_CONTROLLER_VALUE = 32768  # max value that the xbox controller reads
NEW_EVENT_THRESHOLD = 0.075  # percent delta to consider the incoming event a new event
DEADZONE_THRESHOLD = 0.10 # percent of the MAX_CONTROLLER_VALUE needed to consider outside of the deadzone

NUC_IP = '192.168.1.73'
NUC_PORT = 12345

key = {'ABS_Y': 'left', 
       'ABS_RY': 'right'
       }


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    controller = Controller()
    print(controller.get_mode())

    previous_event = 0

    while True:
        events = get_gamepad()        
        
        for event in events:
            if event.code == 'ABS_Y' or event.code == 'ABS_RY':
                
                # Deadzone check
                if -1*MAX_CONTROLLER_VALUE*DEADZONE_THRESHOLD < event.state < MAX_CONTROLLER_VALUE*DEADZONE_THRESHOLD:
                    event.state = 0

                # New event check
                delta = abs(previous_event - event.state)
                if -1*NEW_EVENT_THRESHOLD*MAX_CONTROLLER_VALUE < delta < NEW_EVENT_THRESHOLD * MAX_CONTROLLER_VALUE:
                    break

                else:  # command is new and outside of the deadzone
                    scaled_state = event.state / MAX_CONTROLLER_VALUE * MAX_RPM * -1   # scale down the controller input to our maximum motor input
                    command = (key[event.code] + ' ' + str(scaled_state)).encode()
                    previous_event = event.state

                print(command)
                sock.sendto(command, (NUC_IP, NUC_PORT))
                

if __name__ == '__main__':
    main()