# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# March 2021
# node.py
# Run the required equations and functions to be a node.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from statistics import mean
from pulp import LpMinimize, LpProblem, LpVariable


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

    def update_p(self):
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # This calculation needs to become an actual optimization, all other processes after this calculation can remain
        # Constant.
        #
        # Old.
        # self.p = (mean([i.ld for i in self.lines]) - self.a) / self.b
        #
        # New.
        optimize = LpProblem('power_production', LpMinimize)
        # Finally see the weighted average.  It's in the optimization, eq: 161 shows it well.
        # First we need cost as a function of P, in this case, P^2b+Pa=C(P), and we'll just look at a single time step.
        # random number for upper bound at this time.
        P = LpVariable('power_produced,', lowBound=0, upBound=500)
        # This leads our first problem, we can't use linear optimization to optimize a quadratic.
        # Simple! use linear costs.  Upgrade to the piecewise later.
        # We have an example of storing linear costs from Dr. Wang's 24 bus system, we'll use that for now.
        # We have no constraints beyond the power production limits, using the current lambda and this nodes generator
        # cost, we should be able to do an incredibly simple optimization.
        #
        # This won't work as stated.  This will simply return all 0 since we're minimizing...

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
