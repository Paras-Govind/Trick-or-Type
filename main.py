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
ouiji = pygame.sprite.Group()
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
        pumpGap = 100000
        darkness = 0
        ouijiCurse = False
        cursedLetters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

        reached_end = False
        
        while not gameExit:
            self.network.check_network()
            if darkness == 0:
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == self.network.next_phrase_event:
                        text.next_text()
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


                finishedGhosts = []

                for ghost in ghosts:
                    if ghost.update(pygame.display.get_window_size()[0],pygame.display.get_window_size()[1],self.gameDisplay) == True:
                        finishedGhosts.append(ghost)

                for ghost in finishedGhosts:
                    ghosts.remove(ghost)

                for ghost in ghosts:
                    self.gameDisplay.blit(ghost.surf, ghost.rect)

                pygame.display.flip()

            elif ouijiCurse == True:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == self.network.next_phrase_event:
                        text.next_text()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return
                        if event.unicode in cursedLetters:
                            pass
                        elif event.unicode == text.current_letter():
                            text.next_letter()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousePos = pygame.mouse.get_pos()

                        for ouija in ouiji:
                            result = ouija.checkInput(mousePos)
                            if result == text.current_letter():
                                text.next_letter()

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

                for ghost in ghosts:
                    self.gameDisplay.blit(ghost.surf, ghost.rect)

                pygame.display.flip()

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
            if darkness == 0:
                ghostGap = ghostGap - 1
                pumpGap = pumpGap - 1
            if ghostGap <= random.randint(1, 500) and darkness == 0:
                ghostGap = 500
                directionValue = random.randint(1, 8)
                directions = []
                start = ()
                if directionValue == 1:
                    directions = [True, False, False, False]
                    start = (display_width, random.randint(200,400))
                elif directionValue == 2:
                    directions = [False, True, False, False]
                    start = (0, random.randint(200, 400))
                elif directionValue == 3:
                    directions = [False, False, True, False]
                    start = (random.randint(250, 500), display_height)
                elif directionValue == 4:
                    directions = [False, False, False, True]
                    start = (random.randint(250, 500), 0)
                elif directionValue == 5:
                    directions = [True, False, True, False]
                    start = (display_width, display_height)
                elif directionValue == 6:
                    directions = [True, False, False, True]
                    start= (display_width, 0)
                elif directionValue == 7:
                    directions = [False, True, True, False]
                    start = (0, display_height)
                else:
                    directions = [False, True, False, True]
                    start = (0, 0)

                ghosts.add(Ghost(start ,directions, random.randint(1, 10)))

            if pumpGap <= random.randint(1, 100000) and darkness == 0:
                pumpGap = 100000
                pumpkinsToGrow = random.randint(3, 10)
                pumpkinSize = random.randint(300, 500)

                for i in range(0, pumpkinsToGrow):
                    pumpkins.add(Pumpkin((random.randint(0, display_width-pumpkinSize), random.randint(0, display_height-pumpkinSize)), pumpkinSize))

                darkness = pumpkinsToGrow
                
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
            self.network.send(f"c{self.username}")
            self.code = self.code_box.get_value()
            self.network.send(f"mj{self.code}")
            loop = True
            while loop:
                self.network.check_network()
                for event in pygame.event.get():
                    if event.type == self.network.join_room_event:
                        loop = False
                        break
                    elif event.type == self.network.error_event:
                        self.message_display("Invalid room code")
                        print("Invalid room code")
                        return
        else:
            self.network.send(f"ms{self.code}")
        gameExit = False
        while not gameExit:
            self.network.check_network()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                elif event.type == self.network.start_event:
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
