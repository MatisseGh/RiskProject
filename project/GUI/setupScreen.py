import pygame
import sys
import worldstats
import gamemanager
from humanplayer import HumanPlayer
from bot import Bot
import GUI.screenManager
from GUI.textField import TextField
from GUI.popup import Popup
from GUI.button import Button
from GUI.colors import Color


class SetupScreen:
    """screen in witch the player can choose how many players an bots will be playing.
    Allows the player to enter a name for every (non bot) player."""

    def __init__(self, screen):
        self.screen = screen
        self.size = self.width, self.height = screen.get_size()
        self.showing = False
        self.update_rects = []
        self.buttons = []
        self.text_fields = []
        self.amount_of_players = 3
        self.amount_of_bots = 2
        self.create_screen_attributes()

    def show(self):
        """lets this screen know it's currently showing. needs to be called when loading the screen"""
        self.showing = True
        self.update_rects.append(self.screen.get_rect())
        self.update_screen()
        pos = (400, 200)
        left = self.width // 2 - pos[0] // 2
        top = self.height // 2 - pos[1] // 2
        popup_rect = pygame.Rect((left, top), pos)
        popup = Popup(self, popup_rect, Popup.AMOUNT_INPUT_NO_CANCEL, (2, 3, 5))
        popup.title_text = "amount of players"
        self.amount_of_players = popup.show()
        self.amount_of_bots = self.amount_of_players - 1

    def hide(self):
        """lets this screen know it's no longer showing."""
        self.showing = False

    def update_screen(self):
        """Updates all elements on the screen."""
        self.screen.blit(self.background, (0, 0))
        t = 0
        for tf in self.text_fields:
            tf.update()
            if tf.selected:
                t += 1
        if not t:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        for btn in self.buttons:
            btn.update()
        self.draw_text()
        pygame.display.update(self.update_rects)
        if len(self.update_rects) > 18:
            print("WARNING: updating a lot of areas on the screen!")
            print("amount of update rects:", len(self.update_rects))
        self.update_rects.clear()

    def add_text_field(self):
        """adds a textfield below the other textfields and updates the amount of players/bots."""
        n = len(self.text_fields)
        if n < self.amount_of_players:
            self.amount_of_bots -= 1
            width = 300
            height = 75
            spacing = 10
            x_position = self.screen.get_rect().centerx - width // 2
            y_position = 150 + n * (spacing + height)
            self.text_fields.append(TextField(self, pygame.Rect(x_position, y_position, width, height)))
            self.remove_button.enabled = True
            self.move_buttons()
        if n == self.amount_of_players - 1:
            self.add_button.enabled = False

    def remove_text_field(self):
        """removes the bottom textfield and updates the amount of players/bots."""
        if len(self.text_fields) == 1:
            self.remove_button.enabled = False
        if len(self.text_fields):
            self.amount_of_bots += 1
            self.text_fields.pop()
            self.add_button.enabled = True
            self.move_buttons()

    def move_buttons(self):
        """updates the location aff the add/remove player buttons."""
        width = 20
        height = 20
        x_position = self.screen.get_rect().centerx - width // 2
        y_position = 150 + len(self.text_fields) * 85
        self.remove_button.rect.topleft = (x_position, y_position)
        self.add_button.rect.topleft = (x_position, y_position + height)
        if self.showing:
            self.update_rects.append(pygame.Rect(self.screen.get_width() // 2 - 150, 0, 300, self.screen.get_height()))
            self.update_screen()

    def draw_text(self):
        """draws the amount of players/bots to the screen."""
        myfont = pygame.font.Font('data/fonts/AUGUSTUS.TTF', 30)
        text = "(amount of bots: " + str(self.amount_of_bots) + ")"
        textsurface = myfont.render(text, True, (255, 255, 255))
        text = "please enter a name for every player:"
        textsurface2 = myfont.render(text, True, (255, 255, 255))
        text_pos = (self.screen.get_rect().centerx - textsurface.get_width() // 2, self.screen.get_height() - 200)
        text_pos_2 = (self.screen.get_rect().centerx - textsurface2.get_width() // 2, 40)
        self.screen.blit(textsurface, text_pos)
        self.screen.blit(textsurface2, text_pos_2)
        self.update_rects.append(pygame.Rect(text_pos, (textsurface.get_width() + 5, textsurface.get_height())))
        self.update_rects.append(pygame.Rect(text_pos_2, (textsurface2.get_width(), textsurface2.get_height())))

    def next_screen(self):
        """Switches the displaying screen to GAMEBOARD if all textFields are filled in."""
        id = 0
        names = list()
        # create the players:
        for text_field in self.text_fields:
            name = text_field.text
            names.append(name)
            if len(name) == 0:
                pos = (500, 200)
                left = self.width // 2 - pos[0] // 2
                top = self.height // 2 - pos[1] // 2
                text = "please enter a name for every player"
                self.update_screen()
                popup_rect = pygame.Rect((left, top), pos)
                popup = Popup(self, popup_rect, Popup.CONFIRMATION_INPUT_ATTACK, (text, "ok", "cancel"))
                popup.show()
                return
        for name in names:
            worldstats.instance.addPlayer(HumanPlayer(name, id, [], Color(id)))
            id += 1
        for i in range(0, self.amount_of_bots):
            name = "Bot " + str(i + 1)
            worldstats.instance.addPlayer(Bot(name, id, [], Color(id)))
            id += 1
        gamemanager.initializeOrder()
        GUI.screenManager.instance.setScreen(GUI.screenManager.ScreenManager.GAMEBOARD)

    def create_screen_attributes(self):
        """creates all elements to display"""
        self.background = pygame.transform.scale(pygame.image.load('data/backgrounds/setup_background.png').convert(), self.size)
        width = 20
        height = 20
        x_position = self.screen.get_rect().centerx - width // 2
        y_position = 10
        img = pygame.image.load('data/buttons/plus_button.png')
        img_h = pygame.image.load('data/buttons/plus_button_h.png')
        img_d = pygame.image.load('data/buttons/plus_button_d.png')
        self.add_button = Button(self, pygame.Rect(x_position, y_position, width, height), action=self.add_text_field, images=(img, img_h, img_d, img_d))
        img = pygame.image.load('data/buttons/min_button.png')
        img_h = pygame.image.load('data/buttons/min_button_h.png')
        img_d = pygame.image.load('data/buttons/min_button_d.png')
        self.remove_button = Button(self, pygame.Rect(x_position, y_position + height, width, height), action=self.remove_text_field, images=(img, img_h, img_d, img_d))
        width = 300
        height = 100
        x_position = self.screen.get_rect().right - (width + 50)
        y_position = self.screen.get_rect().bottom - (height + 50)
        continue_button = Button(self, pygame.Rect(x_position, y_position, width, height), "continue >", 30, self.next_screen)
        self.buttons.append(self.add_button)
        self.buttons.append(self.remove_button)
        self.buttons.append(continue_button)
        self.add_text_field()
