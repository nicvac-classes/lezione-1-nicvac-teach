import pygame
import pymunk
import sys
import random
import math

# ============================================================
# COSTANTI
# ============================================================
WIDTH, HEIGHT = 600, 700
FPS = 60

# Colori del gioco
RED    = (220, 50, 50)
GREEN  = (50, 200, 50)
BLUE   = (50, 100, 220)
YELLOW = (240, 220, 50)
DARK_BG = (30, 30, 50)

COLORS = [RED, GREEN, BLUE, YELLOW]

# Canestro
BASKET_CENTER = (WIDTH // 2, HEIGHT - 150)
BASKET_RADIUS = 29  # proporzionato alla pallina come NBA (rim/ball ≈ 1.9)

# Pallina
BALL_RADIUS = 15
BALL_START_Y = 50
ROTATION_SPEED = math.pi / 20  # rad/frame – 90° in ~0.17 s

# ============================================================
# INIZIALIZZAZIONE
# ============================================================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Basket")
clock = pygame.time.Clock()

# Spazio fisico
space = pymunk.Space()
space.gravity = (0, 400)

# ============================================================
# FUNZIONI DI DISEGNO
# ============================================================
def create_basket_surface(radius, colors):
    """Crea una superficie con il canestro disegnato una sola volta."""
    size = radius * 2 + 2
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = (size // 2, size // 2)
    rect = pygame.Rect(0, 0, radius * 2, radius * 2)
    rect.center = center

    for i in range(4):
        start_angle = i * math.pi / 2 + math.pi / 4
        end_angle = (i + 1) * math.pi / 2 + math.pi / 4
        pygame.draw.arc(surf, colors[i], rect, start_angle, end_angle, 8)

    # Interno del canestro
    pygame.draw.circle(surf, DARK_BG, center, radius - 8)
    return surf


def draw_basket(surface, body, basket_surf):
    """Ruota la superficie pre-disegnata in base all'angolo del body e la disegna."""
    angle_deg = math.degrees(body.angle)
    rotated = pygame.transform.rotate(basket_surf, angle_deg)
    rect = rotated.get_rect(center=(int(body.position.x), int(body.position.y)))
    surface.blit(rotated, rect)

# ============================================================
# FUNZIONI DI GIOCO
# ============================================================
def create_ball():
    """Crea una pallina con colore casuale che cade dall'alto."""
    color = random.choice(COLORS)
    x = BASKET_CENTER[0]
    mass = 1
    moment = pymunk.moment_for_circle(mass, 0, BALL_RADIUS)
    body = pymunk.Body(mass, moment)
    body.position = (x, BALL_START_Y)
    shape = pymunk.Circle(body, BALL_RADIUS)
    shape.elasticity = 0.7
    shape.friction = 0.5
    shape.collision_type = 1
    space.add(body, shape)
    return {"body": body, "shape": shape, "color": color}


def remove_ball(ball):
    """Rimuove la pallina dallo spazio fisico."""
    space.remove(ball["shape"], ball["body"])


def reset_ball():
    """Rimuove la pallina corrente e ne crea una nuova."""
    global ball, caught, missed
    remove_ball(ball)
    ball = create_ball()
    caught = False
    missed = False

# ============================================================
# CANESTRO FISICO
# ============================================================
basket_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
basket_body.position = BASKET_CENTER

# Sensore unico per rilevare la collisione con la pallina
basket_sensor = pymunk.Circle(basket_body, BASKET_RADIUS)
basket_sensor.sensor = True
basket_sensor.collision_type = 2

space.add(basket_body, basket_sensor)

# Superficie del canestro (disegnata una sola volta)
basket_surface = create_basket_surface(BASKET_RADIUS, COLORS)

# ============================================================
# COLLISION HANDLER
# ============================================================
caught = False
missed = False
target_rotation_angle = 0.0
basket_top_index = 0  # indice del colore in alto nel canestro
basket_top_color = COLORS[basket_top_index]

def on_ball_enter_basket(arbiter, space, data):
    """Callback: la pallina ha toccato il sensore del canestro."""
    global caught, missed
    if caught or missed:
        return True
    if ball["color"] == basket_top_color:
        caught = True
        ball["body"].velocity = (0, 80)   # rallenta la pallina
    else:
        missed = True
        # Rimbalza la pallina lateralmente
        direction = random.choice([-1, 1])
        ball["body"].velocity = (direction * 300, -350)
    return False

space.on_collision(1, 2, begin=on_ball_enter_basket)

# ============================================================
# CREA LA PRIMA PALLINA
# ============================================================
ball = create_ball()

# ============================================================
# GAME LOOP
# ============================================================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                target_rotation_angle += math.pi / 2
                basket_body.angular_velocity = ROTATION_SPEED * FPS
                basket_top_index = (basket_top_index - 1) % 4
                basket_top_color = COLORS[basket_top_index]
            elif event.key == pygame.K_RIGHT:
                target_rotation_angle -= math.pi / 2
                basket_body.angular_velocity = -ROTATION_SPEED * FPS
                basket_top_index = (basket_top_index + 1) % 4
                basket_top_color = COLORS[basket_top_index]

    screen.fill(DARK_BG)

    # --- Rotazione smooth via pymunk ---
    if basket_body.angular_velocity != 0:
        diff = target_rotation_angle - basket_body.angle
        if abs(diff) <= ROTATION_SPEED:
            basket_body.angle = target_rotation_angle
            basket_body.angular_velocity = 0

    # --- Logica di gioco ---
    if caught:
        # La pallina continua a cadere; quando supera il centro del canestro, reset
        by = ball["body"].position.y
        if by >= BASKET_CENTER[1]:
            reset_ball()
    elif missed:
        # Aspetta che la pallina esca dallo schermo, poi crea una nuova
        bx, by = ball["body"].position
        if by > HEIGHT + 50 or bx < -50 or bx > WIDTH + 50:
            reset_ball()
    else:
        # Pallina uscita dallo schermo senza toccare il canestro
        bx, by = ball["body"].position
        if by > HEIGHT + 50:
            reset_ball()

    # --- Disegno ---
    draw_basket(screen, basket_body, basket_surface)
    pos = ball["body"].position
    pygame.draw.circle(screen, ball["color"],
                       (int(pos.x), int(pos.y)), BALL_RADIUS)

    space.step(1 / FPS)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()