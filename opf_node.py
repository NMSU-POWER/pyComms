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
        try:
            recd = json.loads(self.comm_object.received_value.decode().replace("'", '"'))
        except Exception as e:
            print(e)
            return
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
    for line_ip in sys.argv[4:]:
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
    node = Node(load=float(sys.argv[1]), a=float(sys.argv[2]), b=float(sys.argv[3]), lines=lines)
    # Time to actually run stuff
    while True:
        node.update_power_angle()
        print(node.power)
        for line in lines:
            line.gather_info()
