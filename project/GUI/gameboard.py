import pygame
import worldstats
import sys
import csv
from troopdisplacement import TroopDisplacement
from GUI.button import Button
from GUI.drawableCountry import DrawableCountry
from GUI.events import Events
from GUI.popup import Popup
from GUI.infobar import InfoBar
from GUI.colors import Color
from GUI.statusbar import StatusBar
import GUI.screenManager


class Gameboard:
    """A visual interface for the player to interact with, should do everything the algorithm does for the bot player"""

    def __init__(self, screen):
        pygame.mixer.music.load('data/music/roman_backgroundmusic.ogg') #pygame mixer can only play .ogg files
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.6)
        self.muted = False
        self.screen = screen
        self.size = self.width, self.height = screen.get_size()
        self.update_rects = []
        self.buttons = []
        self.countries = []
        self.EDETING = False
        self.showing = False
        self.create_screen_attributes()
        self.victorySound = pygame.mixer.Sound('data/music/victory.ogg')

    def create_screen_attributes(self):
        """creates all elements to display"""
        self.define_screen_attribute_sizes(self.width, self.height)
        self.worldmap_surface = self.create_worldmap()
        self.action_panel_surace = self.create_action_panel()
        self.infoBar = InfoBar(self, self.info_bar_area)
        self.statusBar = StatusBar(self, self.status_bar_area)
        self.country_info = None

    def show(self):
        """lets this screen know it's currently showing. needs to be called when loading the screen"""
        self.showing = True
        self.update_screen()
        pygame.display.update()

    def hide(self):
        """lets this screen know it's no longer showing."""
        self.showing = False

    def define_screen_attribute_sizes(self, screenwidth, screenheight):
        """defines the sizes of the different attributes on screen"""
        # wouter: define the area of the action panel
        width = screenwidth
        height = screenheight // 6
        xPos = 0
        yPos = screenheight - height
        self.action_panel_area = pygame.Rect(xPos, yPos, width, height)
        # wouter: define the area of the infoBar
        width = screenwidth // 2
        height = 60
        xPos = screenwidth // 2 - width // 2
        yPos = -height
        self.info_bar_area = pygame.Rect(xPos, yPos, width, height)
        self.status_bar_area = pygame.Rect(screenwidth - 300, -440, 300, 500)

        # wouter: define the area of the worldmap
        width = screenwidth
        height = screenheight - self.action_panel_area.height
        xPos = 0
        yPos = 0
        self.worldmap_area = pygame.Rect(xPos, yPos, width, height)

    def update_screen(self, fetch_latest_data=False):
        """update_screen(self, fetch_latest_data=False). Updates all elements on the screen, this includes the buttons and countries,
         if True is given as an argument, the drawable counties will be updated to the latest status of the actual countries"""
        if self.showing:
            self.screen.blit(self.worldmap_surface, self.worldmap_area)
            self.screen.blit(self.action_panel_surace, self.action_panel_area)
            self.update_buttons()
            self.update_countries(fetch_latest_data)
            self.statusBar.update()
            if self.country_info is not None:
                self.country_info.update()
            self.infoBar.update()
            pygame.display.update(self.update_rects)
            if len(self.update_rects) > 16:
                print("WARNING: updating a lot of areas on the screen!")
                print("amount of update rects:", len(self.update_rects))
            self.update_rects.clear()

    def create_worldmap(self):
        """returns a surface containing the worldmap and all it's countries with the size of worldmap_area"""
        background = pygame.image.load("data/maps/roman_map.png").convert()
        normal_width = 1920
        normal_height = 720
        background = pygame.transform.scale(background, self.worldmap_area.size)
        background_width = background.get_width()
        background_heigth = background.get_height()
        for i, continent in enumerate(worldstats.instance.continents):
            for j, country in enumerate(continent.countries):
                x_position = (self.worldmap_area.left + int(country.x)) * background_width // normal_width
                y_position = (self.worldmap_area.top + int(country.y)) * background_heigth // normal_height
                country_width = 50
                countrie_height = 50
                rect = pygame.Rect(x_position, y_position, country_width, countrie_height)
                drawable_country = DrawableCountry(self, rect, country, Color(0))
                country.drawable = drawable_country
                self.countries.append(drawable_country)
        return background

    def create_action_panel(self):
        """returns a surface containing the action panel and creates the buttons in the action_panel"""
        action_panel = pygame.Surface(self.action_panel_area.size)
        background = pygame.transform.scale(pygame.image.load('data/backgrounds/roman_action_panel_background.png'),
                                            self.action_panel_area.size).convert()
        action_panel.blit(background, (0, 0))
        # create buttons:
        self.mute_button = Button(self, pygame.Rect(self.width - 125, self.action_panel_area.top + 30, 100, 50),
                                  "Mute", 20, self.button_click_mute)
        decrease_button = Button(self, pygame.Rect(self.width - 125, self.action_panel_area.top + 80, 50, 25),
                                 "-", 20, self.decrease_volume)
        increase_button = Button(self, pygame.Rect(self.width - 75, self.action_panel_area.top + 80, 50, 25),
                                 "+", 20, self.increase_volume)
        button_width = self.width * 5 // 26
        button_height = button_width // 150 * 60
        self.finish_add_troops_button = Button(self, pygame.Rect(self.action_panel_area.left + 50, self.action_panel_area.top + 30,
                                               button_width, button_height), "finish adding troops", 18)
        self.finish_add_troops_button.user_data = "finish_add_troops"
        self.finish_add_troops_button.enabled = False
        self.finish_attack_button = Button(self, pygame.Rect(self.action_panel_area.left + 100 + button_width, self.action_panel_area.top + 30,
                                           button_width, button_height), "finish attack", 25)
        self.finish_attack_button.user_data = "finish_attack"
        self.finish_attack_button.enabled = False
        self.skip_move_button = Button(self, pygame.Rect(self.action_panel_area.left + 150 + 2 * button_width, self.action_panel_area.top + 30,
                                       button_width, button_height), "skip move", 25)
        self.skip_move_button.user_data = "skip_move"
        self.info_button = Button(self, pygame.Rect(self.action_panel_area.left + 200 + 3 * button_width, self.action_panel_area.top + 30,
                                                    button_width, button_height), "Info", 25, self.info)
        self.info_button.user_data = "Info"
        img = pygame.image.load('data/buttons/bonus_info.png')
        img_hover = pygame.image.load('data/buttons/bonus_info_h.png')
        self.BonusInfo_button = Button(self, pygame.Rect(self.width - 260, self.height - 350, 200, 50), "",
                                       images=(img, img_hover, img_hover, img), action=self.bonusInfo)
        # add buttons to button-list:
        self.buttons.append(self.BonusInfo_button)
        self.buttons.append(decrease_button)
        self.buttons.append(increase_button)
        self.buttons.append(self.mute_button)
        self.buttons.append(self.skip_move_button)
        self.buttons.append(self.finish_add_troops_button)
        self.buttons.append(self.finish_attack_button)
        self.buttons.append(self.info_button)
        return action_panel

    def info(self):
        """switches the diplaying screen to INFOSCREEN"""
        GUI.screenManager.instance.setScreen(GUI.screenManager.instance.INFOSCREEN)
        while not self.showing:
            GUI.screenManager.instance.update_screen()

    def bonusInfo(self):
        """displays a popup with information about the continental bonus"""
        pos = (350, 350)
        left = self.width // 2 - pos[0] // 2
        top = self.height // 2 - pos[1] // 2
        popup_rect = pygame.Rect((left, top), pos)
        popup = Popup(self, popup_rect, Popup.CONINENT_BONUS_INFO, (0, 0))
        popup.show()

    def update_buttons(self):
        """updates and draws all buttons, needs to be called in game loop"""
        for btn in self.buttons:
            btn.update()

    def update_countries(self, fetch_latest_data=False):
        """updates and draws all countries, needs to be called in game loop"""
        for country in self.countries:
            if fetch_latest_data:
                country.fetch_latest_data()
            country.update()

    def write_county_pos_to_file(self):
        """for repositioning the countries if needed"""
        with open('data/output_countries.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for d_country in self.countries:
                normal_width = 1920
                normal_height = 720
                x_position = (self.worldmap_area.left + int(d_country.rect.left)) * normal_width // self.worldmap_area.width
                y_position = (self.worldmap_area.top + int(d_country.rect.top)) * normal_height // self.worldmap_area.height
                writer.writerow([d_country, x_position, y_position])

    def button_click_fullscreen(self):
        """toggles fullscreen mode"""
        if self.fullscreen is False:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.fullscreen = True
        else:
            self.screen = pygame.display.set_mode(self.size)
            self.fullscreen = False
        self.update_screen(True)

    def button_click_mute(self):
        """play or mute the background music"""
        if self.muted is False:
            pygame.mixer.music.pause()
            self.muted = True
            self.statusBarChangeText("Music muted")
            self.mute_button.set_text("Music")
        else:
            pygame.mixer.music.unpause()
            self.muted = False
            self.statusBarChangeText("Music playing")
            self.mute_button.set_text("Mute")

    def decrease_volume(self):
        """decreases background music"""
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)

    def increase_volume(self):
        """increases background music"""
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)

    def addTroopsInput(self, player):
        """asks the given player to add troops. The amount of available troops should be set beforehand in Player.
        returns a dict with countries as keys and troops to add as values."""
        self.skip_move_button.enabled = False
        self.finish_attack_button.enabled = False
        self.finish_add_troops_button.enabled = False
        finished = False
        countries = dict()
        troops_to_place = player.troopsToPlace
        self.infoBar.set_text(player.name + " | troops to place: " + str(troops_to_place))
        self.infoBar.show()
        self.set_selectable(player, 0, highlight=True)
        while not finished:
            self.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == Events.COUNTRY_CLICK and event.country.selectable is True:
                    pos = (400, 200)
                    left = self.width // 2 - pos[0] // 2
                    top = self.height // 2 - pos[1] // 2
                    popup_rect = pygame.Rect((left, top), pos)
                    if not self.EDETING:
                        popup = Popup(self, popup_rect, Popup.AMOUNT_INPUT, (event.country.amount_of_troops, event.country.country.amountOfTroops,
                                                                             troops_to_place + event.country.amount_of_troops))
                        popup.title_text = "adding troops"
                        input = popup.show()
                    else:
                        input = None
                    if input is not None:
                        troops_to_place += (event.country.amount_of_troops - input)
                        countries[event.country.country] = input - event.country.country.amountOfTroops
                        event.country.amount_of_troops = input
                        self.infoBar.set_text(player.name + " | troops to place: " + str(troops_to_place))
                if event.type == Events.BUTTON_CLICK and event.user_data == "finish_add_troops":
                    finished = True
            if troops_to_place == 0:
                self.finish_add_troops_button.enabled = True
                self.infoBar.set_text(player.name + " | placed all troops")
            else:
                self.infoBar.set_text(player.name + " | troops to place: " + str(troops_to_place))
                self.finish_add_troops_button.enabled = False
        for drawableCountry in self.countries:
            drawableCountry.selectable = False
            drawableCountry.highlighted = False
        self.infoBar.hide()
        #for printing on statusbar
        for country in countries.keys():
            countryName = country.getName()
            troops = countries.get(country)
            playerName = player.getName()
            self.statusBarChangeText(playerName + " placed " + str(troops) + " troops on " + countryName)
        return countries

    def attackInput(self, player):
        """asks the given player for an attack, returns a TroopDisplacement with the amount of troops to attack with,
        the country to attack from and the county being attacked. Returns None if the Player does not wish to attack."""
        self.infoBar.set_text(player.name + " | attacking")
        self.infoBar.show()
        self.skip_move_button.enabled = False
        self.finish_attack_button.enabled = True
        self.finish_add_troops_button.enabled = False
        attacker = None
        defender = None
        finished = False
        self.set_selectable(player, highlight=True)
        while not finished:
            self.update_screen(True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == Events.COUNTRY_CLICK and event.country.selectable is True:
                    if event.country.country.player is player:
                        self.set_selectable(player, highlight=False)
                        attacker = event.country
                        attackable = worldstats.instance.getAttackableCountries(attacker.country)
                        for country in attackable:
                            country.drawable.selectable = True
                            country.drawable.highlighted = True
                    else:
                        defender = event.country
                        pos = (400, 200)
                        left = self.width // 2 - pos[0] // 2
                        top = self.height // 2 - pos[1] // 2
                        popup_rect = pygame.Rect((left, top), pos)
                        popup = Popup(self, popup_rect, Popup.AMOUNT_INPUT, (1, 1, attacker.amount_of_troops - 1))
                        popup.title_text = "attacking"
                        input = popup.show()
                        if input is not None:
                            self.finish_attack_button.enabled = False
                            tdp = TroopDisplacement(attacker.country, defender.country, input)
                            print(tdp)
                            return tdp
                if event.type == Events.BUTTON_CLICK and event.user_data == "finish_attack":
                    self.infoBar.hide()
                    self.finish_attack_button.enabled = False
                    return None

    def moveInput(self, player):
        """asks the given player to move troops. Returns a TroopDisplacement with the amount of troops,
        the county from witch to move and county to witch to move to. Returns None if the player does not want to move troops."""
        self.infoBar.set_text(player.name + " | moving troops")
        self.infoBar.show()
        self.skip_move_button.enabled = True
        self.finish_attack_button.enabled = False
        self.finish_add_troops_button.enabled = False
        from_country = None
        to_country = None
        finished = False
        self.set_selectable(player, must_have_group=True, highlight=True)
        while not finished:
            self.update_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == Events.COUNTRY_CLICK and event.country.selectable is True:
                    if from_country is None:
                        from_country = event.country
                        self.set_country_group_selectable(from_country.country, highlight=True)
                        from_country.selectable = False
                    else:
                        to_country = event.country
                if event.type == Events.BUTTON_CLICK and event.user_data == "skip_move":
                    self.infoBar.hide()
                    self.skip_move_button.enabled = False
                    return None
            if from_country is not None and to_country is not None:
                pos = (400, 200)
                left = self.width // 2 - pos[0] // 2
                top = self.height // 2 - pos[1] // 2
                popup_rect = pygame.Rect((left, top), pos)
                popup = Popup(self, popup_rect, Popup.AMOUNT_INPUT, (1, 1, from_country.amount_of_troops - 1))
                popup.title_text = "moving troops"
                input = popup.show()
                if input is not None:
                    self.statusBarChangeText(player.getName() + " moved " + str(input) + " troops from " +
                                             from_country.country.getName() + " to " + to_country.country.getName())
                    return TroopDisplacement(from_country.country, to_country.country, input)
                else:
                    from_country = None
                    to_country = None
                    self.set_selectable(player, must_have_group=True)

    def set_selectable(self, player, minimum_troops=1, must_have_group=False, highlight=False):
        """Sets countries selectable of a given player. optional arguments: minimum_troops, must_have_group & highlight."""
        for drawableCountry in self.countries:
            drawableCountry.selectable = False
            drawableCountry.highlighted = False
            if drawableCountry.amount_of_troops > minimum_troops and drawableCountry.country.player == player:
                if must_have_group:
                    worldstats.instance.updateCountryGroups()
                    if len(worldstats.instance.getGroup(drawableCountry.country)) > minimum_troops:
                        drawableCountry.selectable = True
                        drawableCountry.highlighted = highlight
                else:
                    drawableCountry.selectable = True
                    drawableCountry.highlighted = highlight

    def set_country_group_selectable(self, country, highlight=False):
        """Sets the group of countries surrounding the given county selectable."""
        worldstats.instance.updateCountryGroups()
        for drawableCountry in self.countries:
            if drawableCountry.country in worldstats.instance.getGroup(country):
                drawableCountry.selectable = True
                drawableCountry.highlighted = highlight
            else:
                drawableCountry.selectable = False
                drawableCountry.highlighted = highlight

    def statusBarChangeText(self, text):
        """changes the text in the statusBar"""
        self.statusBar.set_text(text)

    def botAttackPopUp(self, bot, player, amount, countryTo):
        """Displays a popup to let the player know he's under attack."""
        self.update_screen(True)
        pos = (500, 200)
        left = self.width // 2 - pos[0] // 2
        top = self.height // 2 - pos[1] // 2
        text = "OH SNAP, " + bot.name + " is attacking " + player.name + " in " + countryTo.name + " with " + str(amount) + " troops!"
        popup_rect = pygame.Rect((left, top), pos)
        popup = Popup(self, popup_rect, Popup.CONFIRMATION_INPUT_ATTACK, (text, "ok", "cancel"))
        popup.show()

    def worldDominancePopUp(self, player):
        """Displays a popup to let the player know the game is over."""
        self.update_screen(True)
        pos = (500, 200)
        left = self.width // 2 - pos[0] // 2
        top = self.height // 2 - pos[1] // 2
        text = "CONGRATULATIONS!! " + player.name + " [" + player.color.name + "] has won the game!"
        popup_rect = pygame.Rect((left, top), pos)
        popup = Popup(self, popup_rect, Popup.CONFIRMATION_INPUT_ATTACK, (text, "ok", "cancel"))
        popup.show()

    def playerEliminated(self, player, rounds):
        """Displays a popup to let the player know another player is out of the game"""
        self.update_screen(True)
        pos = (500, 200)
        left = self.width // 2 - pos[0] // 2
        top = self.height // 2 - pos[1] // 2
        text = player.name + " [" + player.color.name + "] got eliminated after " + str(rounds) + " rounds!"
        popup_rect = pygame.Rect((left, top), pos)
        popup = Popup(self, popup_rect, Popup.CONFIRMATION_INPUT_ATTACK, (text, "ok", "cancel"))
        popup.show()
