# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# March 2021
# node.py
# Run the required equations and functions to be a node.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from statistics import mean


class Node:
    # Needed as a node: a and b power cost values, load, id number (needed in some transmission styles), connected lines
    def __init__(self, a, b, load=0, id_input=-1, lines=[]):
        self.a = a
        self.b = b
        self.load = load
        self.device_id = id_input
        self.lines = lines
        self.p = 0
        self.delta = 0
        for line in self.lines:
            line.delta[self] = self.delta
            line.ptie[self] = 0
            line.flow[self] = 0

    def update_p(self):
        self.p = (mean([i.ld for i in self.lines]) + sum([i.flow[self] for i in self.lines]) - self.a) / self.b
        other_angle_react = 0
        diagonal_react = 0
        for line in self.lines:
            for key in line.delta.keys():
                if key != self:
                    other_angle_react += line.delta[key] / line.x
            diagonal_react += 1 / line.x
        self.delta = (self.p - self.load + other_angle_react) / diagonal_react
        for line in self.lines:
            for key in line.delta.keys():
                if key == self:
                    line.delta[self] = self.delta
                else:
                    line.ptie[self] = (self.delta - line.delta[key]) / line.x
