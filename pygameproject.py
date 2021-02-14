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
pygame.display.set_caption('My Space Game')
screen = pygame.display.get_surface()
screen.fill((124, 255, 0)) 
myfont = pygame.font.SysFont('ArialBold', 30)
myVector = pymunk.Vec2d(10, 10)
myBall = ball(myVector)
rectangle = pygame.rect.Rect(176, 134, 30, 30)

#added from website
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

rectangle = pygame.rect.Rect(176, 134, 30, 30)
rectangle_draging = False
# end


Exit = False
clock = pygame.time.Clock()

while not Exit:
    screen.fill((255, 255, 255)) 
    timer = int(pygame.time.get_ticks()/1000)
    timer = str(timer)
    clock.tick(60)

    myBall.move()
    #platform()
    pygame.draw.rect(screen, (255,0,0), rectangle)

    pygame.display.flip()
    pygame.display.update()

    #start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:            
                if rectangle.collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle.x - mouse_x
                    offset_y = rectangle.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                rectangle_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                rectangle.x = mouse_x + offset_x
                rectangle.y = mouse_y + offset_y

    pygame.draw.rect(screen, RED, rectangle)

    #end 

    for event in pygame.event.get():
        if event.type == QUIT:
            Exit = True 
    
pygame.quit()
sys.exit(0)