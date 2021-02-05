# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# February 2021
# opf_line.py
# Be a line and run individual DCOPF functions.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import statistics
import threading
import json
import time
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
        self.power_out = 0
        # Lists of other lambdas
        self.other_lambdas = []
        # node's last power out
        self.node1_last_power = 0
        self.node2_last_power = 0
        # Value to send
        self.send_out = str({"reactance": self.reactance,
                             "other_delta": 0,
                             "lambda": 0}).encode()

    def lambda_update(self):
        self.lineLambda = self.lineLambda + self.power_out * alpha
        self.other_lambdas.append(self.lineLambda)
        self.lineLambda = statistics.mean(self.other_lambdas)

    def gather_info(self, node1, node2):
        self.other_lambdas = []
        recval1 = json.loads(node1.received_value.decode().replace("'", '"'))
        recval2 = json.loads(node2.received_value.decode().replace("'", '"'))
        self.other_lambdas.extend(recval1['other_lambdas'])
        self.other_lambdas.extend(recval2['other_lambdas'])
        self.delta[node2] = recval2['delta']
        self.delta[node1] = recval1['delta']
        self.power_out = recval2['power_out']
        self.power_out += recval1['power_out']
        last_n1_power = recval1['power_out']
        last_n2_power = recval2['power_out']
        # Update lambda
        if last_n1_power != self.node1_last_power and last_n2_power != self.node2_last_power:
            self.node1_last_power = last_n1_power
            self.node2_last_power = last_n2_power
            self.lambda_update()
        # Prep objects for sendout
        sendout1 = {}
        sendout2 = {}
        sendout1['reactance'] = self.reactance
        sendout2['reactance'] = self.reactance
        sendout1['other_delta'] = self.delta[node2]
        sendout2['other_delta'] = self.delta[node1]
        sendout1['lambda'] = self.lineLambda
        sendout2['lambda'] = self.lineLambda
        node1.provided_value = str(sendout1).encode()
        node2.provided_value = str(sendout2).encode()


# Set up the line object and the connections, manage the values provided to the line
if __name__ == "__main__":
    line = Line(admittance=1.63-57.10j)
    node_con_1 = LineConnection(provvalue=line.send_out, port=8080)
    node_con_2 = LineConnection(provvalue=line.send_out, port=8081)
    thread1 = threading.Thread(target=node_con_1.trade_values, daemon=True).start()
    while node_con_1.connected is False:
        continue
    thread2 = threading.Thread(target=node_con_2.trade_values, daemon=True).start()
    while node_con_2.connected is False:
        continue
    # Loop continually.  Alternate between updating the lambda and passing around new values
    while True:
        while node_con_1.connected is False:
            continue
        while node_con_2.connected is False:
            continue
        line.gather_info(node_con_1, node_con_2)
        print(line.lineLambda)
