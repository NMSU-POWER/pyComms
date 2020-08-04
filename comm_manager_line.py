# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# July 2020
# comm_manager_line.py
# Manage communicaitons as a line.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import socket

# Accept any incoming connections, then reconnect for out-going?
class Line_comm:
    def __init__(self, y, v=b'1'):
        # v is the voltage of the node connected to this object
        self.v = v
        # other_v is the voltage of the other node connected to the respective line, essentially the voltage the node is
        # communicating to get
        self.other_v = v
        self.y = y
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def comm_connect(self, port):
        self.s.bind(('', port))
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()
        print('connected on port ' + str(port))

    def communicate(self):
        while True:
            val = self.conn.recv(1024)
            if val.decode() == 'y':
                self.conn.sendall(self.y)
            else:
                self.v = val
                self.conn.sendall(self.other_v)
