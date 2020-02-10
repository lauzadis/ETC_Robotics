#!/usr/bin/env python

import socket
import cv2
import pickle
import struct

HOST = ''
PORT=8485

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(10)

conn, addr = s.accept()

data = b''
payload_size = struct.calcsize('>L')

while True:
	while len(data) < payload_size:
		data += conn.recv(4096)

	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack('>L', packed_msg_size)[0]

	while len(data) < msg_size:
		data += conn.recv(4096)

	frame_data = data[:msg_size]
	data = data[msg_size:]

	frame = pickle.loads(frame_data, fix_imports=True, encoding='bytes')
	frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

	cv2.imshow('ImageWindow', frame)
	cv2.waitKey(1)
