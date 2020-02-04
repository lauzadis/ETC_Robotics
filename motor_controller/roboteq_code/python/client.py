import socket

UDP_IP = '10.0.0.148'
UDP_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = ''
while True and data != 'stop':
    data = input('Data to send:')
    data = data.encode()
    sock.sendto(data, (UDP_IP, UDP_PORT))
    data = data.decode('UTF-8')

print('Received stop command!')
sock.close()
