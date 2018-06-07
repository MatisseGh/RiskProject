import pygame
import sys


class TextField:
    """Allows for keyboard input (AZERTY) when selected."""
    def __init__(self, screen, rect):
        self.screen = screen
        self.rect = rect
        self.selected = False
        self.text = ""
        self.is_down = False
        self.buttonClick = pygame.mixer.Sound('data/music/button_click.ogg')
        self.load_images()

    def update(self):
        """listens to keypresses and updates the text. Calls draw()."""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        left = self.rect.left
        right = self.rect.right
        top = self.rect.top
        bottom = self.rect.bottom

        if left <= mouse[0] <= right and top <= mouse[1] <= bottom:
            if click[0] == 1 and self.is_down is False:
                self.buttonClick.play(0)
                self.is_down = True          # wouter: the button will trigger only when the mouse is released while over the button
            if click[0] == 0 and self.is_down is True:
                # wouter: mouse is pressed, do action
                self.is_down = False
                self.selected = True
        else:
            if click[0] == 1 and self.is_down is False:
                self.selected = False
        if self.selected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    buttons = {pygame.K_a: "q", pygame.K_k: "k", pygame.K_u: "u",
                               pygame.K_b: "b", pygame.K_l: "l", pygame.K_v: "v",
                               pygame.K_c: "c", pygame.K_SEMICOLON: "m", pygame.K_w: "z",
                               pygame.K_d: "d", pygame.K_n: "n", pygame.K_x: "x",
                               pygame.K_e: "e", pygame.K_o: "o", pygame.K_y: "y",
                               pygame.K_f: "f", pygame.K_p: "p", pygame.K_z: "w",
                               pygame.K_g: "g", pygame.K_q: "a", pygame.K_SPACE: " ",
                               pygame.K_h: "h", pygame.K_r: "r",
                               pygame.K_i: "i", pygame.K_s: "s",
                               pygame.K_j: "j", pygame.K_t: "t",
                               }
                    if event.key in buttons.keys():
                        self.text += buttons[event.key]
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        print(self.text)
        self.draw()

    def load_images(self):
        """loads the background image."""
        self.selected_img = pygame.transform.scale(pygame.image.load("data/backgrounds/text_view_selected.png"), self.rect.size).convert_alpha()
        self.img = pygame.transform.scale(pygame.image.load("data/backgrounds/text_view.png"), self.rect.size).convert_alpha()

    def draw(self):
        """draws the textField to the screen and adds it's rect to the render update list."""
        if self.selected:
            background = self.selected_img.copy()
        else:
            background = self.img.copy()
        myfont = pygame.font.Font('data/fonts/AUGUSTUS.TTF', 20)
        textsurface = myfont.render(self.text, True, (255, 255, 255))
        self.screen.update_rects.append(self.rect)
        background.blit(textsurface, (15, background.get_rect().centery - textsurface.get_height() // 2))
        self.screen.screen.blit(background, self.rect)
