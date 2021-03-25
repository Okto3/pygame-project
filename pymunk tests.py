import random
import pygame
import pymunk
import pymunk.pygame_util
from pymunk.pygame_util import *
from pymunk.vec2d import Vec2d
from pygame.locals import *
import math



class BouncingBalls(object):
    def __init__(self) -> None:
        self.space = pymunk.Space() 
        #self.binSpace = pymunk.Space()
        self.space.gravity = (0.0, 900.0)
        self.dt = 1.0 / 60.0 
        self.physics_steps_per_frame = 1

        pygame.init()                                       
        self.screen = pygame.display.set_mode((1024, 600))
        self.clock = pygame.time.Clock()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.balls: List[pymunk.Circle] = []
        self.running = True
        self.active_shape = None
        self.dragging = False
        #self.inGame = False
        #self.inMainMenu = True
        self.gameState = 0 #0 main menu, 1 is level select, 2 is instruction, 3 is in a game
        self.binList = []
        self.dropperList = []
        self.ballsToReset= []
        

        

    def run(self) -> None:
            #self.startButton = Button(180,400,267,100,(0,0,0))
            #self.settingsButton = Button(445,401,151,94,(0,0,0))
            #self.quitButton = Button(590,401,236,94,(0,0,0))

            bounceTheBallImage = pygame.image.load('bounce the ball.png')
            self.startImage = pygame.image.load('start.png')
            self.settingsImage = pygame.image.load('settings.png')
            self.quitImage = pygame.image.load('Quite.png')

            self.level1Image = pygame.image.load('Level1.png')
            self.level2Image = pygame.image.load('Level2.png')
            self.level3Image = pygame.image.load('Level3.png')
            self.level4Image = pygame.image.load('Level4.png')
            self.level5Image = pygame.image.load('Level5.png')

            self.backImage = pygame.image.load('back.png')
            self.newPlatformImage = pygame.image.load('newPlatform.png')
            self.binImage = pygame.image.load('bin.png')
            self.ballDropImage = pygame.image.load('ballDrop.png')
            #startRect = startImage.get_rect()

            while self.running:
                for x in range(self.physics_steps_per_frame):
                    self.space.step(self.dt)
                self.process_events()
                self.update_balls()
                self.clear_screen()
                self.draw_objects()

                self.clock.tick(50)
                self.offset_x = 0
                self.offset_y = 0
                self.x = 0
                self.y = 0

                self.linePoint1X = 50
                self.linePoint1Y = 100
                self.linePoint2X = 150
                self.linePoint2Y = 100

                if self.gameState == 0:

                    self.screen.blit(bounceTheBallImage,(165,100))
                    self.screen.blit(self.startImage, (180,400))
                    self.screen.blit(self.settingsImage, (445,401))
                    self.screen.blit(self.quitImage, (590,401))

                    self.startButton = self.startImage.get_rect()
                    self.settingsButton = self.settingsImage.get_rect()
                    self.quitButton = self.quitImage.get_rect()

                    self.startButton.move_ip(180,400)
                    self.settingsButton.move_ip(445,401)
                    self.quitButton.move_ip(590,401)

                if self.gameState == 1:

                    self.screen.blit(self.level1Image, (195,100))
                    self.screen.blit(self.level2Image, (325,100))
                    self.screen.blit(self.level3Image, (460,100))
                    self.screen.blit(self.level4Image, (590,100))
                    self.screen.blit(self.level5Image, (720,100))

                    self.level1Button = self.level1Image.get_rect()
                    self.level2Button = self.level2Image.get_rect()
                    self.level3Button = self.level3Image.get_rect()
                    self.level4Button = self.level4Image.get_rect()
                    self.level5Button = self.level5Image.get_rect()

                    self.level1Button.move_ip(195,100)

                    self.screen.blit(self.backImage, (900,500))
                    self.backButton = self.backImage.get_rect()
                    self.backButton.move_ip(900,500)

                if self.gameState == 3:

                    self.screen.blit(self.newPlatformImage, (950,25))
                    self.newPlatformButton = self.newPlatformImage.get_rect()
                    self.newPlatformButton.move_ip(950,25)

                    self.screen.blit(self.backImage, (925,500))
                    self.backButton = self.backImage.get_rect()
                    self.backButton.move_ip(925,500)

                    self.screen.blit(self.binImage, (960,100))
                    self.binButton = self.binImage.get_rect()
                    self.binButton.move_ip(950,100)

                    self.screen.blit(self.ballDropImage,(950,175))
                    self.ballDropButton = self.backImage.get_rect()
                    self.ballDropButton.move_ip(950,200)

                    #self.startButton.draw(self.screen)
                    #self.settingsButton.draw(self.screen)
                    #self.quitButton.draw(self.screen)
                    
                    #pygame.draw.rect(self.screen,(0,0,0),self.level1Button)

                    pygame.display.flip()
                pygame.display.flip()

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.gameState == 3:
                    if self.newPlatformButton.collidepoint(pygame.mouse.get_pos()):
                        self.create_Platform()
                    elif self.backButton.collidepoint(pygame.mouse.get_pos()):
                        self.gameState = 1
                    elif self.binButton.collidepoint(pygame.mouse.get_pos()):
                        self.removePlatform()
                    elif self.ballDropButton.collidepoint(pygame.mouse.get_pos()):
                        #self.create_ball()
                        self.space.remove(self.trapDoor)
                        print(self.dropperList)  
                        


                    self.mouse_x, self.mouse_y = event.pos
                    nearestShape = self.space.point_query_nearest(event.pos, float("inf"), pymunk.ShapeFilter())
                    if nearestShape is not None:
                        shape = nearestShape.shape
                        if shape is not None and isinstance(shape, pymunk.Segment) and shape not in self.binList and shape not in self.dropperList:
                            self.active_shape = shape
                            self.dragging = True
                            self.mouseMotion(event)
                          
                elif self.gameState == 0:
                    if self.startButton.collidepoint(pygame.mouse.get_pos()):
                        self.gameState = 1   
                    #if self.settingsButton.collidepoint(pygame.mouse.get_pos()):
                    if self.quitButton.collidepoint(pygame.mouse.get_pos()):
                        self.running = False

                elif self.gameState == 1:
                    if self.level1Button.collidepoint(pygame.mouse.get_pos()):
                        self.gameState = 3
                        self.setUpLevel1()
                    if self.backButton.collidepoint(pygame.mouse.get_pos()):
                        self.gameState = 0


            elif event.type == pygame.KEYDOWN:
                if self.gameState == 3:
                    if event.key == pygame.K_LEFT:
                        if self.active_shape:
                            self.active_shape.rotation += 0.2
                            self.rotatePlatform()

                    if event.key == pygame.K_RIGHT:
                        if self.active_shape:
                            self.active_shape.rotation -= 0.2
                            self.rotatePlatform()

                    if event.key == pygame.K_n:
                        self.create_Platform()
                                                        
            
            elif event.type == pygame.MOUSEMOTION:
                if self.gameState == 3:
                    if self.dragging == True:
                        self.mouseMotion(event)    
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.gameState == 3:
                    self.dragging = False
        
            #ballsToReset = [ball for ball in self.balls if ball.body.position.y > 600]
            for ball in self.ballsToReset:
                if ball.body.position.y < 600:
                    print('yes')
                #self.space.remove(ball, ball.body)
                #self.balls.remove(ball)
                

             
    def setUpLevel1 (self):
        self.binLeft = pymunk.Segment(self.space.static_body,(790,500),(800,600),2.0)
        self.binRight = pymunk.Segment(self.space.static_body,(870,500),(860,600),2.0)
        self.binBottom = pymunk.Segment(self.space.static_body,(800,600),(860,600),2.0)
        self.binBottom.collision_type = 2      

        self.binList = [self.binLeft, self.binRight,self.binBottom]
        for lines in self.binList:
            lines.elasticity = .9
            lines.friction = 10
            lines.color = pygame.Color(0,0,0)

        self.dropperLeft = pymunk.Segment(self.space.static_body,(50,0),(50,50),2.0)
        self.dropperRight = pymunk.Segment(self.space.static_body,(110,0),(110,50),2.0)
        self.trapDoor = pymunk.Segment(self.space.static_body,(50,55),(110,55),2.0)

        self.dropperList = [self.dropperLeft, self.dropperRight, self.trapDoor]
        for dropperline in self.dropperList:
            dropperline.color = pygame.Color(0,0,0)

        self.space.add(self.binLeft,self.binRight,self.binBottom, self.dropperLeft, self.dropperRight, self.trapDoor)

        collInfo = self.space.add_collision_handler(1, 2)
        collInfo.begin = self.caughtTheBall

        self.create_ball()
    
    def resetBall (self):
        self.space.add(self.trapDoor)
        self.create_ball()
        
        
    def mouseMotion (self, event) -> None:
        self.mouse_x, self.mouse_y = event.pos
        self.space.remove(self.active_shape)
        self.active_shape.body.position = (self.mouse_x + self.offset_x - self.linePoint1X,self.mouse_y + self.offset_y - self.linePoint1Y)
        self.space.add(self.active_shape)
        


    def create_Platform (self) -> None:
        static_body = self.space.static_body
        self.platformLine = pymunk.Segment(static_body, (self.linePoint1X, self.linePoint1Y), (self.linePoint2X, self.linePoint2Y), 7.0)
        self.platformLine.elasticity = .99
        self.platformLine.friction = 0.9
        self.platformLine.color = pygame.Color(0,0,0)
        self.platformLine.rotation = math.pi/2 # I MADE UP THIS ROTATION VARIABLE AND ASSIGNED IT TO PLATFORM LINE.
        self.space.add(self.platformLine)

    def rotatePlatform (self) -> None:
        
        xc = (self.active_shape.a.x + self.active_shape.b.x) / 2
        yc = (self.active_shape.a.y + self.active_shape.b.y) / 2
        xa = xc - math.sin(self.active_shape.rotation)*50
        ya = yc - math.cos(self.active_shape.rotation)*50
        xb = xc + math.sin(self.active_shape.rotation)*50
        yb = yc + math.cos(self.active_shape.rotation)*50
        
        r = self.active_shape.rotation

        self.space.remove(self.active_shape)
        self.active_shape = pymunk.Segment(self.space.static_body, (xa, ya), (xb, yb), 7.0)
        self.active_shape.rotation = r
        self.active_shape.color = pygame.Color(0,0,0) 
        self.space.add(self.active_shape)
        self.active_shape.elasticity = .99
        self.active_shape.friction = 0.9


    def update_balls(self) -> None:  
        if self.gameState == 3:          
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.create_ball()

            
        balls_to_remove = [ball for ball in self.balls if ball.body.position.y > 700]
        for ball in balls_to_remove:
            self.space.remove(ball, ball.body)
            self.balls.remove(ball)
            #self.space.add(self.trapDoor)
            #self.create_ball()
       

    def create_ball(self) -> None:
        mass = 10
        radius = 25
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = 80, -50
        self.circle = pymunk.Circle(body, radius, (0, 0))
        self.circle.elasticity = .9
        self.circle.friction = 0.9
        self.space.add(body, self.circle)
        self.balls.append(self.circle)
        self.ballsToReset.append(self.circle)
        self.circle.collision_type = 1


    def caughtTheBall(self, space, arbiter, data):
        s1 = arbiter.shapes
        print('colission detected')

        return True

    def removePlatform(self):
        self.space.remove(self.active_shape)

    def clear_screen(self) -> None:
        background = pygame.image.load('background.png')
        self.screen.blit(background,(0,0))
    def draw_objects(self) -> None:
        self.space.debug_draw(self.draw_options)





class Button(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,colour):

        self.x = x; self.y = y; self.width = width; self.height = height; self.colour = colour

    def draw(self,screen):

        pygame.draw.rect(screen,self.colour,(self.x,self.y,self.width,self.height))

    def isClicking(self):

        mouse = pygame.mouse.get_pos()
              

        
if __name__ == "__main__":
    game = BouncingBalls()
    game.run()