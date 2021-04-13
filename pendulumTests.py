import pygame
import pymunk
import pymunk.pygame_util

pygame.init()
space = pymunk.Space() 
space.gravity = 0, 10
screen = pygame.display.set_mode([1000, 600])
draw_options = pymunk.pygame_util.DrawOptions(screen)


b0 = space.static_body 
segment = pymunk.Segment(b0, (0, 600), (640, 600), 4)
segment.elasticity = 1

body = pymunk.Body(mass=1, moment=10)
body.position = (100, 100)
circle = pymunk.Circle(body, radius=20)

body2 = pymunk.Body(mass=1, moment=10)
body2.position = (0,100)
circle2 = pymunk.Circle(body2, radius=20)

joint = pymunk.constraints.PinJoint(b0, body, (200, 200))
joint2 = pymunk.constraints.PinJoint(body2,body)

space.add(body, circle, segment, joint,body2,joint2,circle2)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            print('yes')
            space.remove(body,circle,segment,joint,body2,joint2,circle2)

    screen.fill((255,255,255))
    space.debug_draw(draw_options)
    pygame.display.update()
    space.step(0.01)

pygame.quit()