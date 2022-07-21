import random
import math

# Set to True in order to use an experimental (and IMO not as good) way of adhusting probability
#  such that probability is guaranteed (I think) to increase monotonically with increasing
#  underrepresentedness
use_multiplicative_adjusting = False


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
    """ Mutates the passed in distribution to make the sum of all its values equal 1. The ratios
    between the values stay the same. Bassically, it just divides all values by the sum of the
    values.
    <distribution> must be a dictionary containing all integer values.
    """
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


class GamblersFallacyDice:
    #TODO: Docstring

    def __init__(self, num_dice, num_sides, aggressiveness):
        # TODO: Docstring
        self.aggressiveness = aggressiveness
        # Maps each possible roll to the probability of getting that roll on real, normal dice
        self.normal_probabilities = {roll: dice_sum_probability(
            roll, num_dice, num_sides) for roll in range(num_dice, num_dice * num_sides + 1)}
        self.probabilities = self.normal_probabilities.copy()
        # Maps each possible roll to the number of times it has been rolled so far on these dice
        self.frequencies = {roll: 0 for roll in range(num_dice, num_dice * num_sides + 1)}
        self.all_zeros_frequencies = self.frequencies.copy()
        # Previous self.frequencies maps to return to with undo/redo
        self.undo_states = []
        self.redo_states = []

    def update_probabilities(self):
        # TODO: Docstring
        if use_multiplicative_adjusting:
            if self.frequencies == self.all_zeros_frequencies:
                self.probabilities = self.normal_probabilities.copy()
            else:
                for roll in self.frequencies:
                    self.frequencies[roll] += self.normal_probabilities[roll] * 36
                for roll, fraction_of_rolls in normalized(self.frequencies).items():
                    deviation_from_expected = fraction_of_rolls / self.normal_probabilities[roll]
                    self.probabilities[roll] = self.normal_probabilities[roll] / \
                        (deviation_from_expected ** self.aggressiveness)
                for roll in self.frequencies:
                    self.frequencies[roll] = round(
                        self.frequencies[roll] - self.normal_probabilities[roll] * 36)
                normalize(self.probabilities)
        else:
            if self.frequencies == self.all_zeros_frequencies:
                self.probabilities = self.normal_probabilities.copy()
            else:
                for roll, fraction_of_rolls in normalized(self.frequencies).items():
                    deviation_from_expected = fraction_of_rolls - self.normal_probabilities[roll]
                    self.probabilities[roll] = self.normal_probabilities[roll] - \
                        self.aggressiveness * deviation_from_expected
                set_negative_values_to_0(self.probabilities)
                normalize(self.probabilities)

    def roll_without_updating_frequencies(self):
        # TODO: Docstring
        self.update_probabilities()
        rand = random.random()
        cumulative = 0
        for roll, probability in self.probabilities.items():
            cumulative += probability
            if rand < cumulative:
                return roll
        # Only needed because floating point errors could cause probabilities to sum to < 1
        return roll

    def roll(self):
        # TODO: Docstring
        self.undo_states.append(self.frequencies.copy())
        self.redo_states = []
        roll = self.roll_without_updating_frequencies()
        self.frequencies[roll] += 1
        return roll

    def can_undo(self):
        # TODO: Docstring
        if self.undo_states:
            return True
        return False

    def undo(self):
        # TODO: Docstring
        if self.can_undo():
            self.redo_states.append(self.frequencies.copy())
            self.frequencies = self.undo_states.pop()
        else:
            raise ValueError("Can't undo, no previous state to return to")

    def can_redo(self):
        # TODO: Docstring
        if self.redo_states:
            return True
        return False

    def redo(self):
        # TODO: Docstring
        if self.can_redo():
            self.undo_states.append(self.frequencies.copy())
            self.frequencies = self.redo_states.pop()
        else:
            raise ValueError("Can't redo, no immediately recent undos to redo")

    def __str__(self):
        # TODO: Docstring
        self.update_probabilities()
        string = ""
        for roll, probability in self.probabilities.items():
            if roll < 10:
                string += "\n " + str(roll) + ": " + "{0:3d}".format(
                    round(100 * probability)) + "% chance, " + str(self.frequencies[roll])
            else:
                # TODO: Remove this clause
                string += "\n" + str(roll) + ": " + "{0:3d}".format(
                    round(100 * probability)) + "% chance, " + str(self.frequencies[roll])
        return string


class CatanDice(GamblersFallacyDice):
    # TODO: Docstring

    def __init__(self, num_players, aggressiveness):
        # TODO: Docstring
        GamblersFallacyDice.__init__(self, num_dice=2, num_sides=6, aggressiveness=aggressiveness)
        self.num_players = num_players
        self.curr_player = 1
        self.players_seven_counts = {player: 0 for player in range(1, num_players + 1)}
        self.undo_sevens_states = []
        self.redo_sevens_states = []

    def roll(self):
        self.undo_sevens_states.append(self.players_seven_counts.copy())
        self.redo_sevens_states = []
        self.frequencies[7] = self.players_seven_counts[self.curr_player] * self.num_players
        roll = GamblersFallacyDice.roll(self)
        if roll == 7:
            self.players_seven_counts[self.curr_player] += 1
            self.frequencies[7] = self.players_seven_counts[self.curr_player] * self.num_players
        self.curr_player += 1
        if self.curr_player > self.num_players:
            self.curr_player = 1
        return roll

    def undo(self):
        # TODO: Docstring
        GamblersFallacyDice.undo(self)
        self.redo_sevens_states.append(self.players_seven_counts.copy())
        self.players_seven_counts = self.undo_sevens_states.pop()
        self.curr_player -= 1
        if self.curr_player < 1:
            self.curr_player = self.num_players

    def redo(self):
        # TODO: Docstring
        GamblersFallacyDice.redo(self)
        self.undo_sevens_states.append(self.players_seven_counts.copy())
        self.players_seven_counts = self.redo_sevens_states.pop()
        self.curr_player += 1
        if self.curr_player > self.num_players:
            self.curr_player = 1

    def __str__(self):
        self.frequencies[7] = self.players_seven_counts[self.curr_player] * self.num_players
        self.update_probabilities()
        string = ""
        for roll, probability in self.probabilities.items():
            if roll == 7:
                for player, seven_count in sorted(self.players_seven_counts.items()):
                    if player == self.curr_player:
                        string += "\nPlayer " + str(player) + " 7: " + "{0:3d}".format(
                            round(100 * probability)) + "% chance, " + str(seven_count)
                    else:
                        string += "\nPlayer " + str(player) + " 7:              " + str(seven_count)
            elif roll < 10:
                string += "\n         " + str(roll) + ": " + "{0:3d}".format(
                    round(100 * probability)) + "% chance, " + str(self.frequencies[roll])
            else:
                # TODO: Remove this clause
                string += "\n        " + str(roll) + ": " + "{0:3d}".format(
                    round(100 * probability)) + "% chance, " + str(self.frequencies[roll])
        return string


# Escape character sequence for turning the background of printed text red
RED_BACKGROUND = "\033[41m"
# Escape character sequence for turning printed text the shell's default color (and style)
DEFAULT_COLOR = "\033[0m"
# Escape character sequence for turning printed text light yellow (console) or bold and yellow
#  (xterm)
YELLOW = "\033[1;33m"


def run_catan(num_players, aggressiveness):
    # TODO: Docstring
    dice = CatanDice(num_players, aggressiveness)
    while True:
        print(dice)
        prompt = f"Player {dice.curr_player}'s turn. "
        if dice.can_undo() and dice.can_redo():
            prompt += "Press Enter to roll, Ctrl+c to quit, or type UNDO or REDO: "
        elif dice.can_undo():
            prompt += "Press Enter to roll, Ctrl+c to quit, or type UNDO: "
        elif dice.can_redo():
            prompt += "Press Enter to roll, Ctrl+c to quit, or type REDO: "
        else:
            prompt += "Press Enter to roll or Ctrl+c to quit: "
        try:
            user_input = input(prompt)
        except KeyboardInterrupt:
            print()
            break
        if user_input == "UNDO":
            try:
                dice.undo()
                print("Successful undo")
            except ValueError as e:
                print(e)
        elif user_input == "REDO":
            try:
                dice.redo()
                print("Successful redo")
            except ValueError as e:
                print(e)
        elif user_input == "":
            print(RED_BACKGROUND + "Roll:" + DEFAULT_COLOR,
                  YELLOW + str(dice.roll()) + DEFAULT_COLOR)
        else:
            print("Invalid input, no action done")


def run_no_split_7s_catan(num_players, aggressiveness):
    # TODO: Docstring
    dice = GamblersFallacyDice(num_dice=2, num_sides=6, aggressiveness=aggressiveness)
    player = 1
    # Just keyboard interrupt to stop
    while True:
        player = player % num_players
        if player == 0:
            player = num_players
        print(dice)
        prompt = f"Player {player}'s turn. "
        if dice.can_undo() and dice.can_redo():
            prompt += "Press Enter to roll, Ctrl+c to quit, or type UNDO or REDO: "
        elif dice.can_undo():
            prompt += "Press Enter to roll, Ctrl+c to quit, or type UNDO: "
        elif dice.can_redo():
            prompt += "Press Enter to roll, Ctrl+c to quit, or type REDO: "
        else:
            prompt += "Press Enter to roll or Ctrl+c to quit: "
        try:
            user_input = input(prompt)
        except KeyboardInterrupt:
            print()
            break
        if user_input == "UNDO":
            try:
                dice.undo()
                player -= 1
                print("Successful undo")
            except ValueError as e:
                print(e)
        elif user_input == "REDO":
            try:
                dice.redo()
                player += 1
                print("Successful redo")
            except ValueError as e:
                print(e)
        elif user_input == "":
            print(RED_BACKGROUND + "Roll: " + DEFAULT_COLOR,
                  YELLOW + str(dice.roll()) + DEFAULT_COLOR)
            player += 1
        else:
            print("Invalid input, no action done")


def old_run_catan():
    # TODO: Docstring or maybe remove
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


if __name__ == "__main__":
    # aggressiveness=15 seems good for 2 players at least
    run_catan(num_players=2, aggressiveness=15)
