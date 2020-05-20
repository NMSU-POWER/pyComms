# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# May 2020
# gauss_node.py
# Be a node and run individual power flow.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Node:
    def __init__(self, neighborV, neighborY, selfV, selfS):
        self.neighborV = neighborV
        if type(neighborV) == list:
            self.neighborDelta = [0] * len(self.neighborV)
        else:
            self.neighborDelta = 0
        print(self.neighborDelta)
        self.neighborY = neighborY
        self.selfV = selfV
        self.selfS = selfS

    def gauss_iter(self):
        # Step one, what is the power with the current angles?
        S_current = 0
        for i in len(self.neighborV):
            print(i)
