# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# June 2020
# line_agent.py
# Contains the line agent class, manages information transfer between two nodes.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Line_Agent:
    def __init__(self, own_admittance):
        self.admittance = own_admittance
        # Node reference list
        self._nodes = []

    def link(self, node):
        print(node)
        if node not in self._nodes:
            self._nodes.append(node)
        print(self._nodes)
        return self.admittance

    # Each node requests info, and the line agent sends the other node's info
    def volt_admittance_request(self, requesting_node):
        # Assume the voltage starts at 1 in case the other node hasn't hooked up yet
        voltage = 1
        for node in self._nodes:
            # Makes the assumption that there are only ever two nodes connected
            if node != requesting_node:
                voltage = node.selfV

        return self.admittance, voltage
