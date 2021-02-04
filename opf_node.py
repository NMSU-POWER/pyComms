# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# January 2021
# opf_node.py
# Be a node and run individual DCOPF functions.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import statistics
import threading
import sys
from comm_node import NodeConnection


# Hold information pertaining to the specific bus (node)
class Node:
    def __init__(self, load, a, b, lines):
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
        self.reactanceSum = sum([1 / x.reactance for x in self.lines])
        # set up our delta in the lines
        for line in self.lines:
            line.delta[self] = self.delta
            line.powerOut[self] = 0
        # Value to distribute
        self.send_out = b'node'

    # All the node's calculations can happen in one shot
    def update_power_angle(self):
        # Update power first
        self.power = (statistics.mean([x.lineLambda for x in self.lines]) - self.a) / self.b
        # Now update self angle
        delta_reactance = []
        for line in self.lines:
            otherDelta = {}
            for node in line.delta.keys():
                if node != self:
                    otherDelta = line.delta[node]
                    delta_reactance.append((otherDelta, line.reactance))
        self.delta = (self.power - self.load + sum([x[0] / x[1] for x in delta_reactance]))/self.reactanceSum
        # Now update the power transferred out on this side of the line object
        for line in self.lines:
            line.delta[self] = self.delta
            otherDelta = 0
            for node in line.delta.keys():
                if node != self:
                    otherDelta = line.delta[node]
            line.powerOut[self] = (self.delta - otherDelta) / line.reactance
            lambdas = []
            for line_for_lambda in self.lines:
                if line_for_lambda != line:
                    lambdas.append(line_for_lambda.lineLambda)
            line.other_lambdas[self] = lambdas


if __name__ == '__main__':
    node = Node(load=0, a=1, b=.01, lines=[line1, line2])
    lines = []
    for line_ip in sys.argv[1]:
        lines.append(threading.Thread(target=NodeConnection,
                                      kwargs={'ip': line_ip, 'provvalue': node.send_out, 'port': 8080}))
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
