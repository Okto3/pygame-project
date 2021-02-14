import pygame

class platform(pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.rectangle = pygame.rect.Rect(176, 134, 30, 30)
        self.rectangle_draging = False
        self.surface = pygame.display.get_surface()
        self.offset_x = 0
        self.offset_y = 0

        
        

    def drag (self):

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:            
                    if self.rectangle.collidepoint(event.pos):
                        self.rectangle_draging = True
                        mouse_x, mouse_y = event.pos
                        self.offset_x = self.rectangle.x - mouse_x
                        self.offset_y = self.rectangle.y - mouse_y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:            
                    self.rectangle_draging = False

            elif event.type == pygame.MOUSEMOTION:
                if self.rectangle_draging:
                    mouse_x, mouse_y = event.pos
                    self.rectangle.x = mouse_x + self.offset_x
                    self.rectangle.y = mouse_y + self.offset_y
                    #self.move()

    def move (self):
            
            self.drawRectangle()
            #self.surface.blit(self.surface, (self.rectangle.x, self.rectangle.y))
    
    def drawRectangle (self):
        self.update()
        pygame.draw.rect(self.surface, (0,255,0), self.rectangle)

 