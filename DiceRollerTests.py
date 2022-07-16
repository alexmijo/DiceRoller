import DiceRollerCode

# Number of tests run
num_run = 0
# Number of tests that failed
num_failed = 0


def dice_sum_probability_unit_test():
    """ Returns boolean representing whether test passed or not. Prints results only if it fails.
    Increments num_tests no matter what, increments num_failed iff it fails. Only tests 2 dice 6
    faces and 1 dice 10 faces right now.
    """
    global num_run
    global num_failed
    num_run += 1
    failed = False
    # 2 dice 6 faces
    expecteds = {2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36,
                 7: 6/36, 8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36}
    for roll in range(2, 13):
        actual = DiceRollerCode.dice_sum_probability(roll, 2, 6)
        if (actual != expecteds[roll]):
            print(f"dice_sum_probability_unit_test: dice_sum_probability({roll}, 2, 6)")
            print("Expected:", expecteds[roll], "Actual:", actual)
            failed = True
    # 1 dice 10 faces
    expecteds = {1: 1/10, 2: 1/10, 3: 1/10, 4: 1/10, 5: 1/10,
                 6: 1/10, 7: 1/10, 8: 1/10, 9: 1/10, 10: 1/10}
    for roll in range(1, 11):
        actual = DiceRollerCode.dice_sum_probability(roll, 1, 10)
        if (actual != expecteds[roll]):
            print(f"dice_sum_probability_unit_test: dice_sum_probability({roll}, 1, 10)")
            print("Expected:", expecteds[roll], "Actual:", actual)
            failed = True
    if (failed):
        num_failed += 1

dice_sum_probability_unit_test()

if (num_failed == 0):
    print(num_run, "tests run. All tests passed.")
else:
    print(num_run, "tests run.", num_failed, "tests failed.")

dice = DiceRollerCode.DiceProbabilityDistribution(num_dice=2, num_sides=6, aggressiveness=2)
dice.frequencies = {2: 0, 3: 1, 4: 2, 5: 3, 6: 3, 7: 3, 8: 2, 9: 2, 10: 0, 11: 1, 12: 0}
dice.frequencies[2] -= 1
dice.update(2)
print(dice)
dice.update(11)
print(dice)