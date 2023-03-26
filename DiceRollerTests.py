import DiceRoller

# TODO: Figure out some Python testing utility to use in the future, instead of doing a lot of this
#  stuff manually. Actually, probably do that before I finish implementing the rest of these tests
#  manually, and then just use that for all these tests. Look for something like JUnit but for
#  Python.

# Maximum difference between 2 floating point numbers for them to be considered equal
FLOAT_THRESHOLD = 0.00001


def floats_equal_up_to_float_threshold(float1, float2):
    """ Returns True if the absolute value of the difference between <float1> and <float2> is at
    most FLOAT_THRESHOLD.
    <float1> and <float2> must both be numbers.
    """
    return abs(float1 - float2) <= FLOAT_THRESHOLD


def dicts_equal_up_to_float_threshold(dict1, dict2):
    """ Returns True if <dict1> and <dict2> are equal, where two float values (not keys) are
    considered equal iff the absolute value of their difference is at most FLOAT_THRESHOLD.
    Returns False otherwise.
    <dict1> and <dict2> must both be dictionaries whose values are all numbers.
    """
    if len(dict1) != len(dict2):
        return False
    for key in dict1:
        if key not in dict2:
            return False
        if not floats_equal_up_to_float_threshold(dict1[key], dict2[key]):
            return False
    return True


# Number of tests run
num_run = 0
# Number of tests that failed
num_failed = 0


def dice_sum_probability_test():
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
        if not floats_equal_up_to_float_threshold(actual, expecteds[roll]):
            print(f"dice_sum_probability_test: dice_sum_probability({roll}, 2, 6)")
            print("Expected:", expecteds[roll], "Actual:", actual)
            failed = True

    # 1 dice 10 faces
    expecteds = {1: 1/10, 2: 1/10, 3: 1/10, 4: 1/10, 5: 1/10,
                 6: 1/10, 7: 1/10, 8: 1/10, 9: 1/10, 10: 1/10}
    for roll in range(1, 11):
        actual = DiceRoller.dice_sum_probability(roll, 1, 10)
        if not floats_equal_up_to_float_threshold(actual, expecteds[roll]):
            print(f"dice_sum_probability_test: dice_sum_probability({roll}, 1, 10)")
            print("Expected:", expecteds[roll], "Actual:", actual)
            failed = True

    if failed:
        num_failed += 1


def normalize_test():
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
    if not dicts_equal_up_to_float_threshold(distribution, expected):
        print(
            f"normalize_test: distribution = {original_distribution},",
            "normalize(distribution)")
        print("Expected: mutation to", expected, "Actual:", distribution)
        failed = True

    expected = {1: 3/11, 2: 7/11, 3: 1/11, 4: 0}
    distribution = {1: 0.3, 2: 0.7, 3: 0.1, 4: 0}
    original_distribution = distribution.copy()
    DiceRoller.normalize(distribution)
    if not dicts_equal_up_to_float_threshold(distribution, expected):
        print(
            f"normalize_test: distribution = {original_distribution},",
            "normalize(distribution)")
        print("Expected: mutation to", expected, "Actual:", distribution)
        failed = True

    if (failed):
        num_failed += 1


def normalized_test():
    """Returns boolean representing whether test passed or not. Prints results only if it fails.
    Increments num_tests no matter what, increments num_failed iff it fails.
    """
    global num_run
    global num_failed
    num_run += 1
    failed = False

    expected = {1: 1.5/10, 2: 1.5/10, 3: 3/10, 4: 0, 5: 4/10}
    distribution = {1: 3, 2: 3, 3: 6, 4: 0, 5: 8}
    original_distribution = distribution.copy()
    normalized_distribution = DiceRoller.normalized(distribution)
    if not dicts_equal_up_to_float_threshold(distribution, original_distribution):
        print(
            f"normalized_test: distribution = {original_distribution},",
            "normalized(distribution)")
        print("Expected: no mutation", "Actual: distribution mutated to", distribution)
        failed = True
    if not dicts_equal_up_to_float_threshold(normalized_distribution, expected):
        print(
            f"normalized_test: distribution = {original_distribution},",
            "normalized(distribution)")
        print("Expected:", expected, "Actual:", normalized_distribution)
        failed = True

    expected = {1: 3/11, 2: 7/11, 3: 0.5/11, 4: 0.5/11}
    distribution = {1: 0.3, 2: 0.7, 3: 0.05, 4: 0.05}
    original_distribution = distribution.copy()
    normalized_distribution = DiceRoller.normalized(distribution)
    if not dicts_equal_up_to_float_threshold(distribution, original_distribution):
        print(
            f"normalized_test: distribution = {original_distribution},",
            "normalized(distribution)")
        print("Expected: no mutation", "Actual: distribution mutated to", distribution)
        failed = True
    if not dicts_equal_up_to_float_threshold(normalized_distribution, expected):
        print(
            f"normalized_test: distribution = {original_distribution},",
            "normalized(distribution)")
        print("Expected:", expected, "Actual:", normalized_distribution)
        failed = True

    if (failed):
        num_failed += 1


def set_negative_values_to_0_test():
    """ Returns boolean representing whether test passed or not. Prints results only if it fails.
    Increments num_tests no matter what, increments num_failed iff it fails.
    """
    global num_run
    global num_failed
    num_run += 1
    failed = False

    expected = {1: 2, 2: 0, 3: 0, 4: 8}
    distribution = {1: 2, 2: -4, 3: -6, 4: 8}
    original_distribution = distribution.copy()
    DiceRoller.set_negative_values_to_0(distribution)
    if not dicts_equal_up_to_float_threshold(distribution, expected):
        print(
            f"set_negative_values_to_0_test: distribution = {original_distribution},",
            "set_negative_values_to_0(distribution)")
        print("Expected: mutation to", expected, "Actual:", distribution)
        failed = True

    expected = {1: 0.3, 2: 0, 3: 0.1, 4: 0}
    distribution = {1: 0.3, 2: -0.7, 3: 0.1, 4: 0}
    original_distribution = distribution.copy()
    DiceRoller.set_negative_values_to_0(distribution)
    if not dicts_equal_up_to_float_threshold(distribution, expected):
        print(
            f"set_negative_values_to_0_test: distribution = {original_distribution},",
            "set_negative_values_to_0(distribution)")
        print("Expected: mutation to", expected, "Actual:", distribution)
        failed = True

    if (failed):
        num_failed += 1


class GamblersFallacyDiceTests:
    # TODO: Deal with this, put it somewhere at beggining of module, not in each docstring.
    """ All tests returns boolean representing whether test passed or not. All tests prints results only if test
    fails. Increments num_tests no matter what, increments num_failed iff it fails.
    """

    def init_test():
        """ Returns boolean representing whether test passed or not. Prints results only if it fails.
        Increments num_tests no matter what, increments num_failed iff it fails.
        """
        global num_run
        global num_failed
        num_run += 1
        failed = False

        num_dice, num_sides, aggressiveness = 2, 6, 8
        dice = DiceRoller.GamblersFallacyDice(num_dice, num_sides, aggressiveness)
        if dice.aggressiveness != aggressiveness:
            print(
                f"GamblersFallacyDiceTests.__init__test:",
                "dice = DiceRoller.GamblersFallacyDice({num_dice}, {num_sides}, {aggressiveness})")
            print("Expected dice.aggressiveness:", aggressiveness, "Actual:", dice.aggressiveness)
            failed = True
        expected_frequencies = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
        if dice.frequencies != expected_frequencies:
            print(
                f"GamblersFallacyDiceTests.__init__test:",
                "dice = DiceRoller.GamblersFallacyDice({num_dice}, {num_sides}, {aggressiveness})")
            print("Expected dice.frequencies:", expected_frequencies, "Actual:", dice.frequencies)
            failed = True
        expected_probabilities = {2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36,
                                  6: 5/36, 7: 6/36, 8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36}
        if not dicts_equal_up_to_float_threshold(dice.probabilities, expected_probabilities):
            print(
                f"GamblersFallacyDiceTests.__init__test:",
                "dice = DiceRoller.GamblersFallacyDice({num_dice}, {num_sides}, {aggressiveness})")
            print(
                "Expected dice.probabilities:", expected_probabilities, "Actual:",
                dice.probabilities)
            failed = True
        if dice.redo_states or dice.undo_states:
            print(
                f"GamblersFallacyDiceTests.__init__test:",
                "dice = DiceRoller.GamblersFallacyDice({num_dice}, {num_sides}, {aggressiveness})")
            print(
                "Expected dice.redo_states and dice.undo_states to be empty lists",
                "Actual dice.redo_states:", dice.redo_states, "Actual dice.undo_states:",
                dice.undo_states)
            failed = True

        if (failed):
            num_failed += 1

    def update_probabilities_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1

    def roll_without_updating_frequencies_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1

    def roll_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1

    def can_undo_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1

    def undo_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1

    def can_redo_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1

    def redo_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1

    def str_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1


class CatanDiceTests:
    def init_test():
        # TODO: Modify this to actually use CatanDice (currently just copied from
        #  GamblersFallacyDiceTests.init_test())
        global num_run
        global num_failed
        num_run += 1
        failed = False

        num_dice, num_sides, aggressiveness = 2, 6, 8
        dice = DiceRoller.GamblersFallacyDice(num_dice, num_sides, aggressiveness)
        if dice.aggressiveness != aggressiveness:
            print(
                f"GamblersFallacyDiceTests.__init__test:",
                "dice = DiceRoller.GamblersFallacyDice({num_dice}, {num_sides}, {aggressiveness})")
            print("Expected dice.aggressiveness:", aggressiveness, "Actual:", dice.aggressiveness)
            failed = True
        expected_frequencies = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
        if dice.frequencies != expected_frequencies:
            print(
                f"GamblersFallacyDiceTests.__init__test:",
                "dice = DiceRoller.GamblersFallacyDice({num_dice}, {num_sides}, {aggressiveness})")
            print("Expected dice.frequencies:", expected_frequencies, "Actual:", dice.frequencies)
            failed = True
        expected_probabilities = {2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36,
                                  6: 5/36, 7: 6/36, 8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36}
        if not dicts_equal_up_to_float_threshold(dice.probabilities, expected_probabilities):
            print(
                f"GamblersFallacyDiceTests.__init__test:",
                "dice = DiceRoller.GamblersFallacyDice({num_dice}, {num_sides}, {aggressiveness})")
            print(
                "Expected dice.probabilities:", expected_probabilities, "Actual:",
                dice.probabilities)
            failed = True
        if dice.redo_states or dice.undo_states:
            print(
                f"GamblersFallacyDiceTests.__init__test:",
                "dice = DiceRoller.GamblersFallacyDice({num_dice}, {num_sides}, {aggressiveness})")
            print(
                "Expected dice.redo_states and dice.undo_states to be empty lists",
                "Actual dice.redo_states:", dice.redo_states, "Actual dice.undo_states:",
                dice.undo_states)
            failed = True

        if (failed):
            num_failed += 1

    def update_probabilities_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1

    def roll_without_updating_frequencies_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1

    def roll_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1

    def can_undo_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1

    def undo_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1

    def can_redo_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1

    def redo_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1

    def str_test():
        global num_run
        global num_failed
        num_run += 1
        failed = False

        # TODO

        if (failed):
            num_failed += 1


dice_sum_probability_test()
normalize_test()
normalized_test()
set_negative_values_to_0_test()
GamblersFallacyDiceTests.init_test()

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


print({roll: DiceRoller.dice_sum_probability(roll, 4, 4) * 4**4 for roll in range(4, 16 + 1)})