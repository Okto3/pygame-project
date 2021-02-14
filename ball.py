import pygame
import math

class ball(pygame.sprite.Sprite):
    def __init__ (self,vector):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ball2.png')
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.vector = vector
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 1
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        if self.image.get_rect().height + self.y > self.screen.get_height():
            self.dy *= -.8
            self.y = self.screen.get_height() - self.image.get_rect().height
        self.dy += 1 

        self.x += self.dx
        self.y += self.dy        

    def calcnewpos(self,vector):
        (angle,z) = vector
        (dx,dy) = (z*math.cos(angle),z*math.sin(angle))

    def move(self):
        self.update()
        self.screen.blit(self.image, (self.x, self.y))
