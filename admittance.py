# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall, Andres Acosta, Sarbajit Basu
# February 2020
# admittance.py
# Accept a list of lines and produce an admittance matrix.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np


# Admittance holds/calculates the admittance matrix for the bus network.
class Admittance:

    # Constructor for the class defaults to no lines so we can build up later
    def __init__(self, line_list=None):
        # Need a list to check values, if none was passed, make it blank
        if line_list is None:
            line_list = []
        self.lines = {}
        self.buses = {}
        self.admittance = None
        # Iterate through the list, printing then adding the lines to the list
        for line in line_list:
            self.add_line(line)
        self.produce_matrix()

    # add_line function adds a single line item to the admittance matrix iff the line isn't already there.
    def add_line(self, line):
        # Split the line input at every space
        line_parts = line.split(' ')
        # Assuming line comes in as R + jX instead of G + jB
        self.lines[line_parts[0]] = {'bus1': int(line_parts[1]), 'bus2': int(line_parts[2]),
                                     'impedance': complex(float(line_parts[3]), float(line_parts[4])),
                                     'admittance': 1/complex(float(line_parts[3]), float(line_parts[4]))}

    def produce_matrix(self):
        # Step 1 is identify the number of buses in the system
        bus_count = 0
        for key in self.lines.keys():
            if self.lines[key]['bus1'] not in self.buses.keys():
                self.buses[self.lines[key]['bus1']] = bus_count
                bus_count += 1
            if self.lines[key]['bus2'] not in self.buses.keys():
                self.buses[self.lines[key]['bus2']] = bus_count
                bus_count += 1

        # bus_count now holds the number of buses in the system (count not index)
        # buses now holds a map between bus names and bus numbers
        admittance = np.zeros((bus_count, bus_count), complex)
        # We now have the right shape for our admittance matrix, fill it up
        # Start with connections between buses
        for key in self.lines.keys():
            admittance[self.lines[key]['bus1']-1][self.lines[key]['bus2']-1] \
                += -self.lines[key]['admittance']
            admittance[self.lines[key]['bus2']-1][self.lines[key]['bus1']-1] \
                += -self.lines[key]['admittance']
        # Finish with the diagonal, based on current state, 1,1 is sum of -1 * column 1 etc. etc.
        # The following only works thanks to a square matrix.
        for col in range(len(admittance)):
            val = 0
            for row in range(len(admittance)):
                val += admittance[row][col]
            admittance[col][col] = -1 * val
        self.admittance = admittance
        # Admittance network is now known and stored in matrix self.admittance
