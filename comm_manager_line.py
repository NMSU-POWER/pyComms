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
        # The provided admittance will be provided as requested
        self.y = y
        # The connection to be used in the whole object
        self.conn = None

    #
    # comm_connect
    # connect to the first node that sends a connection on the provided port.
    def comm_connect(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port))
        s.listen(1)
        self.conn, _ = s.accept()
        print('connected on port ' + str(port))

    #
    # communicate
    # Continually send and receive the respective voltage values or the admittance when requested.
    def communicate(self):
        while True:
            val = self.conn.recv(1024)
            if val.decode() == 'y':
                self.conn.sendall(self.y)
            else:
                self.v = val
                self.conn.sendall(self.other_v)
