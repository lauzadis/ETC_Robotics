# from inputs import get_gamepad
import time


class Controller:
    def __init__(self):
        self.mode = 'DRIVE'

    def __str__(self):
        return 'MODE: ' + str(self.mode)

    def set_mode(self, mode):
        self.mode = mode

    def get_mode(self):
        return self.mode




def drive_mode(controller, ev_type, code, state):
    # JOYSTICKS / DPAD
    if ev_type == 'Absolute':
        # Left Joystick - Up and Down
        if code == 'ABS_Y' and (state > 5000 or state < -5000):
            print('Y:', state)
        
        # Right Joystick - Left and Right
        elif code == 'ABS_RX' and (state > 5000 or state < -5000):
            print('X:', state)
        
        # DPAD Up / Down
        elif code == 'ABS_HAT0Y':
            if state == -1:
                print('DPAD Up')
                controller.set_mode('DIG')
                print('Switched to Dig Mode')
                
            elif state == 1:
                print('DPAD Down')
        
        # DPAD Left / Right
        elif code == 'ABS_HAT0X':
            if state == -1:
                print('DPAD Left')
            elif state == 1:
                print('DPAD Right')
             
    elif event.ev_type == 'Key':
        print(code, state)
    return


def dig_mode(controller, ev_type, code, state):
    # JOYSTICKS / DPAD
    if ev_type == 'Absolute':
        # Left Joystick - Up and Down
        if code == 'ABS_Y':
            print('Y:', state)
        
        # Right Joystick - Left and Right
        elif code == 'ABS_RX':
            print('X:', state)
        
        # DPAD Up / Down
        elif code == 'ABS_HAT0Y':
            if state == -1:
                print('DPAD Up')
                
            elif state == 1:
                print('DPAD Down')
                controller.set_mode('DRIVE')
                print('Switched to Drive Mode')
        
        # DPAD Left / Right
        elif code == 'ABS_HAT0X':
            if state == -1:
                print('DPAD Left')
            elif state == 1:
                print('DPAD Right')
             
    elif event.ev_type == 'Key':
        print(code, state)
    return
    
    
    
    
if __name__ == '__main__':
    debug = False
    controller = Controller()
    while True:
        events = get_gamepad()
        for event in events:
            if debug:
                print(event.ev_type, event.code, event.state)
            elif controller.get_mode() == 'DRIVE':
                drive_mode(controller, event.ev_type, event.code, event.state)
            elif controller.get_mode() == 'DIG':
                dig_mode(controller, event.ev_type, event.code, event.state)
            
    # time.sleep(_PING/1000)