import DiceRoller

# Maximum difference between 2 floating point numbers for them to be considered equal
FLOAT_THRESHOLD = 0.00001
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
        actual = DiceRoller.dice_sum_probability(roll, 2, 6)
        if abs(actual - expecteds[roll]) > FLOAT_THRESHOLD:
            print(f"dice_sum_probability_unit_test: dice_sum_probability({roll}, 2, 6)")
            print("Expected:", expecteds[roll], "Actual:", actual)
            failed = True

    # 1 dice 10 faces
    expecteds = {1: 1/10, 2: 1/10, 3: 1/10, 4: 1/10, 5: 1/10,
                 6: 1/10, 7: 1/10, 8: 1/10, 9: 1/10, 10: 1/10}
    for roll in range(1, 11):
        actual = DiceRoller.dice_sum_probability(roll, 1, 10)
        if abs(actual - expecteds[roll]) > FLOAT_THRESHOLD:
            print(f"dice_sum_probability_unit_test: dice_sum_probability({roll}, 1, 10)")
            print("Expected:", expecteds[roll], "Actual:", actual)
            failed = True

    if failed:
        num_failed += 1


def normalize_unit_test():
    """ Returns boolean representing whether test passed or not. Prints results only if it fails.
    Increments num_tests no matter what, increments num_failed iff it fails.
    """
    global num_run
    global num_failed
    num_run += 1
    failed = False

    expected = {1: 1/10, 2: 2/10, 3: 3/10, 4: 4/10}
    distribution = {1: 2, 2: 4, 3: 6, 4: 8}
    original_distribution = distribution.copy()
    DiceRoller.normalize(distribution)
    for key in distribution:
        if abs(distribution[key] - expected[key]) > FLOAT_THRESHOLD:
            print(
                f"normalize_unit_test: distribution = {original_distribution},",
                "normalize(distribution)")
            print("Expected: mutation to", expected, "Actual:", distribution)
            failed = True

    expected = {1: 3/11, 2: 7/11, 3: 1/11, 4: 0}
    distribution = {1: 0.3, 2: 0.7, 3: 0.1, 4: 0}
    original_distribution = distribution.copy()
    DiceRoller.normalize(distribution)
    for key in distribution:
        if abs(distribution[key] - expected[key]) > FLOAT_THRESHOLD:
            print(
                f"normalize_unit_test: distribution = {original_distribution},",
                "normalize(distribution)")
            print("Expected: mutation to", expected, "Actual:", distribution)
            failed = True

    if (failed):
        num_failed += 1


dice_sum_probability_unit_test()
normalize_unit_test()

if (num_failed == 0):
    print(num_run, "tests run. All tests passed.")
else:
    print(num_run, "tests run.", num_failed, "tests failed.")


def for_finding_optimal_aggressiveness_no_split_7s(aggressiveness):
    """ Constructs a situation very likely to give a 100% chance of rolling a 7, if it is actually
    even particularly plausible to have a 100% chance roll at the given level of aggressiveness.
    Used for no split 7s Catan.
    """
    dice = DiceRoller.DiceProbabilityDistribution(
        num_dice=2, num_sides=6, aggressiveness=aggressiveness)
    dice.frequencies = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 5, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
    dice.frequencies[2] -= 1
    dice.update(2)
    print(dice)


def for_finding_optimal_aggressiveness(aggressiveness):
    """ Constructs a situation very likely to give a 100% chance of rolling a 6, if it is actually
    even particularly plausible to have a 100% chance roll at the given level of aggressiveness.
    Used for split 7s Catan (the normal Catan). Uses 2 players.
    """
    dice = DiceRoller.CatanDiceProbabilityDistribution(
        num_players=2, aggressiveness=aggressiveness)
    dice.probability_distributions[1].frequencies = {
        2: 1, 3: 2, 4: 3, 5: 4, 6: 3, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
    dice.probability_distributions[1].frequencies[2] -= 1
    dice.probability_distributions[1].update(2)
    dice.probability_distributions[2].frequencies = {
        2: 1, 3: 2, 4: 3, 5: 4, 6: 3, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
    dice.probability_distributions[2].frequencies[2] -= 1
    dice.probability_distributions[2].update(2)
    print(dice)

# 100 percent chance of a 7
# for_finding_optimal_aggressiveness_no_split_7s(35)
# 98 percent chance of a 7
# for_finding_optimal_aggressiveness_no_split_7s(34)
# 95 percent chance of a 7
# for_finding_optimal_aggressiveness_no_split_7s(33)
# 93 percent chance of a 7
# for_finding_optimal_aggressiveness_no_split_7s(32)
# 90 percent chance of a 7
# for_finding_optimal_aggressiveness_no_split_7s(31)
# 88 percent chance of a 7
# for_finding_optimal_aggressiveness_no_split_7s(30)
# 86 percent chance of a 7
# for_finding_optimal_aggressiveness_no_split_7s(30)
# 98 percent chance of a 7 when 4 sevens have already been rolled (instead of 5)
# for_finding_optimal_aggressiveness_no_split_7s(16.5)

# 100 percent chance of a 6
# for_finding_optimal_aggressiveness(18)
# 95 percent chance of a 6
# for_finding_optimal_aggressiveness(17)
# 90 percent chance of a 6
# for_finding_optimal_aggressiveness(16)
# 90 percent chance of a 6
# for_finding_optimal_aggressiveness(15)
# 85 percent chance of a 6
# for_finding_optimal_aggressiveness(14)
