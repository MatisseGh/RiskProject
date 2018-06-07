import pygame
import sys


class StatusBar:
    """displays a history with recent events. Add events with set_text()."""
    def __init__(self, screen, rect):
        self.screen = screen
        self.rect = rect
        self.prev_rect = self.rect
        self.text_changed = False
        self.images = []
        self.load_background()
        self.background = self.img_down
        self.prev_background = self.background
        self.buttonClick = pygame.mixer.Sound('data/music/button_click.ogg')
        self.text = ""
        self.transitioning = False
        self.shown = False
        self.is_down = False
        self.draw()
        self.counter = 0
        self.sentences = []

    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        left = self.rect.left
        right = self.rect.right
        top = self.rect.top
        bottom = self.rect.bottom
        self.prev_background = self.background
        if left <= mouse[0] <= right and top <= mouse[1] <= bottom:
            if self.shown and self.background is not self.img_up_h:
                self.background = self.img_up_h
            elif not self.shown and self.background is not self.img_down_h:
                self.background = self.img_down_h
            if click[0] == 1 and self.is_down is False:
                self.buttonClick.play(0)
                self.is_down = True
            if click[0] == 0 and self.is_down is True:
                # wouter: mouse is pressed, do action
                self.is_down = False
                if self.shown:
                    self.hide()
                else:
                    self.show()
        else:
            if self.shown and self.background is not self.img_up:
                self.background = self.img_up
            elif not self.shown and self.background is not self.img_down:
                self.background = self.img_down
        self.draw()

    def draw(self):
        pygame.display.get_surface().blit(self.background, self.rect)
        if self.transitioning:
            self.screen.update_rects.append(self.rect)
            self.prev_rect.height += 20
            self.screen.update_rects.append(self.prev_rect)
            self.prev_rect = self.rect.copy()
        elif self.text_changed or self.prev_background is not self.background:
            self.prev_background = self.background
            self.text_changed = False
            self.screen.update_rects.append(self.rect)

    #added some more code for handling sentences longer than 1 one line
    def set_text(self, text):
        self.text_changed = True
        words = text.split()
        if len(words) < 5:
            twoLines = False
            sentence = ""
            for x in range(len(words)):
                sentence += " " + words[x]
            self.printText("--------------------------------------------")
            self.printText(sentence)
        else:
            twoLines = True
            counter = len(words)
            sentence = ""
            for x in range(4):
                sentence += " " + words[x]
            self.printText("--------------------------------------------")
            self.printText(sentence)

            sentence = ""
            for x in range(counter - 4):
                sentence += " " + words[x + 4]
            self.printText(sentence)

        self.load_background()
        myfont1 = pygame.font.Font('data/fonts/AUGUSTUS.TTF', 11)
        myfont2 = pygame.font.Font('data/fonts/AUGUSTUS.TTF', 12)
        myfont2.set_bold(True)
        if twoLines is True:
            amount = 2
        else:
            amount = 1
        for x in range(self.counter):
            if x == self.counter - amount or x == self.counter - 1:
                textsurface = myfont2.render(self.sentences[x], True, (204, 190, 30))
                for image in self.images:
                    image.blit(textsurface, (self.rect.width // 2 - textsurface.get_width() // 2, 30 + (20 * x)))
            else:
                textsurface = myfont1.render(self.sentences[x], True, (255, 255, 255))
                for image in self.images:
                    image.blit(textsurface, (self.rect.width // 2 - textsurface.get_width() // 2, 30 + (20 * x)))

    def load_background(self):
        self.img_up = pygame.transform.scale(pygame.image.load('data/backgrounds/status_bar_up.png'), self.rect.size).convert_alpha()
        self.img_up_h = pygame.transform.scale(pygame.image.load('data/backgrounds/status_bar_up_hover.png'), self.rect.size).convert_alpha()
        self.img_down = pygame.transform.scale(pygame.image.load('data/backgrounds/status_bar_down.png'), self.rect.size).convert_alpha()
        self.img_down_h = pygame.transform.scale(pygame.image.load('data/backgrounds/status_bar_down_hover.png'), self.rect.size).convert_alpha()
        self.images = (self.img_up, self.img_up_h, self.img_down, self.img_down_h)

    def printText(self, sentence):
        if self.counter < 22:
            self.sentences.append(sentence)
            self.counter += 1
        else:
            del self.sentences[0]
            self.sentences.append(sentence)

    def hide(self):
        self.background = self.img_up
        self.transitioning = True
        while self.rect.bottom > 70:
            self.rect.move_ip(0, -15)
            self.screen.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        self.shown = False
        self.transitioning = False

    def show(self):
        self.background = self.img_down
        self.transitioning = True
        while self.rect.top < 0:
            self.rect.move_ip(0, 15)
            self.screen.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        self.shown = True
        self.transitioning = False
