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
        self.lineID
        self.dragging = False
        self.activePlatform = 0
        self.rotating = False
        self.lineAngle = math.pi/2

        
        
        

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
        static_body = self.space.static_body

        self.linePoint1X = 0
        self.linePoint1Y = 0
        self.linePoint2X = 100
        self.linePoint2Y = 0

        self.platformLine = pymunk.Segment(static_body, (self.linePoint1X, self.linePoint1Y), (self.linePoint2X, self.linePoint2Y), 7.0)
        self.platformLine.elasticity = 1
        self.platformLine.friction = 0.9
        
        self.space.add(self.platformLine)
        self.lineID = self.space.shapes[0]._id


    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
                

            elif event.type == pygame.MOUSEBUTTONDOWN:
                #self.dragging = True
                self.mouse_x, self.mouse_y = event.pos
                p = from_pygame(event.pos, self.screen)
                self.active_shape = None
                for s in self.space.shapes:
                    if s._id == self.lineID:
                        
                        dist = s.point_query(p)
                        if dist.distance < 0:
                            self.active_shape = s
                            #print(event.pos)
                            self.dragging = True
                            self.activePlatform = self.active_shape._id

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.active_shape:
                        self.lineAngle += 0.2

                if event.key == pygame.K_RIGHT:
                    if self.active_shape:
                        self.lineAngle -= 0.2

                self.rotatePlatform()
                                                    
            
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging == True:
                    self.mouse_x, self.mouse_y = event.pos
                    self.space.remove(self.platformLine)
                    self.platformLine.body.position = (self.mouse_x + self.offset_x,self.mouse_y + self.offset_y)
                    self.space.add(self.platformLine)
                    self.lineID = self.space.shapes[0]._id
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False


    def rotatePlatform (self) -> None:
        
        xc = (self.platformLine.a.x + self.platformLine.b.x) / 2
        yc = (self.platformLine.a.y + self.platformLine.b.y) / 2
        xa = xc - math.sin(self.lineAngle)*50
        ya = yc - math.cos(self.lineAngle)*50
        xb = xc + math.sin(self.lineAngle)*50
        yb = yc + math.cos(self.lineAngle)*50
        
        self.space.remove(self.platformLine)
        self.platformLine = pymunk.Segment(self.space.static_body, (xa, ya), (xb, yb), 7.0)
        self.space.add(self.platformLine)
        self.lineID = self.space.shapes[0]._id
        self.platformLine.elasticity = .9
        self.platformLine.friction = 0.9


    def update_balls(self) -> None:            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
                self.create_ball()
            
        balls_to_remove = [ball for ball in self.balls if ball.body.position.y > 500]
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
        shape.elasticity = 1
        shape.friction = 0.9
        self.space.add(body, shape)
        self.balls.append(shape)


    def clear_screen(self) -> None:
        self.screen.fill(pygame.Color("white"))

    def draw_objects(self) -> None:
        self.space.debug_draw(self.draw_options)

        if self.active_shape != None:
            s = self.active_shape
            r = int(s.radius)
            p = to_pygame(s.a, self.screen)
            pygame.draw.circle(self.screen, (255,0,0), p, r, 3)

        
if __name__ == "__main__":
    
    game = BouncingBalls()
    game.run()