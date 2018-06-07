import pygame
import sys
from GUI.button import Button
from GUI.events import Events


class Popup:
    AMOUNT_INPUT = 0
    NAME_INPUT = 1
    CONFIRMATION_INPUT = 2
    AMOUNT_INPUT_NO_CANCEL = 3
    CONFIRMATION_INPUT_ATTACK = 4
    CONINENT_BONUS_INFO = 5

    def __init__(self, screen, rect, type, param):
        """the param should be a tuple with the required parameters for the given type of input:
        *AMOUNT_INPUT: (starting_value, minimum, maximum)
        *CONFIRMATION_INPUT: (text, confirm_text, cancel_text)"""
        self.screen = screen
        self.rect = rect
        self.type = type
        self.title_text = "title"
        self.keyboard_input = 0
        self.prev_keyboard_input = 0
        self.param = list(param)
        self.showing = False
        self.buttons = []
        self.load_images()

    def show(self):
        """this will return the input from the user when the popup is closed
        *AMOUNT_INPUT: the input is 'None' when canceled or no input was given
        *CONFIRMATION_INPUT:the input is True when confirmed, False otherwize"""
        #Warning: messy code ahead
        width = self.rect.width
        height = self.rect.height
        left = self.rect.left
        right = self.rect.right
        top = self.rect.top
        self.showing = True
        self.background = pygame.transform.scale(self.background_image, self.rect.size)
        pygame.display.get_surface().blit(self.backdrop, (0, 0))
        pygame.display.get_surface().blit(self.background, self.rect)
        pygame.display.flip()
        if self.type == Popup.AMOUNT_INPUT or self.type == Popup.AMOUNT_INPUT_NO_CANCEL:
            img = pygame.image.load('data/buttons/plus_button.png')
            img_h = pygame.image.load('data/buttons/plus_button_h.png')
            img_d = pygame.image.load('data/buttons/plus_button_d.png')
            self.up_button = Button(self.screen, pygame.Rect(right - 165, top + 30, 40, 40), images=(img, img_h, img_d, img_d))
            self.up_button.user_data = "UP_AMOUNT"
            img = pygame.image.load('data/buttons/min_button.png')
            img_h = pygame.image.load('data/buttons/min_button_h.png')
            img_d = pygame.image.load('data/buttons/min_button_d.png')
            self.down_button = Button(self.screen, pygame.Rect(left + 125, top + 30, 40, 40), images=(img, img_h, img_d, img_d))
            self.down_button.user_data = "DOWN_AMOUNT"
            self.buttons.append(self.up_button)
            self.buttons.append(self.down_button)
            if self.type == Popup.AMOUNT_INPUT_NO_CANCEL:
                ok_button = Button(self.screen, pygame.Rect(self.rect.centerx - 50, top + height - 80, 100, 50), "Ok", 20)
                self.buttons.append(ok_button)
            else:
                cancel_button = Button(self.screen, pygame.Rect(left + width - 130, top + height - 80, 100, 50), "Cancel", 16)
                cancel_button.user_data = "CANCEL"
                ok_button = Button(self.screen, pygame.Rect(left + 30, top + height - 80, 100, 50), "Ok", 16)
                self.buttons.append(cancel_button)
                self.buttons.append(ok_button)
            ok_button.user_data = "CONFIRM"
        elif self.type == Popup.CONINENT_BONUS_INFO:
            confirm_button = Button(self.screen, pygame.Rect(left + 130, top + height - 70, 100, 50), "Ok")
            confirm_button.user_data = "CONFIRM"
            self.buttons.append(confirm_button)
        elif self.type == Popup.CONFIRMATION_INPUT:
            confirm_button = Button(self.screen, pygame.Rect(left + 20, top + height - 70, 100, 50), self.param[1])
            cancel_button = Button(self.screen, pygame.Rect(left + width - 120, top + height - 70, 100, 50), self.param[2])
            confirm_button.user_data = "CONFIRM"
            cancel_button.user_data = "CANCEL"
            self.buttons.append(confirm_button)
            self.buttons.append(cancel_button)
        elif self.type == Popup.CONFIRMATION_INPUT_ATTACK:
            confirm_button = Button(self.screen, pygame.Rect(left + width // 2 - 50, top + height - 80, 100, 50), self.param[1])
            confirm_button.user_data = "CONFIRM"
            self.buttons.append(confirm_button)
        while self.showing:
            self.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == Events.BUTTON_CLICK:
                    if event.user_data == "CANCEL":
                        self.close()
                        return self.result(True)
                    elif event.user_data == "CONFIRM":
                        self.close()
                        return self.result(False)
                    elif event.user_data == "UP_AMOUNT":
                        self.param[0] += 1
                    elif event.user_data == "DOWN_AMOUNT":
                        self.param[0] -= 1
                if event.type == pygame.KEYDOWN:
                    buttons = {pygame.K_0: 0, pygame.K_KP0: 0,
                               pygame.K_1: 1, pygame.K_KP1: 1,
                               pygame.K_2: 2, pygame.K_KP2: 2,
                               pygame.K_3: 3, pygame.K_KP3: 3,
                               pygame.K_4: 4, pygame.K_KP4: 4,
                               pygame.K_5: 5, pygame.K_KP5: 5,
                               pygame.K_6: 6, pygame.K_KP6: 6,
                               pygame.K_7: 7, pygame.K_KP7: 7,
                               pygame.K_8: 8, pygame.K_KP8: 8,
                               pygame.K_9: 9, pygame.K_KP9: 9,
                               }
                    if event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
                        self.param[0] -= 1
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                        self.param[0] += 1
                    if event.key in buttons.keys():
                        self.prev_keyboard_input = self.keyboard_input
                        self.keyboard_input = int(str(self.keyboard_input) + str(buttons[event.key]))
                    if event.key == pygame.K_BACKSPACE:
                        self.prev_keyboard_input = self.keyboard_input
                        self.keyboard_input = self.keyboard_input // 10
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        self.close()
                        return self.result(False)
                    if event.key == pygame.K_ESCAPE:
                        self.close()
                        return self.result(True)

            if self.type == Popup.AMOUNT_INPUT or self.type == Popup.AMOUNT_INPUT_NO_CANCEL:
                if self.prev_keyboard_input != self.keyboard_input:
                    self.prev_keyboard_input = self.keyboard_input
                    self.param[0] = self.keyboard_input
                    if self.keyboard_input > self.param[2]:
                        self.keyboard_input = self.param[2]
                if self.param[0] < self.param[1]:
                    self.param[0] = self.param[1]
                elif self.param[0] > self.param[2]:
                    self.param[0] = self.param[2]

    def result(self, canceled):
        if canceled:
            if self.type == Popup.AMOUNT_INPUT or self.type == Popup.AMOUNT_INPUT_NO_CANCEL:
                return None
            elif self.type == Popup.CONFIRMATION_INPUT:
                return False
        else:
            if self.type == Popup.AMOUNT_INPUT or self.type == Popup.AMOUNT_INPUT_NO_CANCEL:
                return self.param[0]
            elif self.type == Popup.CONFIRMATION_INPUT:
                return True

    def close(self):
        self.showing = False
        self.screen.update_screen()
        pygame.display.update()

    def update(self):
        self.draw()
        pygame.display.update(self.rect)

    def draw(self):
        surface = pygame.display.get_surface()
        surface.blit(self.background, self.rect)
        if self.type == Popup.AMOUNT_INPUT or self.type == Popup.AMOUNT_INPUT_NO_CANCEL:
            myfont = pygame.font.Font('data/fonts/AUGUSTUS.TTF', 36)
            titleFont = pygame.font.Font('data/fonts/AUGUSTUS.TTF', 20)
            textsurface = myfont.render(str(self.param[0]), True, (255, 255, 255))
            titlesurface = titleFont.render(str(self.title_text), True, (255, 255, 255))
            left = self.rect.centerx - textsurface.get_width() // 2
            top = self.rect.centery - self.rect.height // 2 + 40
            rect = pygame.Rect((left - 10, top + titlesurface.get_height() + 5), (textsurface.get_width() + 20, textsurface.get_height()))
            self.up_button.rect.top = rect.top - 2
            self.down_button.rect.top = rect.top - 2
            surface.blit(textsurface, (left, top + titlesurface.get_height() + 5))
            surface.blit(titlesurface, (self.rect.centerx - titlesurface.get_width() // 2, top))
            pygame.display.update(rect)
        elif self.type == Popup.CONFIRMATION_INPUT:
            myfont = pygame.font.Font('data/fonts/AUGUSTUS.TTF', 24)
            textsurface = myfont.render(str(self.param[0]), True, (255, 255, 255))
            left = self.rect.centerx - textsurface.get_width() // 2
            top = self.rect.centery - self.rect.height // 2 + 35
            surface.blit(textsurface, (left, top))
        elif self.type == Popup.CONINENT_BONUS_INFO:
            myfont = pygame.font.Font('data/fonts/AUGUSTUS.TTF', 20)
            textsurface1 = myfont.render("Asia 7", True, (255, 255, 255))
            left = self.rect.centerx - textsurface1.get_width() // 2 - 75
            top = self.rect.centery - self.rect.height // 2 + 80
            surface.blit(textsurface1, (left, top))
            textsurface2 = myfont.render("North America 5", True, (255, 255, 255))
            top += 35
            surface.blit(textsurface2, (left, top))
            textsurface3 = myfont.render("Europe 5", True, (255, 255, 255))
            top += 35
            surface.blit(textsurface3, (left, top))
            textsurface4 = myfont.render("Africa 3", True, (255, 255, 255))
            top += 35
            surface.blit(textsurface4, (left, top))
            textsurface5 = myfont.render("Australia 2", True, (255, 255, 255))
            top += 35
            surface.blit(textsurface5, (left, top))
            textsurface6 = myfont.render("South America 2", True, (255, 255, 255))
            top += 35
            surface.blit(textsurface6, (left, top))
        elif self.type == Popup.CONFIRMATION_INPUT_ATTACK:
            myfont = pygame.font.Font('data/fonts/AUGUSTUS.TTF', 16)
            words = self.param[0].split()
            sentence1 = ""
            sentence2 = ""
            for x in range(len(words)):
                if x < 7:
                    sentence1 += " " + words[x]
                else:
                    sentence2 += " " + words[x]
            textsurface1 = myfont.render(str(sentence1), True, (255, 255, 255))
            textsurface2 = myfont.render(str(sentence2), True, (255, 255, 255))
            left = self.rect.centerx - textsurface1.get_width() // 2
            top = self.rect.centery - self.rect.height // 2 + 35
            surface.blit(textsurface1, (left, top + 20))
            surface.blit(textsurface2, (left, top + 42))
        for button in self.buttons:
            button.update()

    def load_images(self):
        self.background_image = pygame.image.load('data/backgrounds/roman_banner_flag.png').convert_alpha()
        self.backdrop = pygame.transform.scale(pygame.image.load('data/backgrounds/grayed_out.png'), pygame.display.get_surface().get_size())
        self.backdrop.convert_alpha()
