import pygame

from config import *

pygame.init()

clock = pygame.time.Clock()

info = pygame.display.Info()

display_width, display_height = info.current_w, info.current_h
 
gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()