# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# February 2021
# comm_node.py
# Connection tool to be used by nodes to reach out to the line objects.  General purpose
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import socket

class NodeConnection:
    def __init__(self, ip, provvalue, port):
        self.provided_value = provvalue
        self.received_value = None
        self.ip = ip
        self.origin_port = port
        self.port = port
        self.connection = None
        self.connected = False

    def connect(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port))

    def trade_values(self):
        disconnected = True
        while disconnected:
            try:
                print('Connecting...')
                self.connected = False
                self.connect()
                print('Connected...')
                while True:
                    self.connection.sendall(self.provided_value)
                    self.received_value = self.connection.recv(1024)
                    # print(self.received_value)
                    self.connected = True
            except Exception as e:
                print(e)
                if self.port == self.origin_port:
                    self.port = self.port + 1
                else:
                    self.port = self.port - 1
                disconnected = True


if __name__ == "__main__":
    connection = NodeConnection('10.0.0.10', b'test1', 8081)
    connection.trade_values()
