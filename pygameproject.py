import pygame
from pygame.locals import *
import os, sys
from ball import ball
import pymunk


pygame.init()
pygame.mixer.init()
pygame.font.init()


dimensions = [1024, 600]
pygame.display.set_mode(dimensions)
pygame.display.set_caption('My Space Game')
screen = pygame.display.get_surface()
screen.fill((124, 255, 0)) 

#create an image object
#background = pygame.image.load("background.jpg") 
#screen.blit(background, (0,0)) #blit command can be used to show any image.

myfont = pygame.font.SysFont('ArialBold', 30)


myVector = pymunk.Vec2d(10, 10)
myBall = ball(myVector)


x = 0
y = 200

Exit = False
clock = pygame.time.Clock()
while not Exit:
    screen.fill((255, 255, 255)) 
    timer = int(pygame.time.get_ticks()/1000)
    timer = str(timer)
    clock.tick(60)

    myBall.move()

    pygame.display.flip()
    pygame.display.update() 

    for event in pygame.event.get():
        if event.type == QUIT:
            Exit = True 
    
pygame.quit()
sys.exit(0)