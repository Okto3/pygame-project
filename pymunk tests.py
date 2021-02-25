import random
from typing import List
import pygame
import pymunk
import pymunk.pygame_util


class BouncingBalls(object):
    def __init__(self) -> None:
        self._space = pymunk.Space() 
        self._space.gravity = (0.0, 900.0)
        self._dt = 1.0 / 60.0 
        self._physics_steps_per_frame = 1

        pygame.init()                                       
        self._screen = pygame.display.set_mode((1024, 600))
        self._clock = pygame.time.Clock()
        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)
        self._add_static_scenery()
        self._balls: List[pymunk.Circle] = []
        self._running = True
        self._ticks_to_next_ball = 10
        self.mouse_x = 0
        self.mouse_y = 0

    def run(self) -> None:
            while self._running:
                for x in range(self._physics_steps_per_frame):
                    self._space.step(self._dt)

                self._process_events()
                self._update_balls()
                self._clear_screen()
                self._draw_objects()
                pygame.display.flip()
                self._clock.tick(50)
                

    def _add_static_scenery(self) -> None:
        static_body = self._space.static_body
        static_lines = [
            pymunk.Segment(static_body, (50.0, 200), (407.0, 300), 5.0),
            #pymunk.Segment(static_body, (407.0, 600 - 246), (407.0, 600 - 343), 0.0),
        ]
        for line in static_lines:   
            line.elasticity = 0.95
            line.friction = 0.9
        self._space.add(*static_lines)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print('yes')     
                    if static_lines(event.pos):
                        self.mouse_x, self.mouse_y = event.pos
                        print('touching line')


    def _process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(self._screen, "bouncing_balls.png")



    def _update_balls(self) -> None:       
        self._ticks_to_next_ball -= 1      
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
                self._create_ball()
                self._ticks_to_next_ball = 0
            
        balls_to_remove = [ball for ball in self._balls if ball.body.position.y > 500]
        for ball in balls_to_remove:
            self._space.remove(ball, ball.body)
            self._balls.remove(ball)

    def _create_ball(self) -> None:
        mass = 10
        radius = 25
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = 100, 100
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 0.9
        self._space.add(body, shape)
        self._balls.append(shape)
        return

    def _clear_screen(self) -> None:
        self._screen.fill(pygame.Color("white"))

    def _draw_objects(self) -> None:
        self._space.debug_draw(self._draw_options)


if __name__ == "__main__":
    
    game = BouncingBalls()
    game.run()