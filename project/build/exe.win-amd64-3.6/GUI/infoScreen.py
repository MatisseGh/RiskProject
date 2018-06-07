import pygame
from GUI.button import Button
import GUI.screenManager
import sys


class InfoScreen:
    """this screen displays information for how to play the game, returns to previous screen when back is clicked."""
    def __init__(self, screen, nummer):
        self.screen = screen
        self.size = self.width, self.height = screen.get_size()
        self.showing = False
        self.update_rects = []
        self.buttons = []
        self.create_screen_attributes()
        self.nummer = nummer
        self.screennumber = 0
        self.previous_screennumber = self.screennumber

    def show(self):
        """lets this screen know it's currently showing. needs to be called when loading the screen"""
        self.showing = True
        self.screen.blit(self.background, (0, 0))
        self.draw_text()
        self.update_rects.append(self.screen.get_rect())
        self.update_screen()

    def hide(self):
        """lets this screen know it's no longer showing."""
        self.showing = False

    def update_screen(self):
        """Updates all elements on the screen."""
        if self.previous_screennumber != self.screennumber:
            self.previous_screennumber = self.screennumber
            self.screen.blit(self.background, (0, 0))
            self.draw_text()
        self.update_buttons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update(self.update_rects)
        self.update_rects.clear()

    def create_screen_attributes(self):
        """creates all elements to display"""
        self.screennumber = 0
        self.background = pygame.transform.scale(pygame.image.load('data/backgrounds/setup_background.png').convert(), self.size)
        self.draw_text()
        self.button_widht = int(self.width / 10)
        self.button_height = int(self.height / 14)
        self.Back_button = Button(self, pygame.Rect((self.width - self.button_widht) / 2,
                                  self.height - self.button_height * 3 / 2, self.button_widht,
                                  self.button_height), "Back", 35, self.back)
        self.Back_button.user_data = "Back"
        self.buttons.append(self.Back_button)
        self.Next_button = Button(self, pygame.Rect((self.width - self.button_widht) / 2 + self.button_widht * 3 / 2,
                                                    self.height - self.button_height * 3 / 2, self.button_widht,
                                                    self.button_height), "Next", 35, self.next)
        self.Next_button.user_data = "Next"
        self.Next_button.enabled = True
        self.buttons.append(self.Next_button)
        self.Previous_button = Button(self, pygame.Rect((self.width - self.button_widht) / 2 - self.button_widht * 3 / 2,
                                                        self.height - self.button_height * 3 / 2, self.button_widht,
                                                        self.button_height), "Previous", 23, self.previous)
        self.Previous_button.user_data = "Previous"
        self.Previous_button.enabled = False
        self.buttons.append(self.Previous_button)

    def next(self):
        self.Next_button.enabled = False
        self.Previous_button.enabled = True
        self.screennumber += 1

    def previous(self):
        self.Previous_button.enabled = False
        self.Next_button.enabled = True
        self.screennumber -= 1

    def back(self):
            GUI.screenManager.instance.setScreen(GUI.screenManager.instance.previous_screen_id)

    def draw_text(self):
        """draws the text from "data/information.txt" to the screen"""
        myfont = pygame.font.Font('data/fonts/AUGUSTUS.TTF', 15)
        teller = 0
        counting = 0
        with open("data/information.txt") as f:
            if(self.screennumber == 0):
                for line in f:
                    if(counting < 31):
                        textsurface = myfont.render(str(line), True, (255, 255, 255))
                        text_pos = ((self.width - textsurface.get_width()) / 2, 50 + 35 * teller)
                        self.screen.blit(textsurface, text_pos)
                        self.update_rects.append(self.screen.get_rect())
                        teller += 1
                        counting += 1
                    counting += 1
            elif(self.screennumber == 1):
                for line in f:
                    if(counting > 31):
                        textsurface = myfont.render(str(line), True, (255, 255, 255))
                        text_pos = ((self.width - textsurface.get_width()) / 2, 50 + 35 * teller)
                        self.screen.blit(textsurface, text_pos)
                        self.update_rects.append(self.screen.get_rect())
                        teller += 1
                        counting += 1
                    counting += 1

    def update_buttons(self):
        """updates all buttons. Needs to be called every game-loop."""
        for btn in self.buttons:
            btn.update()
