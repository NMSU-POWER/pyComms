# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodal
# March 2021
# controller.py
# Be the overarching control for running experiments on the different lambda style systems.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from statistics import mean
from offline.line import Line
from offline.node import Node
import pandas as pd
import sys

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
    system_info = sys.argv[1]
    branches = pd.read_excel(system_info, sheet_name='Branch Information')
    gens = pd.read_excel(system_info, sheet_name='Generation Information').sort_values(by='Bus ID').\
        reset_index(drop=True)
    loads = pd.read_excel(system_info, sheet_name='Load Information')
    # exit()

    # Set up the line devices
    lines = []
    max_bus = 0
    for i in range(len(branches['Susceptance'])):
        line = Line(branches['Susceptance'][i] * 1j, branches['From Bus'][i], branches['To Bus'][i], i)
        lines.append(line)
        if line.conn2 > max_bus:
            max_bus = line.conn2
        if line.conn1 > max_bus:
            max_bus = line.conn1
        print('Line ' + str(line.device_id) + ' from ' + str(line.conn1) + ' to ' + str(line.conn2) + ' with x=' +
              str(line.x))
    print('Number of buses: ' + str(max_bus))

    # Set up the node devices, pull # nodes from lines, then make generator information from generators? How to combine
    # generators?  Keeping it super simple right now.  Simple average, do unique generator objects later.
    j = 0
    nodes = []
    for i in range(1, max_bus + 1):
        gen_vals = []
        gen_consts = []
        while j < len(gens['Bus ID']) and i == gens['Bus ID'][j]:
            gen_vals.append(gens['Incremental Cost in $/MWh'][j])
            gen_consts.append(gens['IC Constant Cost in $'][j])
            j += 1
        # !! Every node has 100MW load
        try:
            gen_cost = mean(gen_vals)
            gen_const_cost = mean(gen_consts)
        except Exception as e:
            print('At bus ' + str(i) + ' no generation units.')
            print(e)
            gen_cost = float('inf')
        # We need all the lines connected to this node.
        connections = []
        for k in range(len(branches['From Bus'])):
            if branches['From Bus'][k] == i or branches['To Bus'][k] == i:
                connections.append(lines[k])
        node = Node(gen_const_cost, gen_cost, loads['MW Load'][i-1], len(lines) + i, connections)
        nodes.append(node)
        print('Node ' + str(i) + ' with id ' + str(node.device_id) + ' with generation IC=' + str(node.b))

    while True:
        for node in nodes:
            node.update_p()
            print(node.p)
        for line in lines:
            print(line.ld)
            connected_list = []
            for node in nodes:
                if line in node.lines:
                    connected_list.extend(node.lines)
                    connected_list.remove(line)
            lambda_list = []
            for connected in connected_list:
                lambda_list.append(connected.ld)
            line.update_lambda(lambda_list)

    '''
    line1 = Line(57.15j, 1)
    line2 = Line(66.66j, 2)
    line3 = Line(50j, 3)

    node1 = Node(1, .01, 0, 4, [line1, line2])
    node2 = Node(1, .015, 0, 5, [line1, line3])
    node3 = Node(1, .02, 400, 6, [line2, line3])
    

    exit()

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
    '''
