from player import Player
import GUI.screenManager


class HumanPlayer(Player):

    def __init__(self, name, ID, countries, color): #
        Player.__init__(self, name, ID, countries, color)


    def addTroops(self, amount): #ask for input in gameboard and add amounts to countries
        self.troopsToPlace = amount
        amountPerCountry = GUI.screenManager.instance.gameboard.addTroopsInput(self)
        for country, number in amountPerCountry:
            country.addTroops(number)

    def attack(self): #attack another country. Gets its input from the gameboard (unlike the bot, who gets it from the Algorithm)
        troopDisplacement = GUI.screenManager.instance.gameboard.attackInput(self) #returns TroopDisplacement
        while troopDisplacement is not None: #keep attacking while it's effective
            fromCountry = troopDisplacement.fromCountry
            toCountry = troopDisplacement.toCountry
            amount = troopDisplacement.amount
            winner = self.attacking(amount, toCountry.amountOfTroops) #gets a list where the element with 0 is the loser
            #print("winner:", winner)
            if winner[1] == 0: #defender loses
                #fromCountry.removeTroops(amount - winner[0])
                fromCountry.removeTroops(amount)
                toCountry.amountOfTroops = winner[0]
                toCountry.setOwner(self)
            else: #attacker wins
                toCountry.amountOfTroops = winner[1]
                fromCountry.removeTroops(amount)
            troopDisplacement = GUI.screenManager.instance.gameboard.attackInput(self) #keep getting input, if the player chooses to do so

    def moveTroops(self): #move troops to another country. Gets input from gameboard
        troopDisplacement = GUI.screenManager.instance.gameboard.moveInput(self) #returns troopDisplacement
        if troopDisplacement is not None:
            fromCountry = troopDisplacement.fromCountry
            toCountry = troopDisplacement.toCountry
            amount = troopDisplacement.amount
            fromCountry.removeTroops(amount)
            toCountry.addTroops(amount)

    def addTroops2(self): #addTroops only adds troops to a country, but doesn't remove them from the original country
                          #addTroops2 also removes them from the original country
        placement = GUI.screenManager.instance.gameboard.addTroopsInput(self) #returns dict with key: country, value=amount of troops to add
        for country in placement:
            country.addTroops(placement[country])
            self.troopsToPlace -= placement[country]
