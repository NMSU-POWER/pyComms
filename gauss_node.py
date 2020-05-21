# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# May 2020
# gauss_node.py
# Be a node and run individual power flow.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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
        for i in len(self.neighborV):
            print(i)
