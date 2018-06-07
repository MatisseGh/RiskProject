from player import Player
from algorithm import Algorithm
from humanplayer import HumanPlayer
import GUI.screenManager


class Bot(Player):

    def __init__(self, name, ID, countries, color):
        Player.__init__(self, name, ID, countries, color)
        self.algo = Algorithm(self) #uses Algorithm to make a move
        self.troopsToPlace = 0

    def addTroops(self, amount): #add troops to countries chosen by Algorithm
        self.troopsToPlace = amount
        troops_per_country = self.algo.bestAddingTroops() #dict with troops to add to a country
        if troops_per_country is None:
            return None
        counter = 0
        for country in troops_per_country:
            country.addTroops(troops_per_country[country])
            counter += troops_per_country[country]

    def moveTroops(self): #move troops to countries chosen by Algorithm
        troopDisplacement = self.algo.bestMoveTroops() #returns TroopDisplament
        if troopDisplacement is not None:
            fromCountry = troopDisplacement.fromCountry
            toCountry = troopDisplacement.toCountry
            amount = troopDisplacement.amount
            fromCountry.removeTroops(amount)
            toCountry.addTroops(amount)

    def attack(self): #attack countries chosen by Algorithm
        counter = 0
        troopDisplacement = self.algo.bestAttack() #returns TroopDisplacement
        while troopDisplacement is not None: #while it's effective, keep attacking
            counter += 1
            fromCountry = troopDisplacement.fromCountry
            toCountry = troopDisplacement.toCountry
            amount = troopDisplacement.amount
            if isinstance(toCountry.player, HumanPlayer):
                GUI.screenManager.instance.gameboard.botAttackPopUp(self, toCountry.player, amount, toCountry)
            winner = self.attacking(amount, toCountry.amountOfTroops)
            if winner[1] == 0:
                fromCountry.removeTroops(amount)
                toCountry.setTroops(winner[0])
                toCountry.setOwner(self)

            else:
                toCountry.setTroops(winner[1])
                fromCountry.removeTroops(amount)
            GUI.screenManager.instance.gameboard.statusBarChangeText(self.name + " attacked " + toCountry.name +
                                                                     " from " + fromCountry.name + " with " + str(amount))
            troopDisplacement = self.algo.bestAttack() #after each attack -> state changes -> recalculate the attack
