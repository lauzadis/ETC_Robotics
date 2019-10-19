import sys
import socket
from xboxcontroller import send_data


def server(port=10000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()
        connection, address = s.accept()
        with connection:
            print('Connected by', address)
            while True:
                data = bytes(send_data)
                connection.sendall(data)



def client(port=10000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', port))
        while True:
            data = s.recv(1024)
            if not data:
                break
            print(data)

    print('Received', repr(data))
