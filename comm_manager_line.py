# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# July 2020
# comm_manager_line.py
# Manage communicaitons as a line.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import socket


# Accept any incoming connections, then reconnect for out-going?
class Line_comm:
    def __init__(self, y, port):
        # v is the voltage of the node connected to this object
        self.v = b'1'
        # other_v is the voltage of the other node connected to the respective line, essentially the voltage the node is
        # communicating to get
        self.other_v = b'1'
        # The provided admittance will be provided as requested
        self.y = y
        # The connection to be used in the whole object
        self.conn = None
        # The assigned port
        self.port = port

    #
    # comm_connect
    # connect to the first node that sends a connection on the provided port.
    def comm_connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', self.port))
        s.listen(1)
        self.conn, _ = s.accept()
        print('connected on port ' + str(self.port))

    #
    # communicate
    # Continually send and receive the respective voltage values or the admittance when requested.
    def communicate(self):
        self.comm_connect()
        while True:
            val = self.conn.recv(1024)
            if val.decode() == 'y':
                self.conn.sendall(self.y)
            else:
                self.v = val
                self.conn.sendall(self.other_v)
