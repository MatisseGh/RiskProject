import pygame
from GUI.events import Events

#Wouter


class Button:

    def __init__(self, screen, rect, text="", font_size=20, action=None, images=None):
        """The button needs a rect (to set position and size), a label and (optionally) an action.
        (the action is a function to be called when the button is pressed). Finaly a tuple of 4 images can be passed: normal, hover, down & disabled.
        when a button is clicked, it also creates an event of type Events.BUTTON_CLICK with the user_data as an argument"""
        self.screen = screen
        self.rect = rect
        self.font_size = font_size
        self.txt_color = (255, 255, 255)
        self.images = images
        #self.load_images(images)
        self.text = ""
        self.set_text(text)
        self.action = action
        self.is_down = False
        self.user_data = None
        self.enabled = True
        self.prev_image = None
        self.buttonClick = pygame.mixer.Sound('data/music/button_click.ogg')

    def update(self):
        """checks if the button is clicked, hovered, etc. .Also calls the draw function (with the correct image)"""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        left = self.rect.left
        right = self.rect.right
        top = self.rect.top
        bottom = self.rect.bottom

        if self.enabled:
            if left <= mouse[0] <= right and top <= mouse[1] <= bottom:
                if click[0] == 1 and self.is_down is False:
                    self.buttonClick.play(0)
                    self.is_down = True          # wouter: the button will trigger only when the mouse is released while over the button
                if self.is_down is True:
                    self.draw(self.img_down)
                else:
                    self.draw(self.img_hover)

                if click[0] == 0 and self.is_down is True:
                    # wouter: mouse is pressed, do action
                    self.is_down = False
                    if self.action is not None:
                        self.action()
                    event = pygame.event.Event(Events.BUTTON_CLICK, user_data=self.user_data)
                    pygame.event.post(event)
            else:
                self.draw(self.img)
                if click[0] == 0 and self.is_down is True:
                    self.is_down = False         # wouter: if the mouse is released but not over the button, do nothing
        else:
            self.draw(self.img_disabled)

    def draw(self, image):
        """draws the button to the screen with a given image and adds it's rect to the render update list."""
        pygame.display.get_surface().blit(image, self.rect)
        if self.prev_image is not image:
            self.prev_image = image
            self.screen.update_rects.append(self.rect)

    def load_images(self, images=None):
        """loads all images (default-images if none are given)"""
        if images is not None:
            self.img = pygame.transform.scale(images[0], self.rect.size).convert_alpha()
            self.img_hover = pygame.transform.scale(images[1], self.rect.size).convert_alpha()
            self.img_down = pygame.transform.scale(images[2], self.rect.size).convert_alpha()
            self.img_disabled = pygame.transform.scale(images[3], self.rect.size).convert_alpha()
        else:
            path = 'data/buttons/roman_button_large'
            self.img = pygame.transform.scale(pygame.image.load(path + '.png'), self.rect.size).convert_alpha()
            self.img_hover = pygame.transform.scale(pygame.image.load(path + '_h.png'), self.rect.size).convert_alpha()
            self.img_down = pygame.transform.scale(pygame.image.load(path + '_d.png'), self.rect.size).convert_alpha()
            self.img_disabled = pygame.transform.scale(pygame.image.load(path + '_disabled.png'), self.rect.size).convert_alpha()

    def set_text(self, text):
        """calls load_images() and blits given text on the images."""
        self.text = text
        self.load_images(self.images)
        myfont = pygame.font.Font('data/fonts/AUGUSTUS.TTF', self.font_size)
        textsurface = myfont.render(text, True, self.txt_color)
        self.img.blit(textsurface, (self.rect.width // 2 - textsurface.get_width() // 2,
                                    self.rect.height // 2 - textsurface.get_height() // 2))
        self.img_hover.blit(textsurface, (self.rect.width // 2 - textsurface.get_width() // 2,
                                          self.rect.height // 2 - textsurface.get_height() // 2))
        self.img_down.blit(textsurface, (self.rect.width // 2 - textsurface.get_width() // 2,
                                         self.rect.height // 2 - textsurface.get_height() // 2))
        self.img_disabled.blit(textsurface, (self.rect.width // 2 - textsurface.get_width() // 2,
                                             self.rect.height // 2 - textsurface.get_height() // 2))
