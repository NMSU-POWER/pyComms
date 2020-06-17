# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# June 2020
# line_agent.py
# Contains the line agent class, manages information transfer between two nodes.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Be the in-between for two nodes, passing data back to each node as needed.
class Line_Agent:

    # the only argument necessary to set up the line is the admittance of the line.
    def __init__(self, own_admittance):
        self.admittance = own_admittance
        # Node reference list
        self._nodes = []

    # link
    # input the Node to link to
    # Link this line agent to the input node, intended to be called from the node itself during initialization.
    def link(self, node):
        print(node)
        if node not in self._nodes:
            self._nodes.append(node)
        print(self._nodes)
        return self.admittance

    # volt_admittance_request
    # input the node requesting information
    # Each node requests info, and the line agent sends the other node's voltage
    def volt_admittance_request(self, requesting_node):
        # Make sure the node behaved and hooked up first.
        self.link(requesting_node)
        # Assume the voltage starts at 1 in case the other node hasn't hooked up yet
        voltage = 1
        for node in self._nodes:
            # Makes the assumption that there are only ever two nodes connected
            if node != requesting_node:
                voltage = node.selfV

        return self.admittance, voltage
