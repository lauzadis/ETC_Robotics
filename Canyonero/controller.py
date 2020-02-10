class Controller:
    def __init__(self):
        self.mode = 'DRIVE'
        self.MAX_RPM = 200  # max value that we want to send to the motor
        self.MAX_CONTROLLER_VALUE = 32768  # max value that the xbox controller reads
        self.NEW_EVENT_THRESHOLD = 0.075  # percent delta to consider the incoming event a new event
        self.DEADZONE_THRESHOLD = 0.10 # percent of the MAX_CONTROLLER_VALUE needed to consider outside of the deadzone
        self.previous_event = 0  # value of the previous event
        self.bytes_sent = 0  # total bytes sent
        self.mode_key = {'ABS_HAT0Y:-1':'DRIVE',
                         'ABS_HAT0X:-1':'DIG',
                         'ABS_HAT0X:1':'AUTO'
                         }
                         
        self.camera_feed = False

    def set_mode(self, mode):
        if self.mode != mode:
            print('Switched to', mode)
            self.mode = mode
        else:
            print('Already in', mode)


    def get_mode(self):
        return self.mode


    def get_command(self, event):
        
        # Joystick Operations
        if event.code == 'ABS_Y' or event.code == 'ABS_RY':
                # Deadzone check
                if -1*self.MAX_CONTROLLER_VALUE*self.DEADZONE_THRESHOLD < event.state < self.MAX_CONTROLLER_VALUE*self.DEADZONE_THRESHOLD:
                    event.state = 0

                # New event check
                delta = abs(self.previous_event - event.state)
                if -1*self.NEW_EVENT_THRESHOLD*self.MAX_CONTROLLER_VALUE < delta < self.NEW_EVENT_THRESHOLD * self.MAX_CONTROLLER_VALUE:
                    return None
                
                self.previous_event = event.state
                event.state = int(event.state / self.MAX_CONTROLLER_VALUE * self.MAX_RPM * -1)  # scale down the controller input to our maximum motor input

        # Switch Controller Modes
        elif event.code + ':' + str(event.state) in self.mode_key:
            self.set_mode(self.mode_key[event.code+':'+str(event.state)])
            return None

         # Report Bytes Sent
        elif event.code == 'ABS_HAT0Y' and event.state == 1:
            print('Bytes sent:', self.bytes_sent)
            return None

        # Activate Camera Feed
        elif event.code == 'BTN_TL' and event.state == 1:  # Left Button
            if not self.camera_feed:
                return ('C1').encode()
            else:
                return ('C0').encode()

        # Scale Up/Down MAX_RPM
        elif event.code == 'ABS_Z' and event.state == 1023:  # Left Trigger
            self.MAX_RPM -= 50
            print('MAX_RPM:', self.MAX_RPM)
        elif event.code == 'ABS_RZ' and event.state == 1023:  # Right Trigger
            self.MAX_RPM += 50
            print('MAX_RPM:', self.MAX_RPM)


        if self.mode == 'DRIVE':
            return self.drive_mode(event)
        elif self.mode == 'AUTO':
            return self.autonomy_mode(event)
        elif self.mode == 'DIG':
            return self.dig_mode(event)


    def drive_mode(self, event):
        motor_key = {'ABS_Y': 'L',  # Left Joystick --> Left Side Tank
                     'ABS_RY': 'R'  # Right Joystick --> Right Side Tank
                     }

        if event.code in motor_key:
            command = (motor_key[event.code] + str(event.state)).encode()
            self.bytes_sent += len(command)
            return command

        return None
        

    def autonomy_mode(self, event):
        print('Robot is in autonomy mode. Dpad-Up -> Drive Mode. Dpad-Left -> Dig Mode.')
        return None

    def dig_mode(self, event):
        motor_key = {'ABS_Y':'D',}  # Left Joystick --> Roller Motor Speed
        return None


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
    exit(0)