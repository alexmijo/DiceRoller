import random
import math


def dice_sum_probability(sum, num_dice, num_sides):
    """ Returns the probability of getting <sum> points as the sum of rolling <num_dice> dice, each
    with <num_sides> sides.
    """
    # See https://mathworld.wolfram.com/Dice.html and/or
    #  https://www.lucamoroni.it/the-dice-roll-sum-problem/ for an explanation of the formula being
    #  computed here.
    probability = 0
    k_max = math.floor((sum - num_dice) / num_sides)
    for k in range(k_max + 1):
        probability += (-1)**k * math.comb(num_dice,
                                           k) * math.comb(sum - num_sides*k - 1, num_dice - 1)
    probability /= num_sides**num_dice
    return probability

def normalize(distribution):
    # TODO: Docstring
    sum = 0
    for value in distribution.values():
        sum += value
    for key in distribution:
        distribution[key] /= sum

def normalized(distribution):
    # TODO: Docstring
    normalized_distribution = distribution.copy()
    normalize(normalized_distribution)
    return normalized_distribution

def set_negative_values_to_0(distribution):
    # TODO: Docstring
    for key in distribution:
        if distribution[key] < 0:
            distribution[key] = 0

class DiceProbabilityDistribution:
    #TODO: Docstring

    def __init__(self, num_dice, num_sides):
        # TODO: Docstring
        self.probabilities = {roll: dice_sum_probability(
            roll, num_dice, num_sides) for roll in range(num_dice * num_sides)}
        self.classical_probabilities = self.probabilities.copy()
        self.frequencies = {roll: 0 for roll in range(num_dice * num_sides)}
        self.undo_states = []
        self.redo_states = []

    def update(self, new_roll):
        # TODO: Docstring
        # These will take up a lot of memory, but it's fine cause games aren't expected to last
        #  super long
        self.undo_states.append((self.probabilities.copy(), self.frequencies.copy()))
        self.redo_states = []
        self.frequencies[new_roll] += 1
        for roll, fraction_of_rolls in normalized(self.frequencies):
            # TODO: Maybe multiply deviation_from_expected by some constant such that
            #  set_negative_values_to_0 isn't necessary? Maybe that's not better though.
            deviation_from_expected = fraction_of_rolls - self.classical_probabilities[roll]
            self.probabilities[roll] = self.classical_probabilities[roll] - deviation_from_expected
        set_negative_values_to_0(self.probabilities)
        normalize(self.probabilities)

    def undo_update(self):
        # TODO: Docstring
        self.redo_states.append((self.probabilities, self.frequencies))
        self.probabilities, self.frequencies = self.undo_states.pop()

    def redo_update(self):
        # TODO: Docstring
        self.undo_states.append((self.probabilities, self.frequencies))
        self.probabilities, self.frequencies = self.redo_states.pop()

class CatanDiceProbabilityDistribution:
    # Nothing to inherit that wouldn't have to get overridden
    def __init__(self):
        DiceProbabilityDistribution.__init__(self, num_dice=2, num_sides=6)
        self.probabilities["Player One 7"] = self.probabilities[7]
        self.probabilities["Player Two 7"] = self.probabilities[7]
        del self.probabilities[7]
        self.current_player = 1
    


def main():
    mostRecentRoll = 0
    rolls = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0}
    chances = {2: 1.0/36, 3: 2.0/36, 4: 3.0/36, 5: 4.0/36, 6: 5.0/36,
               7: 6.0/36, 8: 5.0/36, 9: 4.0/36, 10: 3.0/36, 11: 2.0/36, 12: 1.0/36}
    biasedChances = chances.copy()
    numRolls = 0
    isPlayer1 = True

    # Program must be stopped with a keyboard interrupt
    while True:
        # TODO: Fix bug for double+ UNDOs
        if isPlayer1:
            prompt = "Player 1, press Enter to roll or type UNDO: "
        else:
            prompt = "Player 2, press Enter to roll or type UNDO: "
        if input(prompt) == "UNDO":
            if isPlayer1 and mostRecentRoll == 7:
                rolls[13] -= 1
            else:
                rolls[mostRecentRoll] -= 1
        else:
            # Get roll
            cumulative = 0.0
            rand = random.random()
            for roll in range(2, 13):
                cumulative += biasedChances[roll]
                if rand < cumulative:
                    mostRecentRoll = roll
                    break
            if isPlayer1:
                rolls[mostRecentRoll] += 1
            elif mostRecentRoll == 7:
                rolls[13] += 1
            else:
                rolls[mostRecentRoll] += 1
            print("")
            print("Roll: " + str(mostRecentRoll))
            print("")

        isPlayer1 = not isPlayer1

        # Find most overrepresented by finding largest R
        R = 0.0
        for roll in range(2, 13):
            if roll == 7:
                if isPlayer1:
                    newR = (rolls[7] * 2.0) / chances[7]
                else:
                    newR = (rolls[13] * 2.0) / chances[7]
            else:
                newR = rolls[roll] / chances[roll]
            if newR > R:
                R = newR

        s = 0
        for roll in range(2, 13):
            if roll == 7:
                if isPlayer1:
                    biasedChances[7] = chances[7] * R - (2.0 * rolls[7])
                else:
                    biasedChances[7] = chances[7] * R - (2.0 * rolls[13])
            else:
                biasedChances[roll] = chances[roll] * R - rolls[roll]
            s += biasedChances[roll]

        if s == 0:
            for roll in range(2, 13):
                biasedChances[roll] = chances[roll]
                if roll == 7 and not isPlayer1:
                    print(
                        " " + str(roll) + ": " + "{0:3d}".format(int(100 * biasedChances[roll])) +
                        "% chance, " + str(rolls[13]))
                else:
                    if roll < 10:
                        print(
                            " " + str(roll) + ": " + "{0:3d}".format(int(100 * biasedChances[roll])) +
                            "% chance, " + str(rolls[roll]))
                    else:
                        print(
                            str(roll) + ": " + "{0:3d}".format(int(100 * biasedChances[roll])) +
                            "% chance, " + str(rolls[roll]))
        else:
            for roll in range(2, 13):
                biasedChances[roll] = biasedChances[roll] / s
                biasedChances[roll] = biasedChances[roll] * 0.7 + chances[roll] * 0.3
                if roll == 7 and not isPlayer1:
                    print(
                        " " + str(roll) + ": " + "{0:3d}".format(int(100 * biasedChances[roll])) +
                        "% chance, " + str(rolls[13]))
                else:
                    if roll < 10:
                        print(
                            " " + str(roll) + ": " + "{0:3d}".format(int(100 * biasedChances[roll])) +
                            "% chance, " + str(rolls[roll]))
                    else:
                        print(
                            str(roll) + ": " + "{0:3d}".format(int(100 * biasedChances[roll])) +
                            "% chance, " + str(rolls[roll]))
