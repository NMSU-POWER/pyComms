# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# May 2020
# gauss_node.py
# Be a node and run individual power flow.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np
import math


class Node:
    def __init__(self, selfV, selfS, neighborV, neighborY):
        self.neighborV = neighborV
        self.neighborDelta = [0] * len(self.neighborV)
        self.neighborY = neighborY
        self.selfV = selfV
        self.selfS = selfS

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
        for v,y in zip(self.neighborV, self.neighborY):
            sums -= y*v
        V_current += sums/Yself
        print(V_current)
