import pygame
import ctypes
import os
import sys
from GUI.gameboard import Gameboard
from GUI.setupScreen import SetupScreen
from GUI.frontPage import FrontPage
from GUI.infoScreen import InfoScreen


class ScreenManager:
    """keeps track of witch screen is being displayed and updates the correct one. Handles switching between screen.
    One instance of gameboard is created when loaded (access via 'GUI.gameboard.instance')."""
    SETUP = 0
    GAMEBOARD = 1
    FRONTPAGE = 2
    INFOSCREEN = 3

    def __init__(self):
        # setup screen window (user32 is used to get phisical screen dimensions)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.mixer.pre_init(44100, -16, 2, 2048)  # befor pygame.init() for less delay
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        user32 = ctypes.windll.user32
        self.screensize = screenWidth, screenHeight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.size = self.width, self.height = self.screensize
        self.previous_screen_id = None
        self.current_screen_id = None

    def initialize(self):
        """Initialize the window"""
        flags = pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode(self.size, flags)
        self.fullscreen = False
        riskIcon = pygame.image.load('data/icons/Risk-icon2.ico')
        pygame.display.set_icon(riskIcon)
        pygame.display.set_caption('Risk')
        self.current_screen = None
        self.setupScreen = SetupScreen(self.screen)
        self.gameboard = Gameboard(self.screen)
        self.frontpage = FrontPage(self.screen)
        self.infoscreen = InfoScreen(self.screen, 0)

    def setScreen(self, screen):
        """Sets the given screen to be displayed."""
        self.previous_screen_id = self.current_screen_id
        self.current_screen_id = screen
        if screen == ScreenManager.SETUP:
            self.current_screen = self.setupScreen
            self.gameboard.hide()
            self.frontpage.hide()
            self.infoscreen.hide()
        elif screen == ScreenManager.GAMEBOARD:
            self.current_screen = self.gameboard
            self.setupScreen.hide()
            self.frontpage.hide()
            self.infoscreen.hide()
        elif screen == ScreenManager.FRONTPAGE:
            self.current_screen = self.frontpage
            self.setupScreen.hide()
            self.gameboard.hide()
            self.infoscreen.hide()
        elif screen == ScreenManager.INFOSCREEN:
            self.current_screen = self.infoscreen
            self.setupScreen.hide()
            self.gameboard.hide()
            self.frontpage.hide()
        self.current_screen.show()

    def update_screen(self, fetch_latest_data=False):
        """Updates the displaying screen. fetch_latest_data can be set for gameboard"""
        pygame.event.pump()
        for event in pygame.event.get(pygame.QUIT):
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if self.current_screen is self.setupScreen:
            self.setupScreen.update_screen()
        elif self.current_screen is self.gameboard:
            self.gameboard.update_screen(fetch_latest_data)
        elif self.current_screen is self.frontpage:
            self.frontpage.update_screen()
        elif self.current_screen is self.infoscreen:
            self.infoscreen.update_screen()


instance = ScreenManager()
