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
    <distribution> must be a dictionary containing all numerical values.
    """
    sum = 0
    for value in distribution.values():
        sum += value
    for key in distribution:
        distribution[key] /= sum


def normalized(distribution):
    """ Returns a normalized copy of the passed in distribution, where the sum of all the values
    equals 1. The ratios between the values stay the same. Bassically, the returned distribution
    contains all the passed in values divided by their sum.
    <distribution> must be a dictionary containing all numerical values.
    """
    normalized_distribution = distribution.copy()
    normalize(normalized_distribution)
    return normalized_distribution


def set_negative_values_to_0(distribution):
    """ Mutates the passed in distribution to make all values (not keys) which were negative become
    0. Values which weren't negative stay the same.
    <distribution> must be a dictionary containing all numerical values.
    """
    for key in distribution:
        if distribution[key] < 0:
            distribution[key] = 0


class GamblersFallacyDice:
    """ Represents dice which actually do exhibit the "gambler's fallacy". So, if an 8 hasn't been
    rolled in a long time, then an 8 actually is overdue and therefore will have a higher chance of
    being rolled than it would have otherwise. Essentially, if a roll has been underrepresented so
    far (it has been rolled fewer times than the expected value of how many times it'd be rolled in
    the amount of rolls that have occurred so far) its probability increases, and if a roll has been
    overrepresented so far its probability decreases. This has the effect of trending towards the
    long term average distribution of normal dice's rolls faster than normal dice would (but the
    distribution being trended to is the same). Can represent an arbitrary number of dice with an
    arbitrary number of faces, and a roll will be the sum of the rolls of all the dice.
    """

    def __init__(self, num_dice, num_sides, aggressiveness):
        """ Initializes an instance representing <num_dice> dice each with <num_sides> sides, which
        adjusts the probabilities to favor underrepresented rolls (and disfavor overrepresented
        rolls) with the passed in level of aggressiveness.
        <num_dice> and <num_sides> must both be positive integers.
        <aggressiveness> must be a non-negative number. An aggressiveness of 0 will result in normal
        dice which don't adjust probability according to the rolls that have occurred so far. The
        higher the aggressiveness, the more probabilities will be adjusted from their normal values,
        and the faster the normal long term average distribution of rolls will be trended towards.
        """
        self.aggressiveness = aggressiveness
        # Maps each possible roll to the probability of getting that roll on real, normal dice
        self.normal_probabilities = {roll: dice_sum_probability(
            roll, num_dice, num_sides) for roll in range(num_dice, num_dice * num_sides + 1)}
        # Initial probabilities will be those of normal dice
        self.probabilities = self.normal_probabilities.copy()
        # Maps each possible roll to the number of times it has been rolled so far on these dice
        self.frequencies = {roll: 0 for roll in range(num_dice, num_dice * num_sides + 1)}
        self.all_zeros_frequencies = self.frequencies.copy()
        # Previous self.frequencies maps to return to with undo/redo
        self.undo_states = []
        self.redo_states = []
        if use_multiplicative_adjusting:
            # Needed for solving the problem of when a roll's frequency is 0
            self.num_individual_dice_roll_permutations = num_sides ** num_dice

    def update_probabilities(self):
        """ Updates self.probabilities according to self.frequencies. Underrepresented rolls will
        tend to have higher probability than on normal dice, and overrepresented rolls will tend to
        have lower probability than on normal dice. The sorted order of the adjustments of
        probabilities will be guaranteed to be the same as the sorted order of underrepresentedness,
        i.e., if roll A is more underrepresented than roll B, than rolls A's probability adjustment
        (either multiplicative or additive, depending on the value of use_multiplicative_adjusting)
        will be greater than that of roll B.
        """
        if use_multiplicative_adjusting:
            # This is an experimental way of adhusting probability such that probability is
            #  guaranteed (I think) to increase monotonically with increasing underrepresentedness.
            #  IMO this isn't as good as the other, additive way of adjusting. It's called
            #  multiplicative because the normal probabilities are multiplied by a value determined
            #  by underrepresentedness.
            if self.frequencies == self.all_zeros_frequencies:
                self.probabilities = self.normal_probabilities.copy()
            else:
                for roll in self.frequencies:
                    # This solves the problem of when a roll's frequency is 0 (so the ratio of the
                    #  roll's frequency to its expected frequency is 0, which can't be used to
                    #  adjust probability since it'd be a divide by 0 error).
                    self.frequencies[roll] += self.normal_probabilities[roll] * \
                        self.num_individual_dice_roll_permutations
                for roll, fraction_of_rolls in normalized(self.frequencies).items():
                    deviation_from_expected = fraction_of_rolls / self.normal_probabilities[roll]
                    # TODO: See if using self.aggressiveness (or its inverse, depending on if
                    #  deviation_from_expected is > or < 1) in a multiplicative way makes this
                    #  method work better.
                    self.probabilities[roll] = self.normal_probabilities[roll] / \
                        (deviation_from_expected ** self.aggressiveness)
                for roll in self.frequencies:
                    # Undos the solution to the roll's frequency being 0 problem above, returning
                    #  self.frequencies back to its original value.
                    self.frequencies[roll] = round(self.frequencies[roll] - \
                        self.normal_probabilities[roll]*self.num_individual_dice_roll_permutations)
                normalize(self.probabilities)
        else:
            # My preferred way of adjusting probability. Probability isn't guaranteed to increase
            #  monotonically with increasing underrepresentedness using this method, but that's
            #  still pretty close to being the case and I don't think it's a big deal at all that
            #  it's not perfectly the case. It's called additive because a value determined by
            #  underrepresentedness is added to the normal probabilities.
            if self.frequencies == self.all_zeros_frequencies:
                self.probabilities = self.normal_probabilities.copy()
            else:
                for roll, fraction_of_rolls in normalized(self.frequencies).items():
                    deviation_from_expected = fraction_of_rolls - self.normal_probabilities[roll]
                    self.probabilities[roll] = self.normal_probabilities[roll] - \
                        self.aggressiveness * deviation_from_expected
                # I think that this (setting negative values to 0 and then normalizing) is why
                #  probability doesn't always increase monotonically with increasing
                #  underrepresentedness.
                set_negative_values_to_0(self.probabilities)
                normalize(self.probabilities)

    def roll_without_updating_frequencies(self):
        """ Returns a roll of these dice but the dice won't remember that this roll occurred, so
        the probabilities won't get adjusted.
        """
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
        """ Returns a roll of these dice and remembers that this roll occurred (which will cause
        probabilities to be changed).
        """
        # Since probabilities depend only on current frequencies, the state of the dice can be
        #  represented solely by self.frequencies.
        self.undo_states.append(self.frequencies.copy())
        self.redo_states = []
        roll = self.roll_without_updating_frequencies()
        self.frequencies[roll] += 1
        return roll

    def can_undo(self):
        """ Returns True if there is a previous state for these dice to return to with an undo,
        False otherwise.
        """
        if self.undo_states:
            return True
        return False

    def undo(self):
        """ Undoes the effects of the previous roll.
        """
        if self.can_undo():
            self.redo_states.append(self.frequencies.copy())
            self.frequencies = self.undo_states.pop()
        else:
            raise ValueError("Can't undo, no previous state to return to")

    def can_redo(self):
        """ Returns True if the last thing to be done with these dice was an undo (and we therefore
        are able to do a redo), False otherwise.
        """
        if self.redo_states:
            return True
        return False

    def redo(self):
        """ Redoes the effects of the previous roll which was just undone. Can be called multiple
        times in a row to redo multiple consecutive undos.
        """
        if self.can_redo():
            self.undo_states.append(self.frequencies.copy())
            self.frequencies = self.redo_states.pop()
        else:
            raise ValueError("Can't redo, no immediately recent undos to redo")

    def __str__(self):
        """ Returns a well formatted string which displays the current (adjusted) probabilities of
        rolling each possible roll and the number of times each roll has already occurred.
        Probabilities are rounded to the nearest percent.
        """
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
    """ Represents GamblersFallacyDice which distinguish between 7s rolled by different players.
    Acts the same as GamblersFallacyDice except that for purposes of determining probabilities (and
    not for purposes of displaying the number of times each roll has already been rolled) the number
    of 7s rolled so far is taken to be the number of players multiplied by the number of times the
    current player (the player who's turn it is to roll) has rolled a 7 so far. This causes players
    who've rolled less 7s than expected to have an increased chance of rolling a 7, and players
    who've rolled more 7s than expected to have a decreased chance of rolling a 7. This is useful
    because in Settlers of Catan rolling a 7 is very powerful and benefits only the player who's
    turn it is to roll.
    """

    def __init__(self, num_players, aggressiveness):
        """ See the docstring for GamblersFallacyDice.__init__(). Initializes with 2 six sided dice,
        and <num_players> players (which matters here for 7s).
        """
        GamblersFallacyDice.__init__(self, num_dice=2, num_sides=6, aggressiveness=aggressiveness)
        self.num_players = num_players
        # The player who's turn it is to roll
        self.curr_player = 1
        # Maps each player (integer 1 through num_players) to the number of times that player has
        #  rolled a 7. 
        self.players_seven_counts = {player: 0 for player in range(1, num_players + 1)}
        # We use the methods in GamblersFallacyDice to keep track of the previous states of
        #  self.frequencies, so the only additional work we need to do is keeping track of the
        #  previous states of self.players_seven_counts.
        self.undo_sevens_states = []
        self.redo_sevens_states = []

    # TODO: Add comments within the code below here in this class.
    def roll(self):
        """ Returns a roll of these dice and remembers that this roll occurred (which will cause
        probabilities to be changed).
        """
        self.undo_sevens_states.append(self.players_seven_counts.copy())
        self.redo_sevens_states = []
        # For purposes of determining probabilities the number of 7s rolled so far is taken to be
        #  the number of players multiplied by the number of times the current player has rolled a 7
        #  so far.
        self.frequencies[7] = self.players_seven_counts[self.curr_player] * self.num_players
        roll = GamblersFallacyDice.roll(self)
        if roll == 7:
            self.players_seven_counts[self.curr_player] += 1
            # It's not necessary to update self.frequencies[7] since that is set at the beggining
            #  of each call to roll(), and is unused by __str__().
        self.curr_player += 1
        if self.curr_player > self.num_players:
            self.curr_player = 1
        return roll

    def undo(self):
        """ Undoes the effects of the previous roll.
        """
        # GamblersFallacyDice.undo() deals with the state of self.frequencies.
        GamblersFallacyDice.undo(self)
        # We also need to deal with the states of self.players_seven_counts and self.curr_player.
        self.redo_sevens_states.append(self.players_seven_counts.copy())
        self.players_seven_counts = self.undo_sevens_states.pop()
        self.curr_player -= 1
        if self.curr_player < 1:
            self.curr_player = self.num_players

    def redo(self):
        """ Redoes the effects of the previous roll which was just undone. Can be called multiple
        times in a row to redo multiple consecutive undos.
        """
        # GamblersFallacyDice.redo() deals with the state of self.frequencies.
        GamblersFallacyDice.redo(self)
        # We also need to deal with the states of self.players_seven_counts and self.curr_player.
        self.undo_sevens_states.append(self.players_seven_counts.copy())
        self.players_seven_counts = self.redo_sevens_states.pop()
        self.curr_player += 1
        if self.curr_player > self.num_players:
            self.curr_player = 1

    def __str__(self):
        """ Returns a well formatted string which displays the current (adjusted) probabilities of
        rolling each possible roll and the number of times each roll has already occurred.
        Probabilities are rounded to the nearest percent. Players other than the current player have
        their number of previously rolled 7s displayed, but no corresponding probability is
        displayed (since it's impossible for any players other than the current player to roll a 7
        during the current player's turn).
        """
        # For purposes of determining probabilities the number of 7s rolled so far is taken to be
        #  the number of players multiplied by the number of times the current player has rolled a 7
        #  so far.
        self.frequencies[7] = self.players_seven_counts[self.curr_player] * self.num_players
        self.update_probabilities()
        string = ""
        for roll, probability in self.probabilities.items():
            if roll == 7:
                # For 7s, the frequencies will be in self.players_seven_counts rather than in
                #  self.frequencies.
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
