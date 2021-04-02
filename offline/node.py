# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# March 2021
# node.py
# Run the required equations and functions to be a node.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Node:
    # Needed as a node: a and b power cost values, load, id number (needed in some transmission styles), connected lines
    def __init__(self, a, b, load=0, id_input=-1, lines=[]):
        self.a = a
        self.b = b
        self.load = load
        self.device_id = id_input
        self.lines = lines

    