import pygame
import pymunk
import pymunk.pygame_util
import random
import sys

def create_ball(pos):
    # Pallina - body
    mass = 1                                          
    radius = random.randint(10, 40)                                       
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

# Rampa inclinata
ramp = pymunk.Segment(space.static_body, (0, 400), (300, 500), 5)  # 🆕
ramp.elasticity = 0.8                                              # 🆕
ramp.friction = 0.5                                                # 🆕
space.add(ramp)                                                    # 🆕

# Parete sinistra
left_wall = pymunk.Segment(space.static_body, (0, 0), (0, 600), 5)   # 🆕
left_wall.elasticity = 0.8                                           # 🆕
left_wall.friction = 0.5                                             # 🆕
space.add(left_wall)                                                 # 🆕

# Parete destra
right_wall = pymunk.Segment(space.static_body, (800, 0), (800, 600), 5)  # 🆕
right_wall.elasticity = 0.8                                              # 🆕
right_wall.friction = 0.5                                                # 🆕
space.add(right_wall)                                                    # 🆕

# Renderer
draw_options = pymunk.pygame_util.DrawOptions(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            ball = create_ball(event.pos)
            balls.append( ball )

        if event.type == pygame.KEYDOWN:              # 🆕
                    if event.key == pygame.K_UP:              # 🆕
                        space.gravity = (0, -900)             # 🆕
                    if event.key == pygame.K_DOWN:            # 🆕
                        space.gravity = (0, 900)              # 🆕
                    if event.key == pygame.K_LEFT:            # 🆕
                        space.gravity = (-900, 0)             # 🆕
                    if event.key == pygame.K_RIGHT:           # 🆕
                        space.gravity = (900, 0)              # 🆕

        if event.type == pygame.KEYDOWN:              # 🆕
                    if event.key == pygame.K_SPACE:           # 🆕
                        for shape in balls:                   # 🆕
                            space.remove(shape.body, shape)   # 🆕
                        balls.clear()                         # 🆕

    screen.fill((30, 30, 50))
    space.debug_draw(draw_options)

    space.step(1/60)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()