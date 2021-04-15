import random
import pygame
import pymunk
import pymunk.pygame_util
from pymunk.pygame_util import *
from pymunk.vec2d import Vec2d
from pygame.locals import *
import math
from datetime import datetime



class BouncingBalls(object):
    def __init__(self) -> None:
        self.space = pymunk.Space() 
        self.space.gravity = (0.0, 900.0)
        #self.dt = 1.0 / 60.0 
        self.physics_steps_per_frame = 1

        pygame.init()                                       
        self.screen = pygame.display.set_mode((1024, 600))
        self.clock = pygame.time.Clock()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.balls: List[pymunk.Circle] = []
        self.running = True
        self.active_shape = None
        self.dragging = False
        self.gameState = 0 #0 is the main menu, 1 is level select, 2 is instruction, 3 is in a game, 4 is scoring screen
        self.binList = []
        self.dropperList = []
        self.ballsToReset= []
        self.platformList = []
        self.spikesList = []
        self.walls = []
        self.pendulumObjects = []  
        self.timesList = []      
        self.highScores = []

        pygame.font.init()
        self.myfont = pygame.font.SysFont('Arial Black', 40)
        self.resultFont = pygame.font.SysFont('Arial Black',30)

        with open("highscores.txt", 'r') as file:
            for line in file:
                line = line.strip()
                self.highScores.append(line+'\n')
        

        

    def run(self) -> None:

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
            self.instructions = pygame.image.load('instructions.png')

            self.star0Image = pygame.image.load('0stars.png')
            self.star1Image = pygame.image.load('1stars.png')
            self.stars2Image = pygame.image.load('2stars.png')
            self.stars3Image = pygame.image.load('3stars.png')
            self.winImage = pygame.image.load('Win.png')
            self.spikesImage = pygame.image.load('spikes.png')
            self.wormholeImage = pygame.image.load('wormhole.png')
            self.wormholeImage2 = pygame.image.load('wormhole2.png')
            self.doubleGravityImage = pygame.image.load('doubleBackground.png')

            #variables for timers
            self.timeOfDrop = 0
            self.timeOfFinish = 0
            self.levelTime = 0
            self.initialLevelTime = 0

            mass = 10
            radius = 25
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            self.body = pymunk.Body(mass, inertia)
            self.body.position = 80, 0
            self.circle = pymunk.Circle(self.body, radius, (0, 0))
            self.circle.elasticity = .9
            self.circle.friction = 0.9
            lastTime = datetime.now()
            dilatedTime = 0
            

            while self.running:
                
                self.space.step(1.0/60.0)
                self.process_events()
                self.update_balls()
                self.clear_screen()
                if self.gameState == 9:
                    self.screen.blit(self.doubleGravityImage,(0,0))
                self.draw_objects()

                self.clock.tick(50)
                self.offset_x = 0
                self.offset_y = 0
                self.x = 0
                self.y = 0

                self.linePoint1X = 50
                self.linePoint1Y = 200
                self.linePoint2X = 150
                self.linePoint2Y = 200


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
                    self.level2Button.move_ip(325,100)
                    self.level3Button.move_ip(460,100)
                    self.level4Button.move_ip(590,100)
                    self.level5Button.move_ip(720,100)

                    self.screen.blit(self.backImage, (900,500))
                    self.backButton = self.backImage.get_rect()
                    self.backButton.move_ip(900,500)

                    self.level1Time = self.resultFont.render(str(self.highScores[0].rstrip('\n')) + 's',False,(0,0,0))
                    self.screen.blit(self.level1Time, (195,420))
                    self.level2Time = self.resultFont.render(str(self.highScores[1].rstrip('\n')) + 's',False,(0,0,0))
                    self.screen.blit(self.level2Time, (325,420))
                    self.level3Time = self.resultFont.render(str(self.highScores[2].rstrip('\n')) + 's',False,(0,0,0))
                    self.screen.blit(self.level3Time, (460,420))
                    self.level4Time = self.resultFont.render(str(self.highScores[3].rstrip('\n')) + 's',False,(0,0,0))
                    self.screen.blit(self.level4Time, (590,420))
                    self.level5Time = self.resultFont.render(str(self.highScores[4].rstrip('\n')) + 's',False,(0,0,0))
                    self.screen.blit(self.level5Time, (720,420))

                if self.gameState == 2:
                    self.screen.blit(self.instructions, (0,0))
                    self.screen.blit(self.backImage, (900,0))
                    self.backButton = self.backImage.get_rect()
                    self.backButton.move_ip(900,0)
                    
                if self.gameState == 3 or self.gameState == 5 or self.gameState == 7 or self.gameState == 9 or self.gameState == 11:

                    self.screen.blit(self.newPlatformImage, (950,25))
                    self.newPlatformButton = self.newPlatformImage.get_rect()
                    self.newPlatformButton.move_ip(950,25)

                    self.screen.blit(self.backImage, (925,500))
                    self.backButton = self.backImage.get_rect()
                    self.backButton.move_ip(925,500)

                    self.screen.blit(self.binImage, (960,100))
                    self.binButton = self.binImage.get_rect()
                    self.binButton.move_ip(960,100)

                    self.screen.blit(self.ballDropImage,(950,175))
                    self.ballDropButton = self.backImage.get_rect()
                    self.ballDropButton.move_ip(950,175)

                    #self.levelTime = self.timeOfFinish-self.timeOfDrop
                    #print(self.timeOfFinish)
                    
                
                if self.gameState == 7:
                    self.screen.blit(self.wormholeImage, (300,200))
                    self.wormholeRect = self.wormholeImage.get_rect()
                    self.wormholeRect.move_ip(300,200)

                    self.screen.blit(self.wormholeImage2, (550,75))
                    self.wormholeRect2 = self.wormholeImage2.get_rect()
                    self.wormholeRect2.move_ip(550,75)
                    #pygame.draw.rect(self.screen,(0,0,0),self.wormholeRect)

                if self.gameState == 9:
                    for ball in self.balls:
                        if ball.body.position.x > 512:
                            self.space.gravity = (0,-900)
                        else:
                            self.space.gravity = (0,900)
                        
                if self.gameState == 11:
                    body = self.body
                    currentTime = 0
                    checkPosition = 10
                    newPlanetX = 0
                    newPlanetY = 0
                    oldPlanetX = body.position.x
                    oldPlanetY = body.position.y
                    planetVelocity = (0)

                    self.body.apply_impulse_at_local_point((-50,20),(0,0))

                    distanceToBlackHole = math.sqrt((500 - body.position.x)**2 + (300 - body.position.y)**2)

                    dx = 500 - body.position.x
                    dy = 300 - body.position.y
                    v1 = pymunk.Vec2d(dx,dy)
                    nv = v1.normalized()
                    nv = nv.scale_to_length(100000/(v1.length**2)+5000)
                    body.velocity *= 0.98

                    self.space.gravity = (nv)

                    if pygame.time.get_ticks() > checkPosition:
                        newPlanetX = body.position.x
                        newPlanetY = body.position.y
                        planetVelocity = math.sqrt((newPlanetX-oldPlanetX)**2 + (newPlanetY-oldPlanetY)**2)
                        newPlanetX = oldPlanetX
                        newPlanetY = oldPlanetY
                        checkPosition += 10
                        
                    normalTime = pygame.time.get_ticks()/1000 - self.timeOfDrop/1000
                    #print('normal time to stationary observer:')
                    #print(normalTime)
                    dilationFactorGravity = (1-(2*(6.674e-11)*(1.7901e31))/(v1.length*1000*((2.9979e8)**2)))**0.5        #gravitational constant: 6.67e-11, mass of black hole: 1.7901e+31kg, 
                    timeDilation = dilationFactorGravity * normalTime
                    #print('time relative to traveling observer:')
                    #print(timeDilation)
                    #dilatedTime += (datetime.utcnow() - lastTime).total_seconds() * (v1.length/480)
                    #lastTime = datetime.utcnow()
                    #print(datetime.utcnow())
                    if self.balls:
                        self.normalTime = self.myfont.render('Normal Time: ' + str(round(normalTime, 2)) + 's',False,(0,0,0))
                        self.screen.blit(self.normalTime, (25,500))
                        self.dilatedtime = self.myfont.render('Dilated Time: ' + str(round(timeDilation, 2)) + 's',False,(0,0,0))
                        self.screen.blit(self.dilatedtime, (25,550))
                    #print(self.timeOfDrop)               
                if self.gameState == 4:                 
                    self.screen.blit(self.winImage,(162,95))

                    if len(self.platformList) < 3:
                        self.screen.blit(self.stars3Image,(400,205))
                    if len(self.platformList) > 2 and len(self.platformList) < 5:
                        self.screen.blit(self.stars2Image,(400,205))
                    if len(self.platformList) > 4:
                        self.screen.blit(self.star1Image,(400,205))

                    self.screen.blit(self.backImage, (740,280))
                    self.backButton = self.backImage.get_rect()
                    self.backButton.move_ip(740,280)

                    self.textSurface = self.myfont.render(str(self.initialLevelTime) + ' s',False,(0,0,0))
                    self.screen.blit(self.textSurface, (500,280))
                    
                    pygame.display.flip()

                pygame.display.flip()
                

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if self.gameState == 4:
                    if self.backButton.collidepoint(pygame.mouse.get_pos()):
                        self.clearLevel()
                        self.timesList.clear()
                        self.gameState = 1
                        continue
                        
                if self.gameState == 6:
                    if self.backButton.collidepoint(pygame.mouse.get_pos()):
                        self.clearLevel()
                        self.gameState = 1
                        continue

                if self.gameState == 3 or self.gameState == 5 or self.gameState == 7 or self.gameState == 9 or self.gameState == 11:
                    if self.backButton.collidepoint(pygame.mouse.get_pos()):
                        self.clearLevel()
                        self.gameState = 1
                        self.platformList.clear()

                    if not self.balls or self.gameState == 9:
                        if self.newPlatformButton.collidepoint(pygame.mouse.get_pos()):
                            self.create_Platform()
                        
                        elif self.binButton.collidepoint(pygame.mouse.get_pos()):
                            if self.active_shape is not None:
                                self.removePlatform()
                        elif self.ballDropButton.collidepoint(pygame.mouse.get_pos()):
                            self.create_ball()  
                            self.timeOfDrop = pygame.time.get_ticks() 
                                                   

                        self.mouse_x, self.mouse_y = event.pos
                        nearestShape = self.space.point_query_nearest(event.pos, float("inf"), pymunk.ShapeFilter())
                        if nearestShape is not None:
                            shape = nearestShape.shape
                            #if shape is not None and isinstance(shape, pymunk.Segment) and shape not in self.binList and shape not in self.dropperList and shape not in self.spikesList and shape not in self.walls and shape not in self.pendulumObjects:  
                            if shape is not None and isinstance(shape, pymunk.Segment) and shape in self.platformList:  

                                self.active_shape = shape
                                self.dragging = True
                                self.mouseMotion(event)
                    

                elif self.gameState == 0:
                    if self.startButton.collidepoint(pygame.mouse.get_pos()):
                        self.gameState = 1   
                    if self.settingsButton.collidepoint(pygame.mouse.get_pos()):
                        self.gameState = 2
                    if self.quitButton.collidepoint(pygame.mouse.get_pos()):
                        self.running = False

                
                elif self.gameState == 1:
                    if self.level1Button.collidepoint(pygame.mouse.get_pos()):
                        self.gameState = 3
                        self.setUpLevel1()
                    if self.level2Button.collidepoint(pygame.mouse.get_pos()):
                        self.gameState = 5
                        self.setUpLevel2()
                    if self.level3Button.collidepoint(pygame.mouse.get_pos()):
                        self.gameState = 7
                        self.setUpLevel3()
                    if self.level4Button.collidepoint(pygame.mouse.get_pos()):
                        self.gameState = 9
                        self.setUpLevel4()
                    if self.level5Button.collidepoint(pygame.mouse.get_pos()):
                        self.gameState = 11
                        self.setUpLevel5()
                    
                    if self.backButton.collidepoint(pygame.mouse.get_pos()):
                        self.gameState = 0
                
                elif self.gameState == 2:
                    if self.backButton.collidepoint(pygame.mouse.get_pos()):
                        self.gameState = 0
             
            elif event.type == pygame.KEYDOWN:
                if self.gameState == 3 or self.gameState == 5 or self.gameState == 7 or self.gameState == 9 or self.gameState == 11:
                    if event.key == pygame.K_LEFT:
                        if self.active_shape:
                            self.active_shape.rotation += 0.2
                            self.rotatePlatform()

                    if event.key == pygame.K_RIGHT:
                        if self.active_shape:
                            self.active_shape.rotation -= 0.2
                            self.rotatePlatform() 

                    if event.key == pygame.K_w:
                        if self.active_shape:
                            self.space.remove(self.active_shape)
                            self.platformList.remove(self.active_shape)
                            if self.active_shape is not None:
                                self.active_shape.body.position = (self.active_shape.body.position.x, self.active_shape.body.position.y-10)
                            self.space.add(self.active_shape)
                            self.platformList.append(self.active_shape)  
                    if event.key == pygame.K_s:
                        if self.active_shape:
                            self.space.remove(self.active_shape)
                            self.platformList.remove(self.active_shape)
                            if self.active_shape is not None:
                                self.active_shape.body.position = (self.active_shape.body.position.x, self.active_shape.body.position.y+10)
                            self.space.add(self.active_shape)
                            self.platformList.append(self.active_shape)       
                    if event.key == pygame.K_d:
                        if self.active_shape:
                            self.space.remove(self.active_shape)
                            self.platformList.remove(self.active_shape)
                            if self.active_shape is not None:
                                self.active_shape.body.position = (self.active_shape.body.position.x + 10, self.active_shape.body.position.y)
                            self.space.add(self.active_shape)
                            self.platformList.append(self.active_shape)  
                    if event.key == pygame.K_a:
                        if self.active_shape:
                            self.space.remove(self.active_shape)
                            self.platformList.remove(self.active_shape)
                            if self.active_shape is not None:
                                self.active_shape.body.position = (self.active_shape.body.position.x - 10, self.active_shape.body.position.y)
                            self.space.add(self.active_shape)
                            self.platformList.append(self.active_shape)                  
            
            elif event.type == pygame.MOUSEMOTION:
                if self.gameState == 3 or self.gameState == 5 or self.gameState == 7 or self.gameState == 9 or self.gameState==11:
                    if self.dragging == True:
                        self.mouseMotion(event)    
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.gameState == 3 or self.gameState == 5 or self.gameState == 7 or self.gameState == 9 or self.gameState == 11:
                    self.dragging = False

             
    def setUpLevel1 (self):
        self.space.gravity = (0,900)
        self.mouse_x = 75
        self.mouse_y = 200
        self.mouseMotionChild()
        
        self.binLeft = pymunk.Segment(self.space.static_body,(790,500),(800,600),2.0)
        self.binRight = pymunk.Segment(self.space.static_body,(870,500),(860,600),2.0)
        self.binBottom = pymunk.Segment(self.space.static_body,(800,600),(860,600),2.0)
        self.binBottom.collision_type = 2      

        self.binList = [self.binLeft, self.binRight,self.binBottom]
        for lines in self.binList:
            lines.elasticity = .9
            lines.friction = 10
            lines.color = pygame.Color(0,0,0)
        
        self.drawDroppers()

        self.space.add(self.binLeft,self.binRight,self.binBottom)

        collInfo = self.space.add_collision_handler(1, 2)
        collInfo.begin = self.caughtTheBall
    
    def setUpLevel2(self):
        self.space.gravity = (0,900)
        self.setUpLevel1()

        self.spike1 = pymunk.Segment(self.space.static_body,(300,300),(400,400),7.0)
        self.spike2 = pymunk.Segment(self.space.static_body,(500,350),(650,300),5.0)
        
        self.spikesList = [self.spike1, self.spike2]

        for spike in self.spikesList:
            spike.color = pygame.Color(255,0,0)
            self.space.add(spike)
            spike.collision_type = 3

        collinfo = self.space.add_collision_handler(1,3)
        collinfo.begin = self.removeBall

    def setUpLevel3(self):
        self.space.gravity = (0,900)
        self.setUpLevel1()

        self.wall1 = pymunk.Segment(self.space.static_body,(500,50),(500,700),5.0)
        self.wormholeLine = pymunk.Segment(self.space.static_body,(340,240),(340,241),2.0)
        
        self.walls = [self.wall1,self.wormholeLine]

        for wall in self.walls:
            self.space.add(wall)
            self.wall1.elasticity= 0.9
            wall.color = pygame.Color(0,0,0)

        self.wormholeLine.collision_type = 4
        
        collInfo = self.space.add_collision_handler(1, 4)
        collInfo.begin = self.teleportTheBall

    def setUpLevel4(self):
        self.space.gravity = (0,900)
        self.mouse_x = 75
        self.mouse_y = 200
        self.mouseMotionChild()
        
        self.binLeftGravity = pymunk.Segment(self.space.static_body,(790,100),(800,0),2.0)
        self.binRightGravity = pymunk.Segment(self.space.static_body,(870,100),(860,0),2.0)
        self.binBottomGravity = pymunk.Segment(self.space.static_body,(800,2),(860,2),2.0)
        self.binBottomGravity.collision_type = 2      

        self.binList = [self.binLeftGravity, self.binRightGravity,self.binBottomGravity]
        for lines in self.binList:
            lines.elasticity = .9
            lines.friction = 10
            lines.color = pygame.Color(200,200,0)
        

        self.drawDroppers()

        self.space.add(self.binLeftGravity,self.binRightGravity,self.binBottomGravity)

        collInfo = self.space.add_collision_handler(1, 2)
        collInfo.begin = self.caughtTheBall

    def setUpLevel5(self):
        self.setUpLevel1()

        #self.space.gravity = (0, 0)
        self.blackHole = pymunk.Circle(self.space.static_body,5,(500,300))
        self.space.add(self.blackHole)
        self.blackHole.color = pygame.Color(0,0,0)

    def drawDroppers (self):
        self.dropperLeft = pymunk.Segment(self.space.static_body,(50,0),(50,50),2.0)
        self.dropperRight = pymunk.Segment(self.space.static_body,(110,0),(110,50),2.0)
        self.dropperList = [self.dropperLeft, self.dropperRight]
        for dropperline in self.dropperList:
            dropperline.color = pygame.Color(0,0,0)
        self.space.add(self.dropperLeft, self.dropperRight)
        
    def mouseMotion (self, event) -> None:
        self.mouse_x, self.mouse_y = event.pos
        self.space.remove(self.active_shape)
        self.platformList.remove(self.active_shape)
        self.mouseMotionChild()
        self.space.add(self.active_shape)
        self.platformList.append(self.active_shape)
    def mouseMotionChild (self):
        if self.active_shape is not None:
            self.active_shape.body.position = (self.mouse_x + self.offset_x - self.linePoint1X,self.mouse_y + self.offset_y - self.linePoint1Y)
           

    def create_Platform (self) -> None:
        self.platformLine = pymunk.Segment(self.space.static_body, (self.linePoint1X, self.linePoint1Y), (self.linePoint2X, self.linePoint2Y), 7.0)
        self.platformLine.elasticity = .9
        self.platformLine.friction = 0.9
        if self.gameState == 9:
            self.platformLine.color = pygame.Color(255,255,0)
        if self.gameState != 9:
            self.platformLine.color = pygame.Color(0,0,0)
        
        self.platformLine.rotation = math.pi/2 # I MADE UP THIS ROTATION VARIABLE AND ASSIGNED IT TO PLATFORM LINE.
        self.space.add(self.platformLine)
        self.platformList.append(self.platformLine)

    def rotatePlatform (self) -> None:
        
        xc = (self.active_shape.a.x + self.active_shape.b.x) / 2
        yc = (self.active_shape.a.y + self.active_shape.b.y) / 2
        xa = xc - math.sin(self.active_shape.rotation)*50
        ya = yc - math.cos(self.active_shape.rotation)*50
        xb = xc + math.sin(self.active_shape.rotation)*50
        yb = yc + math.cos(self.active_shape.rotation)*50
        
        r = self.active_shape.rotation

        self.space.remove(self.active_shape)
        self.platformList.remove(self.active_shape)
        self.active_shape = pymunk.Segment(self.space.static_body, (xa, ya), (xb, yb), 7.0)
        self.active_shape.rotation = r
        if self.gameState == 9:
            self.active_shape.color = pygame.Color(255,255,0)
        if self.gameState != 9:
            self.active_shape.color = pygame.Color(0,0,0)
        
        self.space.add(self.active_shape)
        self.platformList.append(self.active_shape)
        self.active_shape.elasticity = .9
        self.active_shape.friction = 0.9

    def update_balls(self) -> None: 
        for ball in self.balls:
            if ball.body.position.y > 700:
                balls_to_remove = [ball for ball in self.balls if ball.body.position.y > 700]
                for ball in balls_to_remove:
                    self.balls.remove(ball)
                    self.space.remove(ball)
            if ball.body.position.x > 1024:
                balls_to_remove = [ball for ball in self.balls if ball.body.position.x > 1024]
                for ball in balls_to_remove:
                    self.balls.remove(ball)
                    self.space.remove(ball)
            if self.gameState == 11:              
                if ball.body.position.x > 470 and ball.body.position.x < 530 and ball.body.position.y > 270 and ball.body.position.y < 330:
                    self.balls.remove(ball)
                    self.space.remove(ball)
    def create_ball(self) -> None:
        mass = 10
        radius = 25
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self.body = pymunk.Body(mass, inertia)
        self.body.position = 80, -25
        self.circle = pymunk.Circle(self.body, radius, (0, 0))
        self.circle.elasticity = .9
        self.circle.friction = 0.9
        self.space.add(self.body, self.circle)
        self.balls.append(self.circle)
        self.ballsToReset.append(self.circle)
        self.circle.collision_type = 1
        
        
    def caughtTheBall(self, space, arbiter, data):
        self.timeOfFinish = pygame.time.get_ticks()
        self.levelTime = self.timeOfFinish-self.timeOfDrop
        self.timesList.append(self.levelTime)
        self.initialLevelTime = self.timesList[0]
        self.initialLevelTime /= 1000
        
        #print(self.timeOfDrop)
        #print(self.timeOfFinish)
        #print(self.levelTime)

        if self.gameState == 3:
            if self.initialLevelTime < float(self.highScores[0]):
                self.highScores[0] = str(self.initialLevelTime)+'\n'
                with open('highscores.txt','w') as file:
                    file.writelines( self.highScores )
        
        if self.gameState == 5:
            if self.initialLevelTime < float(self.highScores[1]):
                self.highScores[1] = str(self.initialLevelTime)+'\n'
                with open('highscores.txt','w') as file:
                    file.writelines( self.highScores )
        
        if self.gameState == 7:
            if self.initialLevelTime < float(self.highScores[2]):
                self.highScores[2] = str(self.initialLevelTime)+'\n'
                with open('highscores.txt','w') as file:
                    file.writelines( self.highScores )
        
        if self.gameState == 9:
            self.space.gravity = (0,900)
            if self.initialLevelTime < float(self.highScores[3]):
                self.highScores[3] = str(self.initialLevelTime)+'\n'
                with open('highscores.txt','w') as file:
                    file.writelines( self.highScores )

        if self.gameState == 11:
            if self.initialLevelTime < float(self.highScores[4]):
                self.highScores[4] = str(self.initialLevelTime)+'\n'
                with open('highscores.txt','w') as file:
                    file.writelines( self.highScores )

        s1 = arbiter.shapes
        self.gameState = 4
        return True

    def removePlatform(self):
        if self.platformList:
            if self.active_shape:
                self.space.remove(self.active_shape)
                self.platformList.remove(self.active_shape)
    
    def removeBall(self, space, arbiter, data):

        s1 = arbiter.shapes
        for ball in self.balls:
            self.space.remove(ball)
        return True
    
    def teleportTheBall(self, space, arbiter, data):
        s1 = arbiter.shapes
        if self.balls:
            for ball in self.balls:
                ball.body.position = (590,115)
        return True

    def clearLevel(self):
        for line in self.binList:
            self.space.remove(line)
        for lines2 in self.dropperList:
            self.space.remove(lines2)
        if self.walls is not None:
            for wall in self.walls:
                self.space.remove(wall)
            self.walls.clear()
        if self.platformList:
            for platform in self.platformList:
                self.space.remove(platform)
            self.platformList.clear()
        if self.spikesList:
            for spike in self.spikesList:
                self.space.remove(spike)
            self.spikesList.clear()
        if self.balls:
            for ball in self.balls:
                self.space.remove(ball)
            self.balls.clear()
        if self.pendulumObjects:
            for objects in self.pendulumObjects:
                self.space.remove(objects)
            self.pendulumObjects.clear()
        if self.gameState == 11:
            self.space.remove(self.blackHole)


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