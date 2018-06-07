import pygame
import sys


class InfoBar:
    """displays information at the top of the screen, can be hidden. Needs to be updated every game-loop"""

    def __init__(self, screen, rect):
        self.screen = screen
        self.rect = rect
        self.prev_rect = self.rect
        self.shown = False
        self.transitioning = False
        self.load_background()
        self.text = ""

    def update(self):
        """calls draw()"""
        self.draw()

    def draw(self):
        """draws the InfoBar to the screen and adds it's rect to the render update list."""
        pygame.display.get_surface().blit(self.background, self.rect)
        if self.transitioning:
            self.screen.update_rects.append(self.rect)
            self.screen.update_rects.append(self.prev_rect)
            self.prev_rect = self.rect.copy()
        elif self.background is not self.prev_background:
            self.prev_background = self.background
            self.screen.update_rects.append(self.rect)

    def load_background(self):
        """loads the background image"""
        background_image = pygame.image.load('data/backgrounds/roman_info_panel_background.png').convert_alpha()
        self.background = pygame.transform.scale(background_image, self.rect.size)
        self.prev_background = None

    def set_text(self, text):
        """updates the text and blits it to the background"""
        if self.text != text:
            self.text = text
            self.load_background()
            myfont = pygame.font.Font('data/fonts/AUGUSTUS.TTF', 30)
            textsurface = myfont.render(self.text, True, (255, 255, 255))
            self.background.blit(textsurface, (self.rect.width // 2 - textsurface.get_width() // 2, 6))

    def hide(self):
        """starts the hide animation (takes over loop)"""
        self.transitioning = True
        while self.rect.bottom > 0:
            self.rect.move_ip(0, -6)
            self.screen.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        self.shown = False
        self.transitioning = False

    def show(self):
        """starts the show animation (takes over loop)"""
        self.transitioning = True
        while self.rect.top < 0:
            self.rect.move_ip(0, 6)
            self.screen.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        self.shown = True
        self.transitioning = False
