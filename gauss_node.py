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

    def gauss_voltage(self):
        Yself = -1 * sum(self.neighborY)
        # Below only correct when self angle = 0
        V_current = np.conj(self.selfS / self.selfV)
        sums = 0
        for v, y, d in zip(self.neighborV, self.neighborY, self.neighborDelta):
            sums -= y * v * (math.cos(d) + math.sin(d) * 1j)
        V_current += sums
        V_current /= Yself
        print(V_current)
        print(np.abs(V_current))
        return(cmath.phase(V_current))
        # self.selfV = np.abs(V_current)
        # Not sure if we need the following if we're worried about magnitude, probably for more than 1 iteration.
        # self.neighborDelta = [cmath.phase(V_current)]

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
