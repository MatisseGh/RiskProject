

class Continent:

    #Matisse
    def __init__(self, name, bonus, countries):
        self.name = name
        self.bonus = bonus #a bonus (= certain amount of troops) if one player owns the continent
        self.countries = countries
        self.ownership = dict() #key: player, value: percentage of ownership of continent

    def calculateOwnership(self):
        self.ownership.clear()
        numberOfCountriesInContinent = len(self.countries)
        aandeelPerCountry = 100 / numberOfCountriesInContinent #value is a decimal (no floats), helps with rounding errors
        for country in self.countries:
            owner = country.getOwner() #getter for name of owner of country
            aandeel = self.ownership.get(owner)
            if aandeel is None:
                self.ownership[owner] = aandeelPerCountry
            else:
                nieuwAandeel = self.ownership.get(owner) + aandeelPerCountry
                self.ownership[owner] = nieuwAandeel
        return self.ownership

    def getBonus(self):
        return self.bonus

    def getOwnership(self):
        return self.ownership

    def getConnections(self): #how many connections with other continents
        amount = 0
        for country in self.countries:
            for Neigbour in country.neighbours: #check neighbours of countries and see if they're from another continent
                if Neigbour not in self.countries:
                    amount += 1
        return amount

    def __repr__(self):
        return self.name
