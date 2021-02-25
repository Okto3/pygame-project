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
                

    def add_static_scenery(self) -> None:
        static_body = self.space.static_body
        
        
        static_lines = [
            pymunk.Segment(static_body, (50.0, 200), (407.0, 300), 5.0)
            #pymunk.Segment(static_body, (407.0, 600 - 246), (407.0, 600 - 343), 0.0),
        ]
        for line in static_lines:   
            line.elasticity = 0.95
            line.friction = 0.9
        self.space.add(*static_lines)
        self.lineID = self.space.shapes[0]._id
        print(self.lineID)


    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

            
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                p = from_pygame(event.pos, self.screen)
                self.active_shape = None
                for s in self.space.shapes:
                    print(s._id)
                    print(self.lineID)
                    if s._id == self.lineID:
                        dist = s.point_query(p)
                        
                        if dist.distance < 0:
                            
                            self.active_shape = s
                            self.pulling = True

                            s.body.angle = (p - s.body.position).angle

                            if pygame.key.get_mods() & KMOD_META:
                                self.selected_shapes.append(s)
                                print(self.selected_shapes)
                            else:
                                self.selected_shapes = [] 

            #keys = {K_LEFT: (-1, 0), K_RIGHT: (1, 0),K_UP: (0, 1), K_DOWN: (0, -1)}
            
                #self.active_shape.body.position += 1
                #print('yes')
                #v = Vec2d(keys[K_LEFT])* 20
                #if self.active_shape != None:
                #    self.active_shape.body.position += v


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
        shape.elasticity = 0.95
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