# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# September, 2021
# one_fictitious.py
# Conejo algorithm with a single fictitious bus per interconnect.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Area import Area

A = 10
B = 5

if __name__ == '__main__':
    a1 = Area('formatted_data1.xlsx', 1)
    a2 = Area('formatted_data2.xlsx', 2)
    a3 = Area('formatted_data3.xlsx', 3)

    for i in range(10000):
        a1.setup()
        a1.solve_it()
        a2.setup()
        a2.solve_it()
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

        print('Total objective: ' + str(a1.problem.objective.value() + a2.problem.objective.value()
                                        + a3.problem.objective.value()))
    # for i in range(len(a1.tie_flow)):
        # print(a1.tie_flow[i].value())
