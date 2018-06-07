import pygame
from GUI.button import Button
import GUI.screenManager
import sys


class FrontPage:
    """This is the first startup screen"""

    def __init__(self, screen):
        self.screen = screen
        self.size = self.width, self.height = screen.get_size()
        self.showing = False
        self.update_rects = []
        self.buttons = []
        self.create_screen_attributes()

    def show(self):
        """lets this screen know it's currently showing. needs to be called when loading the screen"""
        self.showing = True
        self.update_rects.append(self.screen.get_rect())
        self.update_screen()

    def hide(self):
        """lets this screen know it's no longer showing."""
        self.showing = False

    def update_screen(self):
        """updates the backround-images and all elements on this screen"""
        self.screen.blit(self.background, (0, 0))
        self.update_buttons()
        pygame.display.update(self.update_rects)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.update_rects.clear()

    def create_screen_attributes(self):
        """initializes all elements for this screen"""
        self.background = pygame.transform.scale(pygame.image.load('data/backgrounds/frontPage.jpg').convert(), self.size)
        self.button_widht = int(self.width / 4)
        self.button_height = int(self.width / 14)
        self.start_button = Button(self, pygame.Rect(self.width - self.button_widht * 5 / 2,
                                                     self.height - self.button_height * 7 / 2, self.button_widht,
                                                     self.button_height), "Start", 35, self.start)
        self.start_button.user_data = "start"
        self.buttons.append(self.start_button)
        self.info_button = Button(self, pygame.Rect(self.width - self.button_widht * 5 / 2,
                                                    self.height - self.button_height * 2, self.button_widht,
                                                    self.button_height), "Information", 35, self.info)
        self.info_button.user_data = "Info"
        self.buttons.append(self.info_button)

    def info(self):
        """switches the displaying screen to INFOSCREEN"""
        GUI.screenManager.instance.setScreen(GUI.screenManager.instance.INFOSCREEN)

    def start(self):
        """switches the displaying screen to SETUP"""
        GUI.screenManager.instance.setScreen(GUI.screenManager.instance.SETUP)

    def update_buttons(self):
        """updates and draws all buttons, needs to be called in game loop"""
        for btn in self.buttons:
            btn.update()
