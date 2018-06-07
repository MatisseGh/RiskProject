from enum import Enum, unique


@unique
class Gamestate(Enum): #in which state is the game
    INITIALIZATION = 0
    DISTRIBUTE_COUNTRIES = 1
    DISTRIBUTE_TROOPS = 2
    PLAYING = 3
    FINISHED = 4
