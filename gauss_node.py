# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# August 2020
# gauss_node.py
# Be a node and run individual power flow, use comms over socket instead of IP.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np
from comm_manager_node import Node_Comm
import threading
import sys


class Node:
    def __init__(self, selfV, selfS, slack=False):
        self.selfV = 1
        self.selfS = selfS
        self.slack = slack
        self.selfY = 0
        self.measuredV = selfV
        self.problem = False
        self.lines = {}

    # node_manager
    # shared_info is a class that holds the shared information to this node
    # Run power flow until we hit a stable state, update if values change anywhere
    def node_manager(self):
        errors = 0
        # Loop forever, always keep the power flow up to date
        while True:
            self.gauss_voltage()
            if self.slack:
                self.power_calc()
            if round(np.abs(self.selfV), 4) != self.measuredV:
                errors += 1
            else:
                errors = 0
            if errors > 100:
                self.problem = True
            else:
                self.problem = False

    # gauss_voltage
    # No input argument, Node contains necessary information
    # Calculates own voltage based on current state of voltages and power
    def gauss_voltage(self):
        # Normal Gauss voltage method for a node.
        V_current = np.conj(self.selfS / self.selfV)
        sums = 0
        for key in self.lines.keys():
            sums -= self.lines[key].voltage * self.lines[key].admittance
        V_current += sums
        V_current /= self.selfY
        # Set own, distribution will automate.
        if not self.slack:
            self.selfV = V_current

    # power_calc
    # No input arguments, Node contains necessary information.
    # Calculates the power at the node with the current nodal voltage information.
    def power_calc(self):
        # I = v of each node multiplied by admittance, summation, simplifies where admittance = 0
        I = self.selfV * self.selfY
        for key in self.lines.keys():
            I += self.lines[key].voltage * self.lines[key].admittance
        newS = self.selfV * np.conj(I)
        # New power, based on current voltage information
        self.selfS = newS


# lineVals
# Hold the admittance and voltage provided by a particular line connection.
class lineVals:
    def __init__(self, admittance, voltage):
        self.admittance = admittance
        self.voltage = voltage


if __name__ == '__main__':
    # Process slack or not
    if sys.argv[2] == 'False':
        slack = False
    else:
        slack = True
    # The virtual representation of this particular device.
    node = Node(selfV=sys.argv[0], selfS=sys.argv[1], slack=slack)
    # The ip's of the lines we're connected to (will eventually be a server)
    lines = ['10.0.0.234']
    comm_hold = {}
    threads = {}
    # Set up all the communication handles and threads to run them.
    for line in lines:
        comm_hold[line] = Node_Comm(line)
        threads[line] = threading.Thread(target=comm_hold[line].communicate)
        threads[line].start()
        while not comm_hold[line].is_connected:
            # Below needs to become dynamic
            print('Waiting for connection to line at ' + line + ' on port ' + str(comm_hold[line].port))
            # x = 1
        # Collect all the admittances as soon as possible.
        while comm_hold[line].line_y is None:
            continue
        # Calculate self admittance
        node.selfY -= comm_hold[line].line_y
        # Create object to hold the admittance and voltage for calculations
        admittance = comm_hold[line].line_y
        voltage = comm_hold[line].remote_v
        node.lines[line] = lineVals(admittance, voltage)

    # Start the main thread that runs our calculations
    main_thread = threading.Thread(target=node.node_manager)
    main_thread.start()
    # The final portion of the node is a thread that will continually pull in and push out voltages for the interface.
    while True:
        for line in lines:
            node.lines[line].voltage = comm_hold[line].remote_v
            comm_hold[line].node_v = node.selfV
