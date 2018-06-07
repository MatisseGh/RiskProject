import pygame
from GUI.events import Events
from GUI.countryInfo import CountryInfo


class DrawableCountry:

    def __init__(self, screen, rect, country, color):
        """DrawableCountry(screen, rect, country, color=(255, 0, 0)). The Rect gives the position (relative to the topleft of the screen)
        and the size of the country. the Update function must be called every game-loop to check if the player is interacting with this country.
        The amount of troops wil be displayed on the country and the color of the country indicates the ownership"""
        self.screen = screen
        self.country = country
        self.rect = rect
        self.amount_of_troops = country.amountOfTroops
        self.player = country.player
        self.color = color
        self.load_images(color)
        self.info_panel = CountryInfo(self.screen, pygame.Rect((0, 0), (310, 140)), self)
        self.size = 100
        self.mouse_down = False
        self.selected = False
        self.selectable = False
        self.highlighted = False
        self.prev_image = None
        self.prev_amount = 0

    def set_color(self, color):
        """sets the color and loads the corresponding images"""
        if self.color != color:
            self.color = color
            self.load_images(color)
            self.info_panel.load_images(color)

    def load_images(self, color):
        """loads the images of the given color"""
        color = color.name
        path = 'data/pins/Roman Pin ' + color
        self.img = pygame.transform.scale(pygame.image.load(path + '.png'), self.rect.size).convert_alpha()
        self.img_hover = pygame.transform.scale(pygame.image.load(path + ' hover.png'), self.rect.size).convert_alpha()
        self.img_selected = pygame.transform.scale(pygame.image.load(path + ' selected.png'), self.rect.size).convert_alpha()
        self.img_disabled = pygame.transform.scale(pygame.image.load(path + ' disabled.png'), self.rect.size).convert_alpha()
        self.img_disabled_hover = pygame.transform.scale(pygame.image.load(path + ' disabled hover.png'), self.rect.size).convert_alpha()
        self.img_highlighted = pygame.transform.scale(pygame.image.load(path + ' highlight.png'), self.rect.size).convert_alpha()

    def update(self):
        """This will check if the mouse is hovering over the country or if the country is clicked.
        This also calls the draw function to display the correct state"""
        if self.country.player is not None and self.color != self.country.player.color:
            self.set_color(self.country.player.color)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        left = self.rect.left
        right = self.rect.right
        top = self.rect.top
        bottom = self.rect.bottom

        if left <= mouse[0] <= right and top <= mouse[1] <= bottom and self.selectable:
            if click[0] == 1 and not self.mouse_down:
                self.mouse_down = True          # wouter: the button will trigger only when the mouse is released while over the button
            if self.mouse_down is True:
                self.draw(self.img_selected)
            else:
                self.draw(self.img_hover)
            #  wouter: when the mouse is released, do the click action:
            if click[0] == 0 and self.mouse_down:
                self.mouse_down = False
                print("clicked", self.country.name)
                event = pygame.event.Event(Events.COUNTRY_CLICK, country=self)
                pygame.event.post(event)
        else:
            if not self.selectable:
                self.draw(self.img_disabled)
            elif self.selected:
                self.draw(self.img_selected)
            elif self.selectable:
                if self.highlighted:
                    self.draw(self.img_highlighted)
                else:
                    self.draw(self.img)
        if click[0] == 0 and self.mouse_down:
            self.mouse_down = False
        if left <= mouse[0] <= right and top <= mouse[1] <= bottom:
            self.screen.country_info = self.info_panel
            self.info_panel.show()
        else:
            self.info_panel.hide()
        if self.screen.EDETING and self.mouse_down:
            self.rect.center = mouse

    def draw(self, image):
        """draws the country with the given image and adds it's rect to the render update list."""
        pygame.display.get_surface().blit(image, self.rect)
        # wouter: draw the amount of troops in the center of the country:
        if self.amount_of_troops < 100:
            myfont = pygame.font.Font('data/fonts/AUGUSTUS.TTF', 20)
        else:
            myfont = pygame.font.Font('data/fonts/AUGUSTUS.TTF', 15)
        textsurface = myfont.render(str(self.amount_of_troops), True, (255, 255, 255))
        t_pos_x = self.rect.centerx - textsurface.get_width() // 2 - 2
        t_pos_y = self.rect.top + 12
        pygame.display.get_surface().blit(textsurface, (t_pos_x, t_pos_y))
        if self.prev_image is not image or self.prev_amount != self.amount_of_troops:
            self.prev_image = image
            self.prev_amount = self.amount_of_troops
            self.screen.update_rects.append(self.rect)

    def fetch_latest_data(self):
        """updates the info of the drawable country with the actual country"""
        self.amount_of_troops = self.country.amountOfTroops
        self.player = self.country.player

    def __repr__(self):
        return self.country.name
