# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# March 15, 2020
# gauss.py
# Perform Gauss powerflow calculations given an admittance matrix.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np
from admittance import Admittance


class Gauss:
    def __init__(self, admittance, P, Q, V, d):
        self.admittance = admittance
        self.origin_P = P
        self.origin_Q = Q
        self.origin_V = V
        self.origin_d = d
        self.S = []
        for i in range(len(P)):
            if P[i] == -1:
                P1 = 1
            else:
                P1 = P[i]
            if Q[i] == -1:
                Q1 = 1
            else:
                Q1 = Q[i]
            self.S.append(np.complex(P1, Q1))
        self.V = []
        for i in range(len(V)):
            if V[i] == -1:
                self.V.append(1)
            else:
                self.V.append(V[i])

    def solve(self):
        V_old = self.V
        self.V = self.iterate_V()

        while np.linalg.norm(np.array(V_old) - np.array(self.V)) > .1:
            # Replace known
            for i in range(len(self.origin_V)):
                if self.origin_V[i] != -1:
                    self.V[i] = self.origin_V[i]
            self.S = self.iterate_S()
            # Replace known
            for i in range(len(self.origin_P)):
                if self.origin_P[i] == -1:
                    P1 = np.real(self.S[i])
                else:
                    P1 = self.origin_P[i]
                if self.origin_Q[i] == -1:
                    Q1 = np.imag(self.S[i])
                else:
                    Q1 = self.origin_Q[i]
                self.S[i] = np.complex(P1, Q1)
            V_old = self.V
            self.V = self.iterate_V()

    def iterate_V(self):
        new_V = []
        for i in range(len(self.V)):
            sum = 0
            for j in range(len(self.admittance[0])):
                sum += self.admittance[i][j] * self.V[j]
            new_V.append(1 / self.admittance[i][i] * ((np.conj(self.S[i]/self.V[i]) - sum) + self.admittance[i][i] *
                                                      self.V[i]))
        return new_V

    def iterate_S(self):
        new_S = []
        for i in range(len(self.S)):
            sum = 0
            for j in range(len(self.admittance[0])):
                sum += self.V[j] * self.admittance[i][j]
            new_S.append(self.V[i] * np.conj(sum))
        return new_S
