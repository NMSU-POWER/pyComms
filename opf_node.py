# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# January 2021
# opf_node.py
# Be a node and run individual DCOPF functions.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import statistics
import threading
import sys
import json
import time
from comm_node import NodeConnection


# Hold information about the line in a simple object
class Line:
    def __init__(self, comm_chanel):
        self.local_delta = 0
        self.power_out = 0
        self.line_reactance = 0
        self.other_delta = 0
        self.comm_object = comm_chanel
        self.line_lambda = 0
        self.other_lambdas = []
        self.comm_object.provided_value = str({"delta": self.local_delta,
                                               "other_lambdas": self.other_lambdas,
                                               "power_out": self.power_out}).encode()

    def gather_info(self):
        recd = json.loads(self.comm_object.received_value.decode().replace("'", '"'))
        self.line_reactance = recd['reactance']
        self.other_delta = recd['other_delta']
        self.line_lambda = recd['lambda']
        self.comm_object.provided_value = str({"delta": self.local_delta,
                                               "other_lambdas": self.other_lambdas,
                                               "power_out": self.power_out}).encode()


# Hold information pertaining to the specific bus (node)
class Node:
    def __init__(self, load, a, b, lines, slack=False):
        # Initialization angle is always 0
        self.delta = 0
        # load is assigned at start (for now)
        self.load = load
        # Power initializes to 0
        self.power = 0
        # Trailing constant on power cost
        self.a = a
        # Linear component of power cost
        self.b = b
        # list of internalLine objects (or ips)
        self.lines = lines
        # reactance summation
        self.reactanceSum = sum([1 / x.line_reactance for x in self.lines])
        # set up our delta in the lines
        for line in self.lines:
            line.local_delta = self.delta
            line.power_out = 0
        # Value to distribute
        self.send_out = b'node'

    # All the node's calculations can happen in one shot
    def update_power_angle(self):
        # Update power first
        self.power = (statistics.mean([x.line_lambda for x in self.lines]) - self.a) / 2 / self.b
        # Now update self angle
        delta_reactance = []
        for line in self.lines:
            delta_reactance.append((line.other_delta, line.line_reactance))
        self.delta = (self.power - self.load + sum([x[0] / x[1] for x in delta_reactance])) / self.reactanceSum
        for line in self.lines:
            line.local_delta = self.delta
        # Now update the power transferred out on this side of the line object
        for line in self.lines:
            line.power_out = (self.delta - line.other_delta) / line.line_reactance
            lambdas = []
            for line_for_lambda in self.lines:
                if line_for_lambda != line:
                    lambdas.append(line_for_lambda.line_lambda)
            line.other_lambdas = lambdas


if __name__ == '__main__':
    comms = []
    threads = []
    print('Initializing connection objects...')
    for line_ip in sys.argv[1:]:
        comm = NodeConnection(ip=line_ip, provvalue=b'initialize', port=8080)
        comms.append(comm)
        threads.append(threading.Thread(target=comm.trade_values, daemon=True).start())
    lines = []
    print('Initializing line objects...')
    for comm in comms:
        lines.append(Line(comm))
    print('Waiting for line connections...')
    for line in lines:
        while line.comm_object.connected is False:
            continue
        line.gather_info()
    print('Initializing node...')
    node = Node(load=0, a=1, b=.005, lines=lines)
    # Time to actually run stuff
    while True:
        node.update_power_angle()
        print(node.power)
        for line in lines:
            line.gather_info()

    '''
    # Make lines
    line1 = InternalLine(admittance=1.63-57.10j)
    line2 = InternalLine(admittance=4.42-66.37j)
    line3 = InternalLine(admittance=4.95-49.50j)
    # Make nodes
    node1 = Node(load=0, a=1, b=.01, lines=[line1, line2])
    node2 = Node(load=0, a=1, b=.015, lines=[line1, line3])
    node3 = Node(load=400, a=1, b=.02, lines=[line2, line3])

    # Testing
    for i in range(100):
        node1.update_power_angle()
        node2.update_power_angle()
        node3.update_power_angle()
        line1.lambda_update()
        line2.lambda_update()
        line3.lambda_update()

        print('iteration: ' + str(i + 1))

        print(node1.power)
        print(node2.power)
        print(node3.power)

        print(line1.powerOut)
        print(line2.powerOut)
        print(line3.powerOut)
        
        print(line1.lineLambda)
        print(line2.lineLambda)
        print(line3.lineLambda)'''
