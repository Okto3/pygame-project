import pygame
from pygame.locals import *
import os, sys
from ball import ball
import pymunk
import random
from platform import platform


pygame.init()
pygame.mixer.init()
pygame.font.init()
dimensions = [1024, 600]
pygame.display.set_mode(dimensions)
pygame.display.set_caption('My Ball Game')
surface = pygame.display.get_surface()
myfont = pygame.font.SysFont('ArialBold', 30)
myVector = pymunk.Vec2d(10, 10)
myBall = ball(myVector)
myPlatform = platform()



Exit = False
clock = pygame.time.Clock()

while not Exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Exit = True 

    surface.fill((255, 255, 255)) 
    timer = int(pygame.time.get_ticks()/1000)
    timer = str(timer)
    clock.tick(60)


    myPlatform.drawrect()
    myBall.move()
    if myPlatform.drag() == False:
        Exit = True

    pygame.display.flip()
    pygame.display.update()

    
pygame.quit()
sys.exit(0)