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

    for i in range(100):
        a1.solve_it()
        a2.solve_it()
        a3.solve_it()
        # A1 update
        a1_external = []
        for j in range(len(a1.external)):
            if a1.external[j] // 100 == 2:
                a1_external.append(a2.theta[a1.external[j] % 100 - 1])
            else:
                a1_external.append(a3.theta[a1.external[j] % 100 - 1])
        a1.update_alpha(a1_external, i, A, B)
        # A2 update
        a2_external = []
        for j in range(len(a2.external)):
            if a2.external[j] // 100 == 1:
                a2_external.append(a1.theta[a2.external[j] % 100 - 1])
            else:
                a2_external.append(a3.theta[a2.external[j] % 100 - 1])
        a2.update_alpha(a2_external, i, A, B)
        # A3 update
        a3_external = []
        for j in range(len(a3.external)):
            if a3.external[j] // 100 == 2:
                a3_external.append(a2.theta[a3.external[j] % 100 - 1])
            else:
                a3_external.append(a1.theta[a3.external[j] % 100 - 1])
        a3.update_alpha(a3_external, i, A, B)

    print('Total objective: ' + str(a1.problem.objective.value() + a2.problem.objective.value()
                                    + a3.problem.objective.value()))
