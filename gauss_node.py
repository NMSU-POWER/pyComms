# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# May 2020
# gauss_node.py
# Be a node and run individual power flow.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np


class Node:
    def __init__(self, selfV, selfS, lines, slack=False, current_sensors=[]):
        self.selfV = selfV
        self.selfS = selfS
        self.lines = lines
        self.slack = slack
        self.selfY = 0
        self.current_sensors = current_sensors
        self.current_sensor_power = 0
        for line in self.lines:
            self.selfY -= line.link(self)

    # node_manager
    # shared_info is a class that holds the shared information to this node
    # Run power flow until we hit a stable state, update if values change anywhere
    def node_manager(self):
        # Loop forever, always keep the power flow up to date
        while True:
            self.gauss_voltage()
            if self.slack:
                self.power_calc()

    # gauss_voltage
    # No input argument, Node contains necessary information
    # Calculates own voltage based on current state of voltages and power
    def gauss_voltage(self):
        # Normal Gauss voltage method for a node.
        V_current = np.conj(self.selfS / self.selfV)
        sums = 0
        for line in self.lines:
            node_info = line.volt_admittance_request(self)
            sums -= node_info[0] * node_info[1]
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
        for line in self.lines:
            node_info = line.volt_admittance_request(self)
            I += node_info[0] * node_info[1]
        newS = self.selfV * np.conj(I)
        # New power, based on current voltage information
        self.selfS = newS

    def live_pf(self):
        # If list is empty, can't do anything
        if len(self.current_sensors) == 0:
            return 0
        # If we have at least one current sensor, we can detect power flowing
        power_sum = self.selfV * self.Yself_calc()
        # Add the rest to the power sum
        for current in self.current_sensors:
            power_sum += current.current * self.selfV
        # Power sum will be the net node power.  Power our - power in
        self.current_sensor_power = power_sum

    def Yself_calc(self):
        self.selfY = 1/self.selfV * (np.conj(self.current_sensor_power) / np.conj(self.selfV) - sum([x.current for x in self.current_sensors]))
        return self.selfY
