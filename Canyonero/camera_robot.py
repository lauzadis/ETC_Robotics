#!/home/codetc/anaconda3/bin/python

import cv2
import socket
import struct
import time
import pickle

fps = 10
previous_time = 0 

HOST_IP = '10.0.0.83'
HOST_PORT = 8485

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST_IP, HOST_PORT))

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320);  # Width
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240);  # Height

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    elapsed_time = time.time() - previous_time
    ret, frame = cam.read()
    
    if elapsed_time > 1/fps:
        previous_time = time.time()
        result, frame = cv2.imencode('.jpg', frame, encode_param)  

        data = pickle.dumps(frame, 0)
        size = len(data)

        client_socket.sendall(struct.pack(">L", size) + data)

cam.release()
client_socket.close()