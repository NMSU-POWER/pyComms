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
import time

# class will manage the connection to a line agent.
class Node_Comm:
    def __init__(self, ip):
        self.line_ip = ip
        self.remote_v = complex('-inf')
        self.line_y = None
        self.node_v = 1j
        self.is_connected = False
        self.connection = None
        self.ports = [8080, 8081]
        self.port = self.ports[0]

    #
    # comm_connect
    # connect to the line agent at the provided IP on one of two ports. Doesn't matter which.
    def comm_connect(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        failed = True
        while failed:
            self.port = self.ports[random.randint(0, len(self.ports) - 1)]
            try:
                self.connection.connect((self.line_ip, self.port))
                failed = False
            except:
                failed = True
        self.is_connected = True

    #
    # communicate
    # send our own voltage, receive the other node's voltage.  Request admittance once and store.
    def communicate(self):
        try:
            self.comm_connect()
            self.connection.sendall(b'y')
            y = self.connection.recv(1024).decode()
            self.line_y = complex(y)
            while True:
                self.connection.sendall(str(self.node_v).encode())
                self.connection.settimeout(1)
                self.remote_v = complex(self.connection.recv(1024).decode())
        except:
            self.remote_v = complex('-inf')
            self.connection.close()
            self.communicate()

