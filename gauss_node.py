# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# May 2020
# gauss_node.py
# Be a node and run individual power flow.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np
import math
import cmath


class Node:
    def __init__(self, selfV, selfS, neighborV, neighborY):
        self.neighborV = neighborV
        self.neighborDelta = [0] * len(self.neighborV)
        self.neighborY = neighborY
        self.selfV = selfV
        self.Vmag = selfV
        self.selfS = selfS

    # node_manager
    # shared_info is a class that holds the shared information to this node
    # Run power flow until we hit a stable state, update if values change anywhere
    def node_manager(self, shared_info):
        return True

    # gauss_voltage
    # No input argument, Node contains necessary information
    # Calculates own voltage based on current state of voltages and power
    def gauss_voltage(self):
        # Calculate self diagonal admittance
        Yself = -1 * sum(self.neighborY)
        # Normal Gauss voltage method for a node.
        V_current = np.conj(self.selfS / self.selfV)
        sums = 0
        for v, y, d in zip(self.neighborV, self.neighborY, self.neighborDelta):
            sums -= y * v * (math.cos(d) + math.sin(d) * 1j)
        V_current += sums
        V_current /= Yself
        # Send this value back to the main function for distribution
        return np.abs(V_current), cmath.phase(V_current)

    # power_calc
    # No input arguments, Node contains necessary information.
    # Calculates the power at the node with the current nodal voltage information.
    def power_calc(self):
        # Calculate self diagonal admittance
        Yself = -1 * sum(self.neighborY)
        # I = v of each node multiplied by admittance, summation, simplifies where admittance = 0
        I = self.selfV * Yself
        for v, y, d in zip(self.neighborV, self.neighborY, self.neighborDelta):
            I += v * (math.cos(d) + 1j*math.sin(d)) * y
        newS = self.selfV * np.conj(I)
        # New power, based on current voltage information
        self.selfS = newS

    def angle_calculation(self):
        Yself = -1 * sum(self.neighborY)
        phasor = (np.conj(self.selfS) / self.selfV - (self.selfV * Yself)) / self.neighborV[0] / self.neighborY[0]
        delta = math.degrees(cmath.phase(phasor))
        return delta

    def gauss_iter(self):
        # Step one, what is the power with the current angles?
        S_current = 0
        # Step 1:
        for i in range(len(self.neighborV)):
            print(self.selfV)
            print(self.neighborV[i])
            print(self.neighborY[i])
            S_current -= self.selfV * (self.neighborV[i] * self.neighborY[i])
        print(S_current)

        #Disregard above for now, what about voltages?
        Yself = -1 * sum(self.neighborY)
        print(Yself)
        V_current = np.conj(self.selfS)/self.selfV/Yself
        sums = 0
        for v, y, d in zip(self.neighborV, self.neighborY, self.neighborDelta):
            sums -= y*v*(math.cos(d) + math.sin(d) * 1j)
        V_current += sums/Yself
        print(V_current)
        self.neighborDelta = [cmath.phase(V_current)]
        print(self.neighborDelta)

    def angle_iter(self):
        for i in np.linspace(math.radians(-30), math.radians(30), 10000):
            print(math.degrees(i))
            Yself = -1 * sum(self.neighborY)
            V_current = np.conj(self.selfS) / self.selfV / Yself
            sums = 0
            for v, y in zip(self.neighborV, self.neighborY):
                sums -= y * v * (math.cos(i) + math.sin(i) * 1j)
            V_current += sums / Yself
            print(V_current)
