import pygame
import pygame_menu
import time

from common import *

clock = pygame.time.Clock()

# menu = pygame_menu.Menu(display_width, display_height,
#                        theme=pygame_menu.themes.THEME_BLUE,
#                        title='Welcome')

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    intro = False
                
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Trick or Type", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(15)