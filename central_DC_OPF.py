# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# September, 2020
# central_DC_OPF
# Run a DC OPF centrally.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np

# We'll be using the three bus already put together for a specific case before moving into a general case.
Y = [[6.06-123.47j, -1.63+57.1j, -4.42+66.37j], [-1.63+57.1j, 6.58-106.6j, -4.95+49.5j],
     [-4.42+66.37j, -4.95+49.5j, 9.38-115.88j]]


# Using the costs from the textbook for the 3 bus case (page 357) simply for realistic numbers
c = [.001562 * 2, .00194 * 2, .00482 * 2 * 100000]
b = [7.92, 7.85, 7.97]

# Power load from our system
Pload = [0, 0, 300]

# Equation result
result_col = np.array([[-b[0]], [-b[1]], [-b[2]], [0], [0], [0], [-Pload[0]], [-Pload[1]], [-Pload[2]], [0]])

# Resulting matrix
L = np.array([[2 * c[0], 0, 0, 0, 0, 0, -1, 0, 0, 0],
     [0, 2 * c[1], 0, 0, 0, 0, 0, -1, 0, 0],
     [0, 0, 2 * c[2], 0, 0, 0, 0, 0, -1, 0],
     [0, 0, 0, 0, 0, 0, 100 * Y[0][0], 100 * Y[1][0], 100 * Y[2][0], 1],
     [0, 0, 0, 0, 0, 0, 100 * Y[0][1], 100 * Y[1][1], 100 * Y[2][1], 0],
     [0, 0, 0, 0, 0, 0, 100 * Y[0][2], 100 * Y[1][2], 100 * Y[2][2], 0],
     [-1, 0, 0, 100 * Y[0][0], 100 * Y[0][1], 100 * Y[0][2], 0, 0, 0, 0],
     [0, -1, 0, 100 * Y[1][0], 100 * Y[1][1], 100 * Y[1][2], 0, 0, 0, 0],
     [0, 0, -1, 100 * Y[2][0], 100 * Y[2][1], 100 * Y[2][2], 0, 0, 0, 0],
     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]])

print(np.linalg.inv(L).dot(result_col))

# Works with reservation.  This assigned generation to bus 3 where no generation exists.  the generation totalled the
# desired MW, so now i need to find a way to tie bus 3 generation to 0.  Simple way, add a huge cost factor to the
# bus, so there will be very little if any power generated there.  In this case, 100,000 $/MW does the trick.
# This allows lambda at bus 3, however.