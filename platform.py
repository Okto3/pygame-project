import pygame

class platform(pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('platform.png')
        self.image.set_colorkey((0,0,20))
        
        self.rect_draging = False
        self.surface = pygame.display.get_surface()
        self.offset_x = 0
        self.offset_y = 0
        self.image = pygame.transform.rotate(self.image,45)
        self.rect = self.image.get_rect()
        self.rect.mask = pygame.mask.from_surface(self.rect.image)
    

    def drag (self):

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:            
                    if self.rect.collidepoint(event.pos):
                        print('colide')
                        self.rect_draging = True
                        mouse_x, mouse_y = event.pos
                        self.offset_x = self.rect.x - mouse_x
                        self.offset_y = self.rect.y - mouse_y
                        

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:            
                    self.rect_draging = False

            elif event.type == pygame.MOUSEMOTION:
                if self.rect_draging:
                    mouse_x, mouse_y = event.pos
                    self.rect.x = mouse_x + self.offset_x
                    self.rect.y = mouse_y + self.offset_y
            
            elif event.type == pygame.QUIT:
                return False
        return True            

    def move (self):
            self.drawrect()

    
    def drawrect (self):
        self.surface.blit(self.image,(self.rect.x,self.rect.y))
        #pygame.draw.rect(self.surface, (0,0,0), self.image)
        
        

 