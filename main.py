import pygame
import pygame_menu
import pygame.freetype
import pygame.event
import random
from pygame import mixer 
from networking import Network

mixer.pre_init()
mixer.init()

from common import *
from text import Text, request_text
from spooks import *

pygame.mixer.Channel(0).play(pygame.mixer.Sound("assets/audio/music.mp3"))

background_color = "#3F3F3F"

pygame.display.set_caption('Trick or Type')

ghosts = pygame.sprite.Group()
pumpkins = pygame.sprite.Group()
pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE|pygame.DOUBLEBUF)

scare = pygame.image.load("assets/images/jumpscare.jpg")
scare = pygame.transform.scale(scare, (display_width, display_height))


class Game:
    def __init__(self) -> None:
        self.gameDisplay = gameDisplay
        self.code = ""
        self.username = ""        
        self.menu = pygame_menu.Menu(width=display_width, height=display_height,
                        theme=pygame_menu.themes.THEME_DARK,
                        title='Welcome')
        self.create_room_menu = pygame_menu.Menu(width=display_width, height=display_height,
                        theme=pygame_menu.themes.THEME_DARK,
                        title='Room')
        
        self.username_box = self.menu.add.text_input(title="Username: ")
        self.menu.add.button("Create room", self.create_room_loop)

        self.code_box = self.menu.add.text_input(title="Room code: ")
        self.menu.add.button("Join room", self.join_room_loop)
        self.menu.add.button("Quit", pygame_menu.events.EXIT)
        self.menu.center_content()
        self.network = Network()
        
    def message_display(self, text):
        largeText = pygame.font.Font("assets/fonts/griffy.ttf", 100)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        self.gameDisplay.blit(TextSurf, TextRect)
        
    def game_loop(self):
        text = Text(self.gameDisplay, request_text(), self.network, self.code)
        gameExit = False

        ghostGap = 500
        pumpGap = 50
        darkness = 0
        pumpFlag = True
        reached_end = False
        while not gameExit:

            if darkness == 0:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == self.network.next_phrase_event:
                        self.next_text()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return
                        if event.unicode == text.current_letter():
                            reached_end = text.next_letter()
        
                self.gameDisplay.fill(background_color)
                text.text_surf.fill(background_color)
                
                i = 0
                # render each letter of the current sentence one by one
                for (idx, (letter, metric)) in enumerate(zip(text.current_text(), text.metrics)):
                    if idx == text.letter_index:
                        color = 'lightblue'
                    elif idx < text.letter_index:
                        color = 'red'
                    else:
                        color = 'lightgrey'
                    Text.font.render_to(text.text_surf, (i, text.baseline), letter, color)
                    i += metric[Text.M_ADV_X]
                
                self.gameDisplay.blit(text.text_surf, text.text_surf_rect)
                
                if reached_end:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("assets/audio/music.mp3"))
                    gameDisplay.blit(scare,(0,0))

                pygame.display.update()

                finishedGhosts = []

                for ghost in ghosts:
                    if ghost.update(pygame.display.get_window_size()[0],pygame.display.get_window_size()[1],self.gameDisplay) == True:
                        finishedGhosts.append(ghost)

                for ghost in finishedGhosts:
                    ghosts.remove(ghost)

            else:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        mousePos = pygame.mouse.get_pos()

                        pumpkinsToRemove = []

                        for pumpkin in pumpkins:
                            if pumpkin.checkForInput(mousePos):
                                darkness = darkness - 1
                                pumpkinsToRemove.append(pumpkin)

                        for pumpkin in pumpkinsToRemove:
                            pumpkins.remove(pumpkin)

                self.gameDisplay.fill((0, 0, 0))

                for pumpkin in pumpkins:
                    self.gameDisplay.blit(pumpkin.surf, pumpkin.rect)

            pygame.display.update()
            clock.tick(60)
            ghostGap = ghostGap - 1
            pumpGap = pumpGap - 1
            if ghostGap == 0:
                ghostGap = 100
                newGhost = Ghost((0, 250), [False, True, True, False], 10, 0)
                ghosts.add(newGhost)

            if darkness == 0 and pumpFlag == True and pumpGap == 0:
                pumpFlag = False

                newPumpkin = Pumpkin((25, 250), 200)
                pumpkins.add(newPumpkin)
                darkness = darkness + 1
                
    def start_game(self):
        self.game_loop()
        
    def create_room_loop(self):
        self.username = self.username_box.get_value()
        self.network.send(f"c{self.username}")  
        self.network.send(f"mc")
        loop = True
        while loop:
            self.network.check_network()
            for event in pygame.event.get():
                if event.type == self.network.create_room_event:
                    self.code = event.room_code
                    loop = False
                    break
        
        self.create_room_menu.add.label(f"Room code: {self.code}")
        self.create_room_menu.add.button("Start", self.join_room_loop, self.code)
        self.create_room_menu.add.button("Quit", pygame_menu.events.EXIT)
        self.create_room_menu.mainloop(self.gameDisplay)

    def join_room_loop(self, code=None):
        if not code:
            self.code = self.code_box.get_value()
        else:
            self.network.send(f"ms{self.code}")
        gameExit = False
        while not gameExit:
            self.network.check_network()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                if event.type == self.network.start_event:
                    self.start_game()
                
            self.gameDisplay.fill(white)
            self.message_display(f"Room code: {self.code}. Waiting for host...")
            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.menu.mainloop(game.gameDisplay)
    pygame.quit()
    quit()
