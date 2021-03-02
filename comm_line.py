# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# February 2021
# comm_node.py
# Connection tool to be used by nodes to reach out to the line objects.  General purpose
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import socket


class LineConnection:
    def __init__(self, provvalue, port):
        print('Initializing line connection...')
        self.received_value = None
        self.provided_value = provvalue
        self.port = port
        self.connection = None
        self.connected = False

    def trade_values(self):
        disconnected = True
        while disconnected:
            try:
                print('Connecting...')
                self.connected = False
                self.connect()
                print('Connected...')
                while True:
                    self.received_value = self.connection.recv(1024)
                    # print(self.received_value)
                    self.connection.sendall(self.provided_value)
                    self.connected = True
            except Exception as e:
                print(e)
                disconnected = True

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', self.port))
        s.listen(0)
        self.connection, addr = s.accept()


if __name__ == "__main__":
    line = LineConnection(b'test1')