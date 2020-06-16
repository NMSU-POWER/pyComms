# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# June 2020
# line_agent.py
# Contains the line agent class, manages information transfer between two nodes.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from gauss_node import Node


class Line_Agent:
    def __init__(self, own_admittance):
        self.admittance = own_admittance
        # Node reference list
        self.nodes = []

    def link(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

    # Each node requests info, and the line agent sends the other node's info
    def volt_admittance_request(self, requesting_node):
        # Assume the voltage starts at 1 in case the other node hasn't hooked up yet
        voltage = 1
        for node in self.nodes:
            if node != requesting_node:
                voltage = node.selfV

        return self.admittance, voltage
