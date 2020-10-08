# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# October 2020
# distributed_algorithm_test.py
# Test the distributed algorithm and tweak
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Step 1, calculate the export from every bus given angles
def export_calc():
    print('hellow world')


# Step 2.a, Calculate value of export with bus lambda
def bus_value():
    print('export value')


# Step 2.b, Calculate value of import with other buses lambda
def other_bus_value():
    print('import value')


# Step 3.a, Adjust lambda upward if price to produce > price received for export, down if else
def exported_lambda_calc():
    print('lambda adjust for export')


# Step 3.b, Adjust lambda to match power produced if not exporting
def no_export_lambda_calc():
    print('No export lambda calc')


# Step 4, Estimate desired generation at current lambda
def power_calc():
    print('power calc')


# Step 5, Calculate new angles such that they give the desired power flows
def angle_calc():
    print('angles across lines')


# The process runner, other functions to be fleshed out as this is built
if __name__ == '__main__':
    print('running the main')
