# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# February 2021
# comm_node.py
# Connection tool to be used by nodes to reach out to the line objects.  General purpose
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import socket


class LineConnection:
    def __init__(self):
        self.received_value = b'recline'
        self.provided_value = b'sendline'
        self.connection = None
        disconnected = True
        while disconnected:
            try:
                self.connect()
                while True:
                    self.received_value = self.connection.recv(1024)
                    print(self.received_value)
                    self.connection.sendall(self.provided_value)
            except Exception as e:
                print(e)
                disconnected = True

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 8080))
        s.listen(0)
        self.connection, addr = s.accept()


if __name__ == "__main__":
    line = LineConnection()