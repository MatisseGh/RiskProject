import csv
import pygame
import sys

import random
import worldstats
from continent import Continent
from country import Country
import GUI.screenManager
from GUI.colors import Color
from bot import Bot
from humanplayer import HumanPlayer
from dice import Dice
from gamestates import Gamestate

#initialize pygame


def main(): #the main loop: set up the countries, worldstats, the players, the GUI...

    initializeCountries("data/gameboard.csv") #read countries with neighbours and continent from csv
    screen_manager = GUI.screenManager.instance
    screen_manager.initialize() #initialize GUI
    gamestate = Gamestate.INITIALIZATION #first gamestate
    screen_manager.setScreen(screen_manager.FRONTPAGE)
    while gamestate == Gamestate.INITIALIZATION:
        screen_manager.update_screen()
        if screen_manager.current_screen == screen_manager.gameboard:
            gamestate = Gamestate.DISTRIBUTE_COUNTRIES

    distributeCountries() #random distribution of countries for all players
    worldstats.instance.updateCountryGroups()

    gamestate = Gamestate.DISTRIBUTE_TROOPS
    screen_manager.setScreen(screen_manager.GAMEBOARD)
    gameboard = screen_manager.current_screen
    gameboard.statusBarChangeText("ready to add troops")
    for player in worldstats.instance.players: #different implementation for bots and human players
        player.troopsToPlace = 35
        if isinstance(player, Bot):
            distribution = player.algo.bestDistributeTroops()
        else:
            distribution = gameboard.addTroopsInput(player)

        print("distribution:", distribution) #print to command line for logging and debugging
        counter = 0
        for country in distribution:
            counter += distribution[country]
            country.addTroops(distribution[country]) #add troops to countries
            player.troopsToPlace -= distribution[country]

        print(player, "added", counter, "troops")
        print(player, "has", player.troopsToPlace, "troops to place")
        screen_manager.update_screen(True)

    gamestate = Gamestate.PLAYING #the game starts
    rounds = 0
    while not checkForWorldDomination() and gamestate is Gamestate.PLAYING: #keep playing until world domination
        rounds += 1
        for player in worldstats.instance.players:
            worldstats.instance.player = player
            if len(player.countries) != 0:
                    player.troopsToPlace = player.roundBonus()
                    if isinstance(player, HumanPlayer):
                        player.addTroops2()
                    if isinstance(player, Bot):
                        player.addTroops(player.troopsToPlace)
                    player.attack()
                    player.moveTroops()
            else:
                GUI.screenManager.instance.gameboard.playerEliminated(player, rounds)
                worldstats.instance.players.remove(player)
        screen_manager.update_screen(True)

    gamestate = Gamestate.FINISHED #game is finished
    while gamestate:
        screen_manager.update_screen(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def initializeCountries(filename):  #reads in csv file with countries, creates them and continents. Adds them to worldstats
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        countriesOfContinent = list()
        #print("loading counties\n======================================================================")
        for row in readCSV:
            if row[0] == "#":  #first time this gets skipped because it lists the countries first
                continentName = row[1]
                continentBonus = int(row[2])
                continent = Continent(continentName, continentBonus, countriesOfContinent)
                worldstats.instance.addContinent(continent)  #adding them to worldstats so it's available to every class with an instance
                countriesOfContinent = []
            else:
                countryName = row[0]
                #print("reading " + countryName)
                xCoordinaat = int(row[1])
                yCoordinaat = int(row[2])
                country = Country(countryName, xCoordinaat, yCoordinaat)
                countriesOfContinent.append(country)
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        for row in readCSV: #iterate csv again for adding references to neighbours (countries had to be created first)
            if row[0] != "#":
                country = worldstats.instance.getCountryByName(row[0])
                #print("country:", country)
                i = 3
                while i != 9:
                    if row[i] != "":
                        neighbour = worldstats.instance.getCountryByName(row[i]) #string to country object reference
                        country.addNeighbour(neighbour)
                    i += 1


def distributeCountries(): #distribute the countries random between all the players
    countries = worldstats.instance.getCountries()
    countriesPerPlayer = len(countries) // worldstats.instance.getNumberOfPlayers()
    for player in worldstats.instance.players:
        for i in range(0, countriesPerPlayer):
            country = countries[random.randint(0, len(countries) - 1)]
            countries.remove(country)
            player.addCountry(country)
    #when not all the countries can be distributed equally, give the last few countries to random players:
    while len(countries) > 0:
        players = worldstats.instance.players.copy()
        player = players[random.randint(0, len(players) - 1)]
        country = countries[random.randint(0, len(countries) - 1)]
        countries.remove(country)
        players.remove(player)
        player.addCountry(country)


def initializeOrder():
    diceThow = dict()
    finalOrder = []
    for player in worldstats.instance.players:
            dice = Dice()
            throw = dice.rolTurn()

            diceThow[player] = throw
    while len(diceThow) != 0:
        maxRoll = 0
        maxPlayer = None
        for player in diceThow.keys():
            if diceThow[player] > maxRoll:
                maxRoll = diceThow[player]
                maxPlayer = player
        maxPlayer.color = Color(len(finalOrder))
        finalOrder.append(maxPlayer)
        del diceThow[maxPlayer]
    worldstats.instance.players = finalOrder
    print(finalOrder)
    print(worldstats.instance.players)


def checkForWorldDomination():
    for player in worldstats.instance.players:
        if len(player.countries) == 42:
            print(player, "WON!")
            GUI.screenManager.instance.gameboard.victorySound.play(0)
            GUI.screenManager.instance.gameboard.worldDominancePopUp(player)
            return True
    return False


if __name__ == "__main__":
    main()
