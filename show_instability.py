# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# February 5, 2021
# show_instability.py
# Show the instability of the line agent calculation if allowed to execute unbounded.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import matplotlib.pyplot as plt

lambda_start = 0
P1 = -100
P2 = -450
alpha = -.01

iterations = range(1, 101)

result = [lambda_start]
for iteration in iterations[:99]:
    result.append(result[iteration - 1] + (P1 + P2) * alpha)

plt.plot(iterations, result)
plt.title('System power value versus iterations without P1, P2 change')
plt.xlabel('Iteration')
plt.ylabel('System power value')
plt.show()

iterations = range(1, 201)
P1 = 49900
P2 = 24550

for iteration in iterations[99:199]:
    result.append(result[iteration - 1] + (P1 + P2) * alpha)

plt.plot(iterations, result)
plt.title('System power value versus iterations without P1, P2 change until iteration 100')
plt.xlabel('Iteration')
plt.ylabel('System power value')
plt.show()
