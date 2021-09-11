# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# September, 2021
# one_fictitious.py
# Conejo algorithm with a single fictitious bus per interconnect.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Area import Area
from matplotlib import pyplot as plt

A = .1
B = .1

if __name__ == '__main__':
    a1 = Area('formatted_data1.xlsx', 1, [False, False, False, False])
    a2 = Area('formatted_data2.xlsx', 2, [True, True, True, False])
    a3 = Area('formatted_data3.xlsx', 3, [True, True])
    a1_alpha = [[], [], [], []]
    a2_alpha = [[], [], [], []]
    a3_alpha = [[], []]
    delta = [0, 0, 0, 0, 0]
    index = []
    for i in range(1):
        index.append(i)
        for j in range(len(a1.alpha)):
            a1_alpha[j].append(a1.alpha[j])
        a1.delta_tied_vals = [delta[0], delta[1], delta[2], delta[3]]
        a1.setup()
        a1.solve_it()
        delta[0] = a1.tie_theta[0].value()
        delta[1] = a1.tie_theta[1].value()
        delta[2] = a1.tie_theta[2].value()
        delta[3] = a1.tie_theta[3].value()

        for j in range(len(a2.alpha)):
            a2_alpha[j].append(a2.alpha[j])
        a2.delta_tied_vals = [delta[0], delta[1], delta[2], delta[4]]
        a2.setup()
        a2.solve_it()
        delta[4] = a2.tie_theta[3].value()

        for j in range(len(a3.alpha)):
            a3_alpha[j].append(a3.alpha[j])
        a3.delta_tied_vals = [delta[3], delta[4]]
        a3.setup()
        a3.solve_it()

        # A1 update
        # a1_external = []
        # a1_other_tie = []
        a1_other_flow = []
        for j in range(len(a1.external)):
            if a1.external[j] // 100 == 2:
                # a1_external.append(a2.theta[a1.external[j] % 100 - 1].value())
                for k in range(len(a2.external)):
                    if a2.external[k] == a1.internal[j]:
                        a1_other_flow.append(a2.tie_flow[k].value())
            else:
                # a1_external.append(a3.theta[a1.external[j] % 100 - 1].value())
                for k in range(len(a3.external)):
                    if a3.external[k] == a1.internal[j]:
                        a1_other_flow.append(a3.tie_flow[k].value())
        a1.update_alpha(a1_other_flow, i, A, B)
        # A2 update
        # a2_external = []
        # a2_other_tie = []
        a2_other_flow = []
        for j in range(len(a2.external)):
            if a2.external[j] // 100 == 1:
                # a2_external.append(a1.theta[a2.external[j] % 100 - 1].value())
                for k in range(len(a1.external)):
                    if a1.external[k] == a2.internal[j]:
                        a2_other_flow.append(a1.tie_flow[k].value())
            else:
                # a2_external.append(a3.theta[a2.external[j] % 100 - 1].value())
                for k in range(len(a3.external)):
                    if a3.external[k] == a2.internal[j]:
                        a2_other_flow.append(a3.tie_flow[k].value())
        a2.update_alpha(a2_other_flow, i, A, B)
        # A3 update
        # a3_external = []
        # a3_other_tie = []
        a3_other_flow = []
        for j in range(len(a3.external)):
            if a3.external[j] // 100 == 2:
                # a3_external.append(a2.theta[a3.external[j] % 100 - 1].value())
                for k in range(len(a2.external)):
                    if a2.external[k] == a3.internal[j]:
                        a3_other_flow.append(a2.tie_flow[k].value())
            else:
                # a3_external.append(a1.theta[a3.external[j] % 100 - 1].value())
                for k in range(len(a1.external)):
                    if a1.external[k] == a3.internal[j]:
                        a3_other_flow.append(a1.tie_flow[k].value())
        a3.update_alpha(a3_other_flow, i, A, B)

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
