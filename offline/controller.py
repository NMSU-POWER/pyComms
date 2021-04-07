# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodal
# March 2021
# controller.py
# Be the overarching control for running experiments on the different lambda style systems.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from statistics import mean
from offline.line import Line
from offline.node import Node

# pseudocode:
# For every input line
# # Set up the line object to a thread
# # Line objects need to have a block
# For every input node
# # Set up the node to a thread
# # Pass the proper line references to the node
# # Start the node threads
# For every line object
# # Remove the block, allow all lines to start ASAP

# What this means we need:
# An object for each node
# A parallel styled object for each line (Blocking start)

# We also need to format input from csv, this way we could even feed in a 114 or higher bus system if desired

# Standard setup for 3-bus (testing)
if __name__ == "__main__":
    line1 = Line(57.15j, 1)
    line2 = Line(66.66j, 2)
    line3 = Line(50j, 3)

    node1 = Node(1, .01, 0, 4, [line1, line2])
    node2 = Node(1, .015, 0, 5, [line1, line3])
    node3 = Node(1, .02, 400, 6, [line2, line3])

    while(True):
        node1.update_p()
        node2.update_p()
        node3.update_p()
        print(node1.p)
        print(node2.p)
        print(node3.p)
        line1.update_lambda([line2.ld, line3.ld])
        line2.update_lambda([line1.ld, line3.ld])
        line3.update_lambda([line2.ld, line1.ld])
        print(line1.ld)
        print(line2.ld)
        print(line3.ld)
        print(mean([line1.ld, line2.ld]))
        print(mean([line1.ld, line3.ld]))
        print(mean([line2.ld, line3.ld]))
        print()
