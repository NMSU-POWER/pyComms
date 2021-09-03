# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# September, 2021
# one_fictitious.py
# Conejo algorithm with a single fictitious bus per interconnect.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Area import Area

if __name__ == '__main__':
    a1 = Area('formatted_data1.xlsx')
    a2 = Area('formatted_data2.xlsx')
    a3 = Area('formatted_data3.xlsx')

    a1.solve_it()
    a2.solve_it()
    a3.solve_it()

    print('Total objective: ' + str(a1.problem.objective.value() + a2.problem.objective.value()
                                    + a3.problem.objective.value()))
