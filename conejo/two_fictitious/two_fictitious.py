# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# September, 2021
# one_fictitious.py
# Conejo algorithm with a single fictitious bus per interconnect.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Area import Area
from matplotlib import pyplot as plt
import numpy as np

A = .1
B = .1

if __name__ == '__main__':
    a1 = Area('formatted_data1.xlsx', 1, [False, False, False, False])
    a2 = Area('formatted_data2.xlsx', 2, [False, False, False, False])
    a3 = Area('formatted_data3.xlsx', 3, [False, False])
    a1_alpha = [[], [], [], []]
    a2_alpha = [[], [], [], []]
    a3_alpha = [[], []]
    delta = [0, 0, 0, 0, 0]

    index = []
    for i in range(100):
        index.append(i)
        for j in range(len(a1.Beta)):
            a1_alpha[j].append(a1.Beta[j])
        a1.delta_tied_vals = [delta[0], delta[1], delta[2], delta[3]]
        a1.setup()
        a1.solve_it()
        delta[0] = a1.tie_theta[0].value()
        delta[1] = a1.tie_theta[1].value()
        delta[2] = a1.tie_theta[2].value()
        delta[3] = a1.tie_theta[3].value()

        for j in range(len(a2.Beta)):
            a2_alpha[j].append(a2.Beta[j])
        a2.delta_tied_vals = [delta[0], delta[1], delta[2], delta[4]]
        a2.setup()
        a2.solve_it()
        delta[4] = a2.tie_theta[3].value()

        for j in range(len(a3.Beta)):
            a3_alpha[j].append(a3.Beta[j])
        a3.delta_tied_vals = [delta[3], delta[4]]
        a3.setup()
        a3.solve_it()

        a1_bus_theta = []
        a1_connection_theta = []
        for j in range(len(a1.internal)):
            a1_bus_theta.append(a1.theta[a1.internal[j] % 100 - 1])
            a1_connection_theta.append(a1.tie_theta[j])
        a2_bus_theta = []
        a2_connection_theta = []
        for j in range(len(a2.internal)):
            a2_bus_theta.append(a2.theta[a2.internal[j] % 100 - 1])
            a2_connection_theta.append(a2.tie_theta[j])
        a3_bus_theta = []
        a3_connection_theta = []
        for j in range(len(a3.internal)):
            a3_bus_theta.append(a3.theta[a3.internal[j] % 100 - 1])
            a3_connection_theta.append(a3.tie_theta[j])

        # Beta in area A is gamma in area B...
        react1 = a1.tie_X[0]
        s1 = [300/react1*(a1_bus_theta[0].value() - a1.tie_theta[0].value()) + 300/react1*(a2.tie_theta[0].value() - a1.tie_theta[0].value()),
              300/react1*(a2_bus_theta[0].value() - a2.tie_theta[0].value()) + 300/react1*(a1.tie_theta[0].value() - a2.tie_theta[0].value())]
        s1_mag = np.sqrt(s1[0]**2 + s1[1]**2)
        react2 = a1.tie_X[1]
        s2 = [300/react2*(a1_bus_theta[1].value() - a1.tie_theta[1].value()) + 300/react2*(a2.tie_theta[1].value() - a1.tie_theta[1].value()),
              300/react2*(a2_bus_theta[1].value() - a2.tie_theta[1].value()) + 300/react2*(a1.tie_theta[1].value() - a2.tie_theta[1].value())]
        s2_mag = np.sqrt(s2[0]**2 + s2[1]**2)
        react3 = a1.tie_X[2]
        s3 = [-300/react3*(a1_bus_theta[2].value() - a1.tie_theta[2].value()) + -300/react3*(a2.tie_theta[2].value() - a1.tie_theta[2].value()),
              -300/react3*(a2_bus_theta[2].value() - a2.tie_theta[2].value()) + -300/react3*(a1.tie_theta[2].value() - a2.tie_theta[2].value())]
        s3_mag = np.sqrt(s3[0]**2 + s3[1]**2)
        react4 = a1.tie_X[3]
        s4 = [-300/react4*(a1_bus_theta[3].value() - a1.tie_theta[3].value()) + -300/react4*(a3.tie_theta[0].value() - a1.tie_theta[3].value()),
              -300/react4*(a3_bus_theta[0].value() - a3.tie_theta[0].value()) + -300/react4*(a1.tie_theta[3].value() - a3.tie_theta[0].value())]
        s4_mag = np.sqrt(s4[0]**2 + s4[1]**2)
        react5 = a2.tie_X[3]
        s5 = [-300/react5*(a2_bus_theta[3].value() - a2.tie_theta[3].value()) + -300/react5*(a3.tie_theta[1].value() - a2.tie_theta[3].value()),
              -300/react5*(a3_bus_theta[1].value() - a3.tie_theta[1].value()) + -300/react5*(a2.tie_theta[3].value() - a3.tie_theta[1].value())]
        s5_mag = np.sqrt(s5[0]**2 + s5[1]**2)
        k = 1 / (A + i * B)
        epsilon = .1
        if abs(s1[0] + s1[1]) > epsilon:
            update1 = [s1[0] / s1_mag * k + a1.Beta[0], s1[1] / s1_mag * k + a2.Beta[0]]
        else:
            update1 = [a1.Beta[0], a2.Beta[0]]
        if abs(s2[0] + s2[1]) > epsilon:
            update2 = [s2[0] / s2_mag * k + a1.Beta[1], s2[1] / s2_mag * k + a2.Beta[1]]
        else:
            update2 = [a1.Beta[1], a2.Beta[1]]
        if abs(s3[0] + s3[1]) > epsilon:
            update3 = [s3[0] / s3_mag * k + a1.Beta[2], s3[1] / s3_mag * k + a2.Beta[2]]
        else:
            update3 = [a1.Beta[2], a2.Beta[2]]
        if abs(s4[0] + s4[1]) > epsilon:
            update4 = [s4[0] / s4_mag * k + a1.Beta[3], s4[1] / s4_mag * k + a3.Beta[0]]
        else:
            update5 = [a1.Beta[3], a3.Beta[0]]
        if abs(s5[0] + s5[1]) > epsilon:
            update5 = [s5[0] / s5_mag * k + a2.Beta[3], s5[1] / s5_mag * k + a3.Beta[1]]
        else:
            update1 = [a2.Beta[3], a3.Beta[1]]
        a1.Beta = [update1[0], update2[0], update3[0], update4[0]]
        a2.Beta = [update1[1], update2[1], update3[1], update5[0]]
        a3.Beta = [update4[1], update5[1]]
        a1.gamma = [update1[1], update2[1], update3[1], update4[1]]
        a2.gamma = [update1[0], update2[0], update3[0], update5[1]]
        a3.gamma = [update4[0], update5[0]]
        print(s1)
        print(s1_mag)
        print(s2)
        print(s2_mag)
        print(s3)
        print(s3_mag)
        print(s4)
        print(s4_mag)
        print(s5)
        print(s5_mag)
        print(a1.Beta)
        print(a2.Beta)
        print(a3.Beta)
        # exit()

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
    print(a1.Beta)
    print(a2.Beta)
    print(a3.Beta)
    print()
    print(str(a1.tie_flow[0].value()) + ':' + str(a2.tie_flow[0].value()))
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
