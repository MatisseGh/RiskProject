#Roll dice to generate order of play for all the players, and roll dice for attacking
import random


class Dice:
    def rol(self, attacker, defender=0): #attacker and defender is the amount of dice rolls the player has
        attack = [random.randint(1, 6)]
        defend = [random.randint(1, 6)]
        for i in range(attacker - 1):
            attack.append(random.randint(1, 6))
        for i in range(defender - 1):
            defend.append(random.randint(1, 6))
        attack.sort(reverse=True)
        defend.sort(reverse=True)
        m = [attack, defend] #return list where m[0] are the dice rolls (list) of the attacker and m[1] are the dice rolls (list) of the defender
        return m

    def rolTurn(self):
        return random.randint(1, 6)
