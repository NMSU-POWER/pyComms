# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodal
# March 2021
# controller.py
# Be the overarching control for running experiments on the different lambda style systems.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
