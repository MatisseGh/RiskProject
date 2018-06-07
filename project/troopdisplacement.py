

class TroopDisplacement:
    """a class to move troops from a country, to another and specifies the exact amount
    this class reduces arguments in methods and provides clean code"""

    def __init__(self, fromCountry, toCountry, amount):
        self.fromCountry = fromCountry
        self.toCountry = toCountry
        self.amount = amount

    def __repr__(self):
        return str(self.fromCountry) + ", " + str(self.toCountry) + ": " + str(self.amount)
