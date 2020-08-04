# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# July 2020
# comm_manager_node.py
# Manage socket comms for nodes.  Node will distribute these objects, each object will have a target IP for a line
# agent.  There will be a connection established with this line agent.  This manager will reach out and touch the line
# agent to start the process.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import socket
import random

# class will manage the connection to a line agent.
class Node_Comm:
    def __init__(self, ip):
        self.line_ip = ip
        self.remote_v = 1
        self.line_y = 0 # Need some way to request this from the assigned line
        self.node_v = 1
        self.is_connected = False
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ports = [8080, 8081]
        self.port = 8080

    def comm_connect(self):
        print('test1')
        failed = True
        while failed:
            self.port = self.ports[random.randint(0, len(self.ports) - 1)]
            try:
                self.connection.connect((self.line_ip, self.port))
                failed = False
            except:
                failed = True
        print('test2')
        self.is_connected = True
        self.connection.sendall(b'y')
        self.line_y = complex(self.connection.recv(1024).decode())
        while True:
            self.connection.sendall(str(self.node_v).encode())
            # This line causes a problem
            rem_v = self.connection.recv(1024).decode()
            print(rem_v)
            self.remote_v = complex(rem_v)

