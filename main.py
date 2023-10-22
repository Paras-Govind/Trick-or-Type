import pygame
import pygame_menu
import pygame.freetype

from common import *
from text import Text
from spooks import *

background_color = "#3F3F3F"

pygame.display.set_caption('Trick or Type')

ghosts = pygame.sprite.Group()


def game_loop():
    text = Text(gameDisplay, ['This', 'This is another longer sentence'])
    gameExit = False

    ghostGap = 100
    darkness = 0
 
    while not gameExit:
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
        
        pygame.display.update()
        clock.tick(60)
        ghostGap = ghostGap - 1
        if ghostGap == 0:
            ghostGap = 100
            newGhost = Ghost((0, 250), [False, True, False, False], 10, 0)
            ghosts.add(newGhost)
        
menu = pygame_menu.Menu(width=display_width, height=display_height,
                    theme=pygame_menu.themes.THEME_DARK,
                    title='Welcome')

username_box = menu.add.text_input(title="Username: ")
menu.add.button('Create room', game_loop)

code_box = menu.add.text_input(title="Room code: ")
menu.add.button('Join room', game_loop)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.center_content()

menu.mainloop(gameDisplay)
pygame.quit()
quit()