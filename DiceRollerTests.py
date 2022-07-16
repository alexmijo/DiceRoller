import DiceRollerCode

# Number of tests run
num_run = 0
# Number of tests that failed
num_failed = 0

def dice_sum_probability_unit_test():
    """ Returns boolean representing whether test passed or not. Prints results only if it fails.
    Increments num_tests no matter what, increments num_failed iff it fails.
    """
    global num_run
    global num_failed
    num_run += 1
    expecteds = {2: 1.0/36, 3: 2.0/36, 4: 3.0/36, 5: 4.0/36, 6: 5.0/36,
                 7: 6.0/36, 8: 5.0/36, 9: 4.0/36, 10: 3.0/36, 11: 2.0/36, 12: 1.0/36}
    for roll in range(2, 13):
        actual = DiceRollerCode.dice_sum_probability(roll, 2, 6)
        if (actual != expecteds[roll]):
            print("dice_sum_probability_unit_test: dice_sum_probability(%1, 2, 6)")
            print("Expected:", expecteds[roll], "Actual:", actual)
            num_failed += 1

dice_sum_probability_unit_test()

if (num_failed == 0):
    print(num_run, "tests run. All tests passed.")
else:
    print(num_run, "tests run.", num_failed, "tests failed.")