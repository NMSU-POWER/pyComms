# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# February 2021
# opf_line.py
# Be a line and run individual DCOPF functions.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import statistics

# Global for now, constant that affects how quickly a node changes lambda.
alpha = -.01



# Hold information about the line connected to the node objects
class InternalLine:
    def __init__(self, admittance):
        # Delta of the node at the other end
        self.delta = {}
        # Admittance of this line
        self.admittance = admittance
        # reactance of the line
        self.reactance = (1/self.admittance).imag
        # The lambda of this line
        self.lineLambda = 0
        # Power being pushed into the line from this side of a node
        self.powerOut = {}
        # Lists of other lambdas
        self.other_lambdas = {}

    def lambda_update(self):
        collected_lambdas = []
        power_out = 0
        for node in self.other_lambdas.keys():
            collected_lambdas.extend(self.other_lambdas[node])
            power_out += self.powerOut[node]
        self.lineLambda = self.lineLambda + power_out * alpha
        collected_lambdas.append(self.lineLambda)
        self.lineLambda = statistics.mean(collected_lambdas)