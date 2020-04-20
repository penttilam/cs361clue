#!/usr/bin/env python3

import socket

HOST = '2a02:4780:1:1::1:94bb'
PORT = 42069

with socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0) as server:
    server.bind((HOST, PORT, 0, 0))
    server.listen()
    conn, addr = server.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv()
            if not data:
                break
            conn.sendall(data)
