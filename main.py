import pygame
import pygame_menu
import pygame.freetype

from common import *
from text import Text, request_text
from spooks import *

background_color = "#3F3F3F"

pygame.display.set_caption('Trick or Type')

ghosts = pygame.sprite.Group()
pumpkins = pygame.sprite.Group()

code = ""

def game_loop(code: str):
    text = Text(gameDisplay, request_text())
    print(code)
    gameExit = False

    ghostGap = 100
    pumpGap = 50
    darkness = 0
    pumpFlag = True
    
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
            pygame.display.flip()

            finishedGhosts = []

            for ghost in ghosts:
                if ghost.update(pygame.display.get_window_size()[0],pygame.display.get_window_size()[1],gameDisplay) == True:
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

            gameDisplay.fill((0, 0, 0))

            for pumpkin in pumpkins:
                gameDisplay.blit(pumpkin.surf, pumpkin.rect)

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
