import pygame
import time

from common import *
from menu import game_intro
 
pygame.init()
 
ghost_width = 73

pygame.display.set_caption('Trick or Type')

 
ghostImg = pygame.image.load('assets/images/home_ghost.jpg')
 
def ghost(x,y):
    gameDisplay.blit(ghostImg,(x,y))

 
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
 
    pygame.display.update()
 
    time.sleep(2)
 
    game_loop()
    
def game_loop():
 
    gameExit = False
 
    while not gameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
        gameDisplay.fill(white)
        message_display("Typing game")
        
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()