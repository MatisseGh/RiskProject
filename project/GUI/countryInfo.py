import pygame


class CountryInfo:
    """holds a reference to a drawable country to display information, follows mouse.
       Only one should be visable at any given moment"""

    def __init__(self, screen, rect, drawableCountry):
        self.screen = screen
        self.rect = rect
        self.drawableCountry = drawableCountry
        self.color = drawableCountry.color
        self.text = ""
        self.load_images(self.color)
        self.set_text(self.fetch_info())
        self.visible = False
        self.prev_rect = self.rect

    def update(self):
        """gets latest information from the drawable country and updtates the position to the mouse locationself.
           Calls draw()"""
        if self.visible:
            self.set_text(self.fetch_info())
            mouse = pygame.mouse.get_pos()
            self.rect.topleft = (mouse[0] + 10, mouse[1] + 10)
            self.draw()

    def draw(self):
        """Draws the countryInfo to the screen and adds it's rect to the render update list."""
        pygame.display.get_surface().blit(self.background, self.rect)
        self.screen.update_rects.append(self.rect)
        self.screen.update_rects.append(self.prev_rect)
        self.prev_rect = self.rect.copy()

    def hide(self):
        """disables draw and adds it's rect to the render update list."""
        if self.visible:
            self.visible = False
            self.screen.update_rects.append(self.rect)

    def show(self):
        """enables draw"""
        if not self.visible:
            self.visible = True

    def set_text(self, text):
        """calls load_images() and blit's the given text to the images"""
        if self.text != text:
            self.text = text
            self.load_images(self.color)
            font_size = 18
            myfont = pygame.font.Font('data/fonts/AUGUSTUS.TTF', font_size)
            horizontal_spacing = 5
            for i, s in enumerate(text):
                line_surface = myfont.render(s, True, (255, 255, 255))
                self.background.blit(line_surface, pygame.Rect((25, 35 + i * (font_size + horizontal_spacing)), line_surface.get_rect().size))

    def load_images(self, color):
        """loads the background of the correct color (should be the country 's color')"""
        self.color = color
        color = color.name
        self.background = pygame.transform.scale(pygame.image.load('data/backgrounds/roman_banner_flag_' + self.color.name + '.png'), self.rect.size).convert_alpha()

    def fetch_info(self):
        """gets the info from the drawable country as a formatted string (a tuple with each element a line of the string)."""
        return (self.drawableCountry.country.name,
                "---------------------------------------------",
                "Troops: " + str(self.drawableCountry.amount_of_troops),
                "Player: " + str(self.drawableCountry.player))
