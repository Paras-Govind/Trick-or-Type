import pygame

pygame.init()

from config import *

clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width,display_height))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()