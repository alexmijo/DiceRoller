import random

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
