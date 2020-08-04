# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# August 2020
# gauss_node.py
# Be a node and run individual power flow, use comms over socket instead of IP.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np
from comm_manager_node import Node_Comm
import threading


class Node:
    def __init__(self, selfV, selfS, slack=False, current_sensors=[]):
        self.selfV = 1
        self.otherV = 1
        self.selfS = selfS
        self.slack = slack
        self.selfY = 0
        self.current_sensors = current_sensors
        self.current_sensor_power = 0
        self.measuredV = selfV
        self.problem = False
        self.comms = {}

    # node_manager
    # shared_info is a class that holds the shared information to this node
    # Run power flow until we hit a stable state, update if values change anywhere
    def node_manager(self):
        errors = 0
        # Loop forever, always keep the power flow up to date
        while True:
            print(self.selfV)
            print(np.abs(self.selfV))
            print(self.selfS)
            # for line in self.lines:
            #     requests.post(line + '/pushv', params={'volts': self.selfV})
            self.gauss_voltage()
            if self.slack:
                self.power_calc()
            # print(np.abs(self.selfV))
            # print(self.measuredV)
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
        for line in self.comms.keys():
            # Old lines
            # node_info = line.volt_admittance_request(self)
            # sums -= node_info[0] * node_info[1]
            # New lines
            # v = complex(requests.get(line + '/pullv').content.decode())
            # y = complex(requests.get(line + '/pully').content.decode())
            sums -= self.otherV * self.comms[line]
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
        for line in self.comms.keys():
            # Old lines
            # node_info = line.volt_admittance_request(self)
            # I += node_info[0] * node_info[1]
            # New lines
            # v = complex(requests.get(line + '/pullv').content.decode())
            # y = complex(requests.get(line + '/pully').content.decode())
            I += self.otherV * self.comms[line]
        newS = self.selfV * np.conj(I)
        # New power, based on current voltage information
        self.selfS = newS

    def live_pf(self):
        # If list is empty, can't do anything
        if len(self.current_sensors) == 0:
            return 0
        # If we have at least one current sensor, we can detect power flowing
        power_sum = (self.selfV ** 2) * self.Yself_calc()
        # Add the rest to the power sum
        for current in self.current_sensors:
            power_sum += np.conj(current.current) * self.selfV
        # Power sum will be the net node power.  Power out - power in
        self.current_sensor_power = power_sum

    def Yself_calc(self):
        self.selfY = 1/self.selfV * (np.conj(self.current_sensor_power) / np.conj(self.selfV) - sum([x.current for x in self.current_sensors]))
        return self.selfY

    def live_current_sum(self):
        return np.sum([np.conj(x.current) * self.selfV for x in self.current_sensors])


if __name__ == '__main__':
    node = Node(1, 0, True)
    lines = ['10.0.0.234']
    comm_hold = {}
    threads = {}
    for line in lines:
        comm_hold[line] = Node_Comm(line)
        threads[line] = threading.Thread(target=comm_hold[line].comm_connect)
        threads[line].start()
        while not comm_hold[line].is_connected:
            # Below needs to become dynamic
            print('Waiting for connection to line at ' + line + ' on port ' + str(comm_hold[line].port))
        # Need to wait for connections to go through before calculating this.
        node.selfY -= comm_hold[line].line_y
        node.comms[line] = comm_hold[line].line_y
    main_thread = threading.Thread(target=node.node_manager)
    main_thread.start()
    while True:
        for line in lines:
            node.otherV = comm_hold[line].remote_v
            comm_hold[line].node_v = node.selfV
