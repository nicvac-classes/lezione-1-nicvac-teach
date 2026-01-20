import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Test Pygame")

clock = pygame.time.Clock()

x, y = 320, 240
speed = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed
    
    screen.fill((30, 30, 50))
    pygame.draw.circle(screen, (255, 100, 100), (x, y), 30)
    pygame.display.flip()

    clock.tick(60)
    
pygame.quit()
sys.exit()
