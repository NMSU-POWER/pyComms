# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# August 2020
# central_observer.py
# Observes the voltage of the distributed nodes.  Provides each node with a list of lines connected.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import socket
import threading
import time

class comm_handle:
    def __init__(self, connection, addr):
        self.connection = connection
        self.addr = addr
        self.voltage = 1

    def communicate(self):
        try:
            while True:
                self.voltage = complex(self.connection.recv(1024).decode())
                self.connection.sendall(b'ack')
        except:
            self.voltage = complex('-inf')


connection_list = []


def accept_connections():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 8080))
    s.listen(5)
    while True:
        conn, address = s.accept()
        comm = comm_handle(conn, address)
        connection_list.append(comm)
        threading.Thread(target=comm.communicate).start()


if __name__ == "__main__":
    # Accept forever
    threading.Thread(target=accept_connections).start()
    # print the values in the comm handles
    while True:
        for node in connection_list:
            if node.voltage == complex('-inf'):
                connection_list.remove(node)
                continue
            print('v @ ' + str(node.addr[0]) + ': ' + str(node.voltage))
        print('list complete.\n')
        time.sleep(2)
