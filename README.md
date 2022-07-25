# DiceRoller
Originally used for making settlers of catan slightly more skill based and less random. Program written in Python which simulates rolling and summing n different s-sided
dice. One way in which it differs from normal dice is that the sum’s probability distribution is adjusted according to previous rolls so that the dice exhibit the
“Gambler’s Fallacy", in that if (for example) an 8 hasn't been rolled in a while, then it actually is overdue and the probability of the next roll being an 8 will
actually be higher than if many 8s have been rolled. The frequencies of rolls trend towards the same long term average distribution as normal dice, but faster.
It also has the ability to make sure that each of an arbitrary different number of players who take turns rolling the dice roll 7s at roughly equal frequencies, achieving
this by increasing the probability of rolling a 7 for a player who has rolled fewer 7s than would be expected, and decreasing the probability of rolling a 7 for a player
who has rolled more 7s than would be expected. Has a text based UI which I run in the shell to play Settlers of Catan (the only board game I've used this for so far,
although it'd work for any game with dice), and allows for undoing and redoing rolls as well.
