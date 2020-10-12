# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# October 2020
# distributed_algorithm_test.py
# Test the distributed algorithm and tweak
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Step 1, calculate the export from every bus given angles
def export_calc(ang, B):
    return [[100 * B[0][0] * ang[0] + 100 * B[0][1] * ang[1] + 100 * B[0][2] * ang[2]],
            [100 * B[1][0] * ang[0] + 100 * B[1][1] * ang[1] + 100 * B[1][2] * ang[2]],
            [100 * B[2][0] * ang[0] + 100 * B[2][1] * ang[1] + 100 * B[2][2] * ang[2]]]


# Step 2, Calculate value of export with correct lambda
def bus_value(exported, ld, b, ang):
    # Bus 1 -> 2
    one_two = b[0][1] * 100 * (ang[1] - ang[0])
    two_one = -1 * one_two
    one_three = b[0][2] * 100 * (ang[2] - ang[0])
    three_one = -1 * one_three
    two_three = b[1][2] * 100 * (ang[2] - ang[1])
    three_two = -1 * two_three
    transfers = [[one_two, two_one],  # Line 1
                 [one_three, three_one],  # Line 2
                 [two_three, three_two]]  # Line 3
    transfers[0][0] *= ld[0]
    transfers[0][1] *= ld[1]
    transfers[1][0] *= ld[0]
    transfers[1][1] *= ld[2]
    transfers[2][0] *= ld[1]
    transfers[2][1] *= ld[2]
    return transfers


# Step 3, Adjust lambda upward if price to produce > price received for export, down if else
def exported_lambda_calc():
    print('lambda adjust for export')


# Step 4, Estimate desired generation at current lambda
def power_calc():
    print('power calc')


# Step 5, Calculate new angles such that they give the desired power flows
def angle_calc():
    print('angles across lines')


# The process runner, other functions to be fleshed out as this is built
if __name__ == '__main__':
    # DC OPF, all voltages assumed to be 1
    # Need generation values
    # Starts at 0
    gen = [0, 0, 0]
    # loads as they are
    load = [0, 0, 100]
    # Angles start at 0
    angles = [0, 0, 0]
    # export starts at 0
    export = [0, 0, 0]
    # B matrix
    B = [[-123.47j, 57.1j, 66.37j], [57.1j, -106.6j, 49.5j],
     [66.37j, 49.5j, -115.88j]]
    # Price of import/received for export
    values = [0, 0, 0]
    # Lambdas of each bus
    lds = [0, 0, 0]

    # Start with step 1
    export = export_calc(angles, B)

    # Step 2
    value = bus_value(export, lds, B, angles)

    # Step 3
    lds = exported_lambda_calc()
