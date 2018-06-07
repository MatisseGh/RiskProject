import worldstats
from troopdisplacement import TroopDisplacement


class Algorithm:

    def __init__(self, player):
        self.player = player #the currently active player

    def calculateContinentScore(self, continent): #returns a score based on continent attractiveness
        bonus = continent.getBonus()
        ownerShipOfContinent = continent.calculateOwnership().get(self.player)
        if ownerShipOfContinent is None:
            ownerShipOfContinent = 0
        enemies_on_continent = 0
        for country in continent.countries:
            if country.player is not self.player:
                enemies_on_continent += country.amountOfTroops
        connections = continent.getConnections()
        return (bonus * ownerShipOfContinent) / (connections + enemies_on_continent / 10) # added an extra +2 for better results

    def bestDistributeTroops(self): #calculates the best countries to place your troops
        contintentScores = dict()
        for continent in worldstats.instance.continents:
            score = self.calculateContinentScore(continent)
            contintentScores[continent] = score
            if worldstats.instance.numberOfPlayers < 5: #less than 5 players => focus on two continents
                FOCUS = 2
            else:
                FOCUS = 1
        bestContinents = dict() #key = continent, value = attractiveness score
        scores = list(contintentScores.values())
        while 0.0 in scores:
            scores.remove(0.0)
        scores.sort()
        if len(scores) >= FOCUS:
            last = scores[-FOCUS:]
        else:
            last = scores
        for continent in contintentScores:
            if contintentScores[continent] in last and len(bestContinents) <= FOCUS:
                bestContinents[continent] = contintentScores[continent]
        # Now we'll calculate the percentages for each continent and put those in bestContinents:
        norm = 0
        for continent in list(bestContinents):
            if bestContinents[continent] > norm:
                norm = bestContinents[continent]
        som = 0.0
        for continent in list(bestContinents):
            bestContinents[continent] /= norm
            som += bestContinents[continent]
        for continent in list(bestContinents):
            bestContinents[continent] /= som
        # Now we give the best continents the actual amounts of troops they can have:
        troops_to_place = self.player.troopsToPlace
        for continent in list(bestContinents):
            bestContinents[continent] = int(bestContinents[continent] * troops_to_place)
            troops_to_place -= bestContinents[continent]
            lastContinent = continent
        bestContinents[lastContinent] += troops_to_place    #the last continent gets the remaining troops

        # fill a dictionary with countries and their score:
        countryScores = dict()
        for continent in list(bestContinents):
            for country in continent.countries:
                if country.player == self.player:
                    score = 0
                    for neighbour in country.neighbours:
                        if neighbour.player != self.player:
                            score += neighbour.amountOfTroops
                    countryScores[country] = score

        # finds the norm for each of the continents
        norm = dict()
        for continent in list(bestContinents):
            for country in continent.countries:
                if country.player is self.player:
                    if continent not in norm:
                        norm[continent] = countryScores[country]
                    elif countryScores[country] > norm[continent]:
                        norm[continent] = countryScores[country]

        # divides every score by the norm (of the correct continent)
        for continent in bestContinents:
            sum = 0
            for country in list(countryScores):
                if country in continent.countries:
                    countryScores[country] /= norm[continent]
                    sum += countryScores[country]

            # the actual percentage is calculated!
            for country in list(countryScores):
                if country in continent.countries:
                    countryScores[country] /= sum

            distributed = 0
            # the percentage is applied to the available troops for every country
            for country in list(countryScores):
                if country in continent.countries:
                    countryScores[country] *= bestContinents[continent]
                    countryScores[country] = int(countryScores[country])
                    distributed += countryScores[country]                #these things are only to fix the 'rest troops'
                    lastCountry = country

            if distributed != bestContinents[continent]:
                difference = bestContinents[continent] - distributed
                countryScores[lastCountry] += difference

        return countryScores #a dict with countries and their attractiveness scores (not amount of troops!)

    def bestAddingTroops(self): #Returns a dict with countries and how many troops to place
        scores = dict()
        total_score = 0
        for country in self.player.countries:
            enemy_troops = 0 #enemy troops on neighboring countries
            ownership = 0 #ownership percentage of continent
            my_troops = country.amountOfTroops #amount of troops on the player's countries
            for neighbour in country.neighbours: #fill up the variables
                if neighbour.player is not self.player:
                    enemy_troops += neighbour.amountOfTroops
                    enemy_continent = worldstats.instance.getContinentByCountry(neighbour)
                    enemy_ownership = enemy_continent.calculateOwnership().get(neighbour.player)
                    continent = worldstats.instance.getContinentByCountry(country)
                    ownership = continent.calculateOwnership().get(country.player)

            if enemy_troops != 0:
                if ownership > 0.98:
                    score = (my_troops / enemy_troops) + (enemy_ownership)#score if the continent is entirely ours
                else:
                    score = (my_troops / enemy_troops) + (3 * ownership)  #score if the continent is not entirely ours
                if my_troops > enemy_troops:
                    score = 0 #if your country is already strong compared to its neigbours, it won't be effective to keep adding troops
                scores[country] = score
            else:
                scores[country] = 0
        for s in scores.values():
            total_score += s
        if total_score <= 0:
            return
        for country in list(scores.keys()):
            scores[country] /= total_score #every country is given a percentage (how likely to add there)

        best_score = 0
        counter = 0
        troops = dict()
        for country in scores:
            if scores[country] > best_score:
                best_country = country
                best_score = scores[country]
            amount_of_troops = int(scores[country] * self.player.troopsToPlace)
            counter += amount_of_troops
            troops[country] = amount_of_troops
        if counter != self.player.troopsToPlace:
            difference = self.player.troopsToPlace - counter
            troops[best_country] += difference
        return troops #returns a dict with countries and the amount of troops they deserve

    def check_neighbours(self, country): #returns True if there's an enemy surrounding the country
        for neighbour in country.getNeigbours():
            if neighbour.player != self.player:
                return True
        return False

    def bestMoveTroops(self): #Move troops to another country the player owns. Returns a TroopDisplacement
        weakest_countries = dict() #each country with enemyies nearby gets a 'weakness'-score
        for country in self.player.countries:
            if self.check_neighbours:
                amount_of_enemies = 0 #enemy troops surrounding the country
                for neighbour in country.neighbours:
                    if neighbour.player is not self.player:
                        amount_of_enemies += neighbour.amountOfTroops
                weakness = amount_of_enemies / country.amountOfTroops #calculating weakness score
                weakest_countries[weakness] = country

        # finding best country to move from:
        strongest_countries = dict()
        while weakest_countries and not strongest_countries:
            weakness = sorted(weakest_countries.keys())[-1]
            weak_country = weakest_countries[weakness]
            weakest_countries.pop(weakness)     # if there are no countries to move from, check second weakest country
            worldstats.instance.updateCountryGroups()
            countrygroup = worldstats.instance.getCountryGroup(weak_country)
            for country in countrygroup:
                if country.amountOfTroops > 1 and not self.check_neighbours(country):
                    strength = country.amountOfTroops * worldstats.instance.stepsToNearestEnemy(country)
                    strongest_countries[strength] = country
        if strongest_countries:
            strength = sorted(strongest_countries.keys())[-1]
            strongest_country = strongest_countries[strength]
            amount = strongest_country.amountOfTroops - 1
            return TroopDisplacement(strongest_country, weak_country, amount)
        else:
            return None

    def bestAttack(self): #Which country does the player attack? Returns a TroopDisplacement
        scores = list()
        for country in self.player.countries:
            my_Troops = country.amountOfTroops #amount of troops the player owns
            my_continent = worldstats.instance.getContinentByCountry(country)
            my_ownership = my_continent.calculateOwnership().get(country.player) #returns ownership of the player
            for attackable_country in worldstats.instance.getAttackableCountries(country): #which countries are attackable?
                for neighbourCountry in attackable_country.neighbours:
                    if neighbourCountry.player is self and neighbourCountry is not country:
                        my_Troops += neighbourCountry.amountOfTroops
                enemy_troops = attackable_country.amountOfTroops
                continent_of_enemy = worldstats.instance.getContinentByCountry(attackable_country)
                enemy_ownership = continent_of_enemy.calculateOwnership().get(attackable_country.player)
                if continent_of_enemy is my_continent:
                    score = (my_Troops / enemy_troops) + (4 * my_ownership) #calculate the score for each attackable country
                else:
                    score = (my_Troops / enemy_troops) + (4 * my_ownership) + (2 * enemy_ownership)
                scores.append(TroopDisplacement(country, attackable_country, score)) #Params = fromCountry, toCountry, amountOfTroops
        # wouter: bestAttack as described in document:
        while scores:
            highest_score = scores[0]
            for country_couple in scores:
                if country_couple.amount > highest_score.amount:
                    highest_score = country_couple
            scores.remove(highest_score)
            my_country = highest_score.fromCountry
            enemy_country = highest_score.toCountry
            #troops_left = my_country.amountOfTroops - enemy_country.amountOfTroops
            friendly_troops = 0
            amount_of_enemies = 0
            enemy_countries = list()
            for neighbour in my_country.neighbours:
                if neighbour.player is not self.player and neighbour is not enemy_country:
                    if neighbour not in enemy_countries:
                        enemy_countries.append(neighbour)
                        amount_of_enemies += neighbour.amountOfTroops - 1
            for neighbour in enemy_country.neighbours:
                if neighbour.player is self.player:
                    friendly_troops += neighbour.amountOfTroops - 1
                elif neighbour not in enemy_countries:
                        enemy_countries.append(neighbour)
                        amount_of_enemies += neighbour.amountOfTroops - 1
            if ((friendly_troops > amount_of_enemies and enemy_country.amountOfTroops <= 5 or
                    friendly_troops > amount_of_enemies and enemy_country.amountOfTroops)):
                amount_of_enemies = 0
                for neighbour in my_country.neighbours:
                    if neighbour.player is not self.player:
                            amount_of_enemies += neighbour.amountOfTroops - 1
                attack_amount = my_country.amountOfTroops - 1 - amount_of_enemies
                #attack_amount will be negative if there are to many enemies surrounding the country
                #For now exactly as many troops will be left as there are enemies surrounding the county
                if attack_amount > 0:
                    #print("att amm", attack_amount)
                    displacement = TroopDisplacement(my_country, enemy_country, attack_amount)
                    return displacement
        return None
