# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# January 20201
# opf_node.py
# Be a node and run individual DCOPF functions.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import statistics


# Hold information about the line connected to the node objects
class InternalLine:
    def __init__(self, admittance):
        # Delta of the node at the other end
        self.otherSideDelta = 0
        # Admittance of this line
        self.admittance = admittance
        # reactance of the line
        self.reactance = (1/self.admittance).imag
        # The lambda of this line
        self.lineLambda = 0
        # Power being pushed into the line from this side of a node
        self.powerOutThisSide = 0

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
        self.reactanceSum = sum([x.reactance for x in self.lines])

    def update_power_angle(self):
        # Update power first
        self.power = (statistics.mean([x.lineLambda for x in self.lines]) - self.a) / self.b
        # Now update self angle
        self.delta = self.power - self.load + sum([x.otherSideDelta / x.reactance for x in self.lines])
        # Now update the power transferred out on this side of the line object
        for line in self.lines:
            line.powerOutThisSide = (self.delta - line.otherSideDelta) / self.reactanceSum


if __name__ == '__main__':
    # Make lines
    line1 = InternalLine(admittance=1.63-57.10j)
    line2 = InternalLine(admittance=4.42-66.37j)
    line3 = InternalLine(admittance=4.95-49.50j)
    # Make nodes
    node1 = Node(load=0, a=1, b=.01, lines=[line1, line2])
    node2 = Node(load=0, a=1, b=.015, lines=[line1, line3])
    node3 = Node(load=400, a=1, b=.02, lines=[line2, line3])
