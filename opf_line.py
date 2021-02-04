# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# February 2021
# opf_line.py
# Be a line and run individual DCOPF functions.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import statistics
import threading
from comm_line import LineConnection

# Global for now, constant that affects how quickly a node changes lambda.
alpha = -.01


# Hold information about the line connected to the node objects
class Line:
    def __init__(self, admittance):
        print('Initializing line object...')
        # Delta of the node at the other end
        self.delta = {}
        # Admittance of this line
        self.admittance = admittance
        # reactance of the line
        self.reactance = (1/self.admittance).imag
        # The lambda of this line
        self.lineLambda = 0
        # Power being pushed into the line from this side of a node
        self.powerOut = {}
        # Lists of other lambdas
        self.other_lambdas = {}
        # Value to send
        self.send_out = str({"reactance": self.reactance}).encode()

    def lambda_update(self):
        collected_lambdas = []
        power_out = 0
        for node in self.other_lambdas.keys():
            collected_lambdas.extend(self.other_lambdas[node])
            power_out += self.powerOut[node]
        self.lineLambda = self.lineLambda + power_out * alpha
        collected_lambdas.append(self.lineLambda)
        self.lineLambda = statistics.mean(collected_lambdas)


# Set up the line object and the connections, manage the values provided to the line
if __name__ == "__main__":
    line = Line(admittance=1.63-57.10j)
    node_con_1 = threading.Thread(target=LineConnection, kwargs={'provvalue': line.send_out, 'port': 8080}).start()
    node_con_2 = threading.Thread(target=LineConnection, kwargs={'provvalue': line.send_out, 'port': 8081}).start()
    # Loop continually.  Alternate between updating the lambda and passing around new values
    while True:
        line.lambda_update()
        # Need to update values passed around
        # Get the node working first
