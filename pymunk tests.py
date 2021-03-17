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
        self.binSpace = pymunk.Space()
        self.space.gravity = (0.0, 900.0)
        self.dt = 1.0 / 60.0 
        self.physics_steps_per_frame = 1

        pygame.init()                                       
        self.screen = pygame.display.set_mode((1024, 600))
        self.clock = pygame.time.Clock()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.add_static_scenery()
        self.balls: List[pymunk.Circle] = []
        self.selected_shapes = []
        self.running = True
        self.ticks_to_next_ball = 10
        self.active_shape = None
        self.dragging = False
        self.rotating = False
        self.platformRotations = []   
        #self.create_bin()
        self.binLeft = pymunk.Segment(self.space.static_body,(500,500),(500,400),1.0)
        self.binRight = pymunk.Segment(self.space.static_body,(600,500),(600,400),1.0)
        self.space.add(self.binLeft,self.binRight)

        
        

    def run(self) -> None:
            while self.running:
                for x in range(self.physics_steps_per_frame):
                    self.space.step(self.dt)

                self.process_events()
                self.update_balls()
                self.clear_screen()
                self.draw_objects()
                
                pygame.display.flip()
                self.clock.tick(50)
                self.offset_x = 0
                self.offset_y = 0
                self.x = 0
                self.y = 0
         

    def add_static_scenery(self) -> None:
        
        self.linePoint1X = 50
        self.linePoint1Y = 100
        self.linePoint2X = 150
        self.linePoint2Y = 100
        

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
                
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = event.pos
                shape = self.space.point_query_nearest(event.pos, float("inf"), pymunk.ShapeFilter()).shape
                if shape is not None and isinstance(shape, pymunk.Segment):
                    if shape != self.binLeft or shape != self.binRight:
                        self.active_shape = shape
                        self.dragging = True
                        self.mouseMotion(event)
                        #print(self.active_shape)

            elif event.type == pygame.KEYDOWN:
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
                if self.dragging == True:
                    self.mouseMotion(event)    
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False


        
    def mouseMotion (self, event) -> None:
        self.mouse_x, self.mouse_y = event.pos
        self.space.remove(self.active_shape)
        self.active_shape.body.position = (self.mouse_x + self.offset_x - self.linePoint1X,self.mouse_y + self.offset_y - self.linePoint1Y)
        self.space.add(self.active_shape)


    def create_Platform (self) -> None:
        static_body = self.space.static_body
        platformLine = pymunk.Segment(static_body, (self.linePoint1X, self.linePoint1Y), (self.linePoint2X, self.linePoint2Y), 7.0)
        platformLine.elasticity = .9
        platformLine.friction = 0.9
        platformLine.rotation = math.pi/2 # I MADE UP THIS ROTATION VARIABLE AND ASSIGNED IT TO PLATFORM LINE.

        self.space.add(platformLine)


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
        self.space.add(self.active_shape)
        self.active_shape.elasticity = .9
        self.active_shape.friction = 0.9


    def update_balls(self) -> None:            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.create_ball()

            
        balls_to_remove = [ball for ball in self.balls if ball.body.position.y > 700]
        for ball in balls_to_remove:
            self.space.remove(ball, ball.body)
            self.balls.remove(ball)

    def create_ball(self) -> None:
        mass = 10
        radius = 25
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = 100, 100
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = .99
        shape.friction = 0.9
        self.space.add(body, shape)
        self.balls.append(shape)

    #def create_bin (self) -> None:
        #static_bodies_bin = self.space.static_body
        #self.bin_lines = [
        

        #]
        #for line in bin_lines:
        #    line.elasticity = 0.95
        #    line.friction = 0.9
        
        #print('yes')
       

    def clear_screen(self) -> None:
        self.screen.fill(pygame.Color("white"))

    def draw_objects(self) -> None:
        self.space.debug_draw(self.draw_options)


        
if __name__ == "__main__":
    game = BouncingBalls()
    game.run()