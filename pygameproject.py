import pygame
from pygame.locals import *
import os, sys

pygame.init()
pygame.mixer.init()
pygame.font.init()
 
dimensions = [1024, 600]
pygame.display.set_mode[dimensions]
pygame.display.set_caption('myGame')
screen = pygame.display.get_surface()
screen.fill((0,255,0))

input('press enter to exit')
pygame.quit()
sys.exit(0)
