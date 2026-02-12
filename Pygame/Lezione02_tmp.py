import pygame
import pymunk
import pymunk.pygame_util
import sys

def create_ball(pos):
    # Pallina - body
    mass = 1
    radius = 20
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = pos

    # Pallina - shape
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.9
    shape.friction = 0.5
    space.add(body, shape)
    return shape

balls = []

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test Pymunk - Fisica")
clock = pygame.time.Clock()

# Spazio fisico
space = pymunk.Space()
space.gravity = (0, 900)

# Pavimento
floor = pymunk.Segment(space.static_body, (0, 580), (800, 580), 5)
floor.elasticity = 0.8
floor.friction = 0.5
space.add(floor)

# Renderer
draw_options = pymunk.pygame_util.DrawOptions(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            ball = create_ball(event.pos)
            balls.append(ball)

    screen.fill((30, 30, 50))
    space.debug_draw(draw_options)
    space.step(1/60)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()