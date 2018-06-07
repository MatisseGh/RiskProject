

class Country:
    def __init__(self, name, x, y, neighbours=[]):
        self.name = name
        self.x = x
        self.y = y
        self.neighbours = neighbours.copy()
        self.amountOfTroops = 1 #every country has at least one troop
        self.player = None #owner
        self.drawable = None #For the GUI

    def __repr__(self):
        return self.name

    def setTroops(self, amount):
        self.amountOfTroops = amount

    def getOwner(self):
        return self.player

    def addTroops(self, amount):
        self.amountOfTroops += amount
        if self.drawable is not None:
            self.drawable.fetch_latest_data() #update GUI

    def getNeigbours(self):
        return self.neighbours.copy()

    def removeTroops(self, amount):
        self.amountOfTroops -= amount
        self.drawable.fetch_latest_data() #update GUI

    def setOwner(self, newOwner):
        if self.player is not None and self in self.player.countries:
            self.player.removeCountry(self)
        self.player = newOwner
        self.player.addCountry(self)
        if self.drawable is not None:
            self.drawable.fetch_latest_data() #update GUI

    def getName(self):
        return self.name

    def addNeighbour(self, neighbour):
        self.neighbours.append(neighbour)
