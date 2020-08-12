# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# August 2020
# comm_manager_central.py
# Send communication data to the central computer.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import socket


class central_comm_manager:
    def __init__(self, central_ip):
        self.central_ip = central_ip
        self.v = 1
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect
    # continually try to connect until a connection is made.
    def connect(self):
        while True:
            try:
                self.connection.connect((self.central_ip, 8080))
                break
            except:
                continue

    def communicate(self):
        self.connect()
        while True:
            self.connection.sendall(str(self.v).encode())
