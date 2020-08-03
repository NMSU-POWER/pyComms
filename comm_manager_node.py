# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# July 2020
# comm_manager_node.py
# Manage socket comms for nodes.  Node will distribute these objects, each object will have a target IP for a line
# agent.  There will be a connection established with this line agent.  This manager will reach out and touch the line
# agent to start the process.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import socket

# class will manage the connection to a line agent.
class Node_Comm:
    def __init__(self, ip, v):
        self.remote_v = 1
        self.line_y = 0
        self.node_v = v
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 8080))
        while True:
            s.sendall(str(self.node_v).encode())
            print(s.recv(1024))
