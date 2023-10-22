import pygame
import pygame_menu
import pygame.freetype
import random

from common import *
from text import Text, request_text
from spooks import *

background_color = "#3F3F3F"

pygame.display.set_caption('Trick or Type')

ghosts = pygame.sprite.Group()
pumpkins = pygame.sprite.Group()
pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE|pygame.DOUBLEBUF)


code = ""

def game_loop(code: str):
    text = Text(gameDisplay, request_text())
    print(code)
    gameExit = False

    ghostGap = 500
    pumpGap = 100000
    darkness = 0
    
    while not gameExit:

        if darkness == 0:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.unicode == text.current_letter():
                        text.next_letter()
    
            gameDisplay.fill(background_color)
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
            
            gameDisplay.blit(text.text_surf, text.text_surf_rect)


            finishedGhosts = []

            for ghost in ghosts:
                if ghost.update(display_width,display_height,gameDisplay) == True:
                    finishedGhosts.append(ghost)
                else:
                    gameDisplay.blit(ghost.surf, ghost.rect)

            for ghost in finishedGhosts:
                ghosts.remove(ghost)

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

            gameDisplay.fill((0, 0, 0))

            for pumpkin in pumpkins:
                gameDisplay.blit(pumpkin.surf, pumpkin.rect)

        pygame.display.update()
        clock.tick(60)
        ghostGap = ghostGap - 1
        if random.randint(1, 500) >= ghostGap:
            ghostGap = 500
            ghostDirection = random.randrange(1, 9)
            direction = []
            start = ()
            if ghostDirection == 1:
                direction = [True, False, False, False]
                start = (display_width, random.randint(100, 400))
            elif ghostDirection == 2:
                direction = [False, True, False, False]
                start = (-149, random.randint(100, 400))
            elif ghostDirection == 3:
                direction = [False, False, True, False]
                start = (random.randint(250, 450), display_height)
            elif ghostDirection == 4:
                direction = [False, False, False, True]
                start = (random.randint(250, 450), -149)
            elif ghostDirection == 5:
                direction = [True, False, True, False]
                start = (display_width, display_height)
            elif ghostDirection == 6:
                direction = [True, False, False, True]
                start = (display_width, -149)
            elif ghostDirection == 7:
                direction = [False, True, True, False]
                start = (-149, display_height)
            elif ghostDirection == 8:
                direction = [False, True, False, True]
                start = (-149, -149)

            newGhost = Ghost(start, direction, random.randint(2, 10), 0)
            ghosts.add(newGhost)

        if darkness == 0:
            pumpGap = pumpGap - 1
            if random.randint(1, 100000) >= pumpGap:
                pumpGap = 100000

                pumpkinsToGrow = random.randint(3, 8)
                darkness = pumpkinsToGrow

                for i in range(0, pumpkinsToGrow):
                    size = random.randint(300, 500)
                    position = (random.randint(0, display_width - size), random.randint(0, display_height - size))

                    newPumpkin = Pumpkin(position, size)
                    pumpkins.add(newPumpkin)
            
menu = pygame_menu.Menu(width=display_width, height=display_height,
                    theme=pygame_menu.themes.THEME_DARK,
                    title='Welcome')


create_room_menu = pygame_menu.Menu(width=display_width, height=display_height,
                    theme=pygame_menu.themes.THEME_DARK,
                    title='Room')

create_room_menu.add.button("Start", game_loop, code)

def create_room_loop():
    code = "12345"
    # do something with code
    create_room_menu.mainloop(gameDisplay)

username_box = menu.add.text_input(title="Username: ")
menu.add.button("Create room", create_room_loop)

code_box = menu.add.text_input(title="Room code: ")
menu.add.button("Join room", game_loop)
menu.add.button("Quit", pygame_menu.events.EXIT)
menu.center_content()



menu.mainloop(gameDisplay)
pygame.quit()
quit()
