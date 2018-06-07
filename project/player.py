from dice import Dice
import worldstats
#quintenx3


class Player:

    def __init__(self, name, ID, countries, color):
        self.name = name
        self.ID = ID
        self.countries = countries
        self.troopsToPlace = 3 #default
        self.color = color #the color of the player in the GUI

    # quintenx3 , this is a methode that helps the methode attack (thats gonna be implementated in bot and human) so we dont use 2 times the same code.
    def attacking(self, attackTroops, defenceTroops): #attack another player using Dice rolls
        h1 = attackTroops
        h2 = defenceTroops
        while h1 > 0 and h2 > 0:
            helpattack = h1
            helpdefence = h2
            if helpattack > 3: #reduce the number of Dice rolls (see Risk instructions)
                helpattack = 3
            if helpdefence > 2:
                helpdefence = 2
            d = Dice()
            m = d.rol(helpattack, helpdefence)
            if m[0][0] > m[1][0]:
                h2 = h2 - 1
            elif m[0][0] <= m[1][0]:
                h1 = h1 - 1
            if not (len(m[0]) < 2 or len(m[1]) < 2):
                if m[0][1] > m[1][1]:
                    h2 = h2 - 1
                elif m[0][1] <= m[1][1]:
                    h1 = h1 - 1
        h = [h1, h2]
        return h #return a list where h1 are the remaining troops of the attacker, h2 from the defender. The element with 0 is the loser

    def addTroops(int): #abstract method
        raise NotImplementedError('subclasses must override addTroops')

    def moveTroops(self): #abstract method
        raise NotImplementedError('subclasses must override addTroops')

    def attack(self): #abstract method
        raise NotImplementedError('subclasses must override addTroops')

    def updateCountryList(self): #update the countries the player owns
        self.countries = list()
        allCountries = worldstats.instance.continents.countries
        for country in allCountries:
            if country.player is self:
                self.countries.append(country)

    def getName(self):
        return self.name

    def getID(self):
        return self.ID

    def getCountries(self):
        return self.countries

    # wouter:
    def addCountry(self, newCountry):
        if newCountry not in self.countries:
            self.countries.append(newCountry)
        if newCountry.player is not self:
            newCountry.setOwner(self)

    def removeCountry(self, country):
        self.countries.remove(country)
        if country.getOwner is self:
            country.setOwner(None)

    def roundBonus(self): #calculate the amount of troops the player deserves after each round
        continentBonus = 0
        for continent in worldstats.instance.continents:
            if self.ownsContinent(continent) is True:
                continentBonus += continent.bonus
        if len(self.countries) < 10:
            roundBonus = 3
        else:
            roundBonus = len(self.countries) // 3
        return roundBonus + continentBonus #roundBonus = owned countries/3, continentBonus = continent.bonus

    def ownsContinent(self, continent): #does the player owns the whole continent?
        counter = 0
        for country in continent.countries:
            if country.player is self:
                counter += 1
        if counter == len(continent.countries):
            return True
        return False

    def __repr__(self):
        return self.name
