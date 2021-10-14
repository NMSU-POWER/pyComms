# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# September, 2021
# one_fictitious.py
# Conejo algorithm with a single fictitious bus per interconnect.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Area import Area
from matplotlib import pyplot as plt
import numpy as np

A = 1000
B = 500

if __name__ == '__main__':
    a1 = Area('3-bus_decoupled_1.xlsx', 1, [False, False, False, False])
    a2 = Area('3-bus_decoupled_2.xlsx', 2, [True, False, False, False])
    a3 = Area('3-bus_decoupled_3.xlsx', 3, [True, True])
    a1_alpha = [[], [], [], []]
    a2_alpha = [[], [], [], []]
    a3_alpha = [[], []]
    delta = [0, 0, 0]
    alpha = [115.09, 112.356, 100, 100, 100]
    index = []
    for i in range(50):
        index.append(i)
        for j in range(len(a1.alpha)):
            a1_alpha[j].append(a1.alpha[j])
        #a1.delta_tied_vals = [delta[0], delta[1], delta[2], delta[3]]
        a1.setup()
        a1.solve_it()
        delta[0] = a1.tie_theta[0].value()
        delta[1] = a1.tie_theta[1].value()
        #delta[2] = a1.tie_theta[2].value()
        #delta[3] = a1.tie_theta[3].value()

        for j in range(len(a2.alpha)):
            a2_alpha[j].append(a2.alpha[j])
        #a2.delta_tied_vals = [delta[0], delta[1], delta[2], delta[4]]
        a2.delta_tied_vals = [delta[0]]
        a2.setup()
        a2.solve_it()
        delta[2] = a2.tie_theta[1].value()
        #delta[4] = a2.tie_theta[3].value()

        for j in range(len(a3.alpha)):
            a3_alpha[j].append(a3.alpha[j])
        a3.delta_tied_vals = [delta[1], delta[2]]
        a3.setup()
        a3.solve_it()

        '''a1_bus_theta = []
        for j in range(len(a1.internal)):
            a1_bus_theta.append(a1.theta[a1.internal[j] % 100 - 1].value())
        a2_bus_theta = []
        for j in range(len(a2.internal)):
            a2_bus_theta.append(a2.theta[a2.internal[j] % 100 - 1].value())
        a3_bus_theta = []
        for j in range(len(a3.internal)):
            a3_bus_theta.append(a3.theta[a3.internal[j] % 100 - 1].value())

        alpha = [a1.alpha[0], a1.alpha[1], a1.alpha[2], a1.alpha[3], a2.alpha[3]]
        s = a1_bus_theta[0] + a2_bus_theta[0] - 2 * delta[0]
        if s != 0:
            alpha[0] += (1/(A+B*i)) * -s/abs(s)
        s = a1_bus_theta[1] + a2_bus_theta[1] - 2 * delta[1]
        if s != 0:
            alpha[1] += (1 / (A + B * i)) * -s / abs(s)
        s = a1_bus_theta[2] + a2_bus_theta[2] - 2 * delta[2]
        if s != 0:
            alpha[2] += (1 / (A + B * i)) * -s / abs(s)
        s = a1_bus_theta[3] + a3_bus_theta[0] - 2 * delta[3]
        if s != 0:
            alpha[3] += (1 / (A + B * i)) * -s / abs(s)
        s = a2_bus_theta[3] + a3_bus_theta[1] - 2 * delta[4]
        if s != 0:
            alpha[4] += (1 / (A + B * i)) * -s / abs(s)'''

        k = 1/(A+B*i)
        if a1.tie_flow[0].value() + a2.tie_flow[0].value() != 0:
            alpha[0] = alpha[0] + (a1.tie_flow[0].value() + a2.tie_flow[0].value()) / abs(a1.tie_flow[0].value() + a2.tie_flow[0].value()) * k
        # if a1.tie_flow[1].value() + a2.tie_flow[1].value() != 0:
        #     alpha[1] = alpha[1] + (a1.tie_flow[1].value() + a2.tie_flow[1].value()) / abs(a1.tie_flow[1].value() + a2.tie_flow[1].value()) * k
        a1.alpha = [alpha[0]]
        a2.alpha = [alpha[0]]
        '''alpha[1] = alpha[1] + (a1.tie_flow[1].value() + a2.tie_flow[1].value()) / np.sqrt(a1.tie_flow[1].value() ** 2 + a2.tie_flow[1].value() ** 2) * k
        alpha[2] = alpha[2] + (a1.tie_flow[2].value() + a2.tie_flow[2].value()) / np.sqrt(a1.tie_flow[2].value() ** 2 + a2.tie_flow[2].value() ** 2) * k
        alpha[3] = alpha[3] + (a1.tie_flow[3].value() + a3.tie_flow[0].value()) / np.sqrt(a1.tie_flow[3].value() ** 2 + a3.tie_flow[0].value() ** 2) * k
        alpha[4] = alpha[4] + (a2.tie_flow[3].value() + a3.tie_flow[1].value()) / np.sqrt(a2.tie_flow[3].value() ** 2 + a3.tie_flow[1].value() ** 2) * k

        a1.alpha = [alpha[0], alpha[1], alpha[2], alpha[3]]
        a2.alpha = [alpha[0], alpha[1], alpha[2], alpha[4]]
        a3.alpha = [alpha[3], alpha[4]]'''

        # print('Total objective: ' + str(a1.problem.objective.value() + a2.problem.objective.value()
        #                                 + a3.problem.objective.value()))
    # for i in range(len(a1.tie_flow)):
        # print(a1.tie_flow[i].value())
    print('Total objective: ' + str(a1.problem.objective.value() + a2.problem.objective.value()
                                    + a3.problem.objective.value()))
    print(delta)
    a1.data_dump()
    a2.data_dump()
    a3.data_dump()
    print(a1.alpha)
    print(a2.alpha)
    print(a3.alpha)
    print()
    print(str(a1.tie_flow[0].value()) + ':' + str(a2.tie_flow[0].value()))
    # print(str(a1.tie_flow[1].value()) + ':' + str(a2.tie_flow[1].value()))
    fig = plt.figure()
    plt.plot(index, a1_alpha[0])
    # plt.plot(index, a1_alpha[1])
    plt.show()
    exit()
    print(str(a1.tie_flow[1].value()) + ':' + str(a2.tie_flow[1].value()))
    print(str(a1.tie_flow[2].value()) + ':' + str(a2.tie_flow[2].value()))
    print(str(a1.tie_flow[3].value()) + ':' + str(a3.tie_flow[0].value()))
    print(str(a2.tie_flow[3].value()) + ':' + str(a3.tie_flow[1].value()))
    print()
    print(a1.internal)
    print(a2.internal)
    print(a3.internal)
    print()
    print(a2.problem.status)
    fig = plt.figure()
    plt.subplot(2, 2, 1)
    for i in range(len(a1_alpha)):
        plt.plot(index, a1_alpha[i], label=i)
    plt.subplot(2, 2, 2)
    for i in range(len(a2_alpha)):
        plt.plot(index, a2_alpha[i], label=i)
    plt.subplot(2, 2, 3)
    for i in range(len(a3_alpha)):
        plt.plot(index, a3_alpha[i], label=i)
    plt.show()
