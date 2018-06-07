

class WorldStats:
    """this class holds all the statistics, it has to remain up-to-date
    It's a Singleton class, because every class has to see the same data"""

    def __init__(self):
        self.continents = list() #all the continents (with their countries)
        self.players = list() #all the participating players
        self.numberOfPlayers = 0
        self.countryGroups = list(list()) #a list of a list of neighboring countries with the same owner
        self.player = None #the active player

    def getPlayer(self):
        return self.players

    def getNumberOfPlayers(self):
        return self.numberOfPlayers

    def refactorPlayers(self):
        self.players = list()

    def addContinent(self, continent):
        self.continents.append(continent)

    def addPlayer(self, player):
        self.players.append(player)
        self.numberOfPlayers += 1

    def getCountries(self):
        """returns a shallow copy of the countries list"""
        countries = []
        for continent in self.continents:
            for country in continent.countries:
                countries.append(country)
        return countries

    def getCountryByName(self, countryName):
        """returns first country wound with given name, returns None if country is not found"""
        for continent in self.continents:
            for country in continent.countries:
                if country.name == countryName:
                    return country
        return None

    def getAttackableCountries(self, country): #get neighboring countries who are attackable
        attackableCountries = list()
        for land in country.neighbours:
            if land.player is not country.player:
                attackableCountries.append(land)
        return attackableCountries #return value = list of countries

    def exploreGroup(self, startCountry): #used BFS algorithm to make group with same owners
        # visits all the nodes of a graph (connected component) using BFS
        # keep track of all visited nodes
        explored = []
        # keep track of nodes to be checked
        queue = [startCountry]
        player = startCountry.player
        # keep looping until there are nodes still to be checked
        while queue:
            # pop shallowest node (first node) from queue
            node = queue.pop(0)
            if node not in explored and node.player is player:
                # add node to list of checked nodes
                explored.append(node)
                neighbours = node.neighbours

                # add neighbours of node to queue
                for neighbour in neighbours:
                    queue.append(neighbour)
        return explored #a list of a list of neighboring countries with the same owner

    def updateCountryGroups(self): #recalculate the countrygroups
        in_group = list()
        self.countryGroups = list(list())
        for continent in self.continents:
            for country in continent.countries:
                if country not in in_group:
                    group = self.exploreGroup(country)
                    in_group.extend(group)
                    self.countryGroups.append(group)

    def getCountryGroup(self, country): #return list of the countrygroup of a country
        for group in self.countryGroups:
            if country in group:
                return group

    def stepsToNearestEnemy(self, country): #how many steps to nearest enemy, uses BFS
        steps = 1
        amount_of_neighbours = len(country.neighbours)
        enemy_found = False
        explored = []
        queue = [country]
        while queue and not enemy_found:
            # pop shallowest node (first node) from queue
            node = queue.pop(0)
            if node not in explored:
                # add node to list of checked nodes
                if node.player is not country.player:
                    enemy_found = True
                    #print("found enemy:", node, ",", steps, "steps away")
                    continue
                explored.append(node)
                neighbours = node.neighbours
                # add neighbours of node to queue
                for neighbour in neighbours:
                    queue.append(neighbour)
                # each time all new neighbours are checked, add 'one' to the steps
                if amount_of_neighbours == 1:
                    amount_of_neighbours = 0
                    found = []
                    steps += 1
                    for element in queue:
                        if element not in explored:
                            if element not in found:
                                found.append(element)
                                amount_of_neighbours += 1
                elif node is not country:
                    amount_of_neighbours -= 1
        return steps

    def getGroup(self, country):
        for group in self.countryGroups:
            if country in group:
                return group
        return None

    def getContinentByCountry(self, country):
        for continent in self.continents:
            if country in continent.countries:
                return continent


instance = WorldStats() #the singleton instance
