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
ROTATION_SPEED = math.pi / 20  # rad/frame – 90° in ~0.17 s

# Pallina
BALL_RADIUS = 15
BALL_START_Y = 50

# Collisioni
COLLISION_TYPE_BALL = 1
COLLISION_TYPE_BASKET = 2

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
# Creazione degli oggetti
# ============================================================

# Canestro
def create_basket():
    # Disegna il canestro con i 4 colori, il primo colore in alto
    size = BASKET_RADIUS * 2
    surface = pygame.Surface((size,size), pygame.SRCALPHA) # sfondo trasparente
    center = (size//2, size//2)
    rect = pygame.Rect(0,0,size,size)
    rect.center = center

    angle_start, angle_stop = -math.pi/4, math.pi/4
    angle_step = math.pi/2
    for i in range(4):
        pygame.draw.arc(surface, COLORS[i], rect, angle_start, angle_stop, 8 )
        angle_start = angle_stop
        angle_stop += angle_step

    # Interno del canestro
    pygame.draw.circle(surface, DARK_BG, center, BASKET_RADIUS - 8)

    # Definiamo il Body del canestro (oggetto fisico)
    # KINEMATIC: non soggetto alla gravità
    basket_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC) 
    basket_body.position = BASKET_CENTER

    # Sensore per rilevare la collisione con la pallina
    basket_sensor = pymunk.Circle(basket_body, BASKET_RADIUS)
    basket_sensor.sensor = True
    basket_sensor.collision_type = COLLISION_TYPE_BASKET

    # Aggiungo allo spazio fisico il canestro
    space.add(basket_body, basket_sensor)

    return {"body": basket_body, "surface": surface}


def draw_basket(screen, basket):

    basket_body = basket["body"]
    basket_surf = basket["surface"]

    """Ruota la superficie pre-disegnata in base all'angolo del body e la disegna."""
    angle_deg = math.degrees(basket_body.angle)
    rotated = pygame.transform.rotate(basket_surf, angle_deg)
    rect = rotated.get_rect(center=(int(basket_body.position.x), int(basket_body.position.y)))
    screen.blit(rotated, rect)

# Palla
def create_ball():
    """Crea una pallina con colore casuale che cade dall'alto."""
    #@@@ color = random.choice(COLORS)
    color = RED
    x = BASKET_CENTER[0]
    mass = 1
    moment = pymunk.moment_for_circle(mass, 0, BALL_RADIUS)
    body = pymunk.Body(mass, moment)
    body.position = (x, BALL_START_Y)
    shape = pymunk.Circle(body, BALL_RADIUS)
    shape.elasticity = 0.7
    shape.friction = 0.5
    shape.collision_type = COLLISION_TYPE_BALL
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

space.on_collision(COLLISION_TYPE_BALL, COLLISION_TYPE_BASKET, 
                   begin=on_ball_enter_basket)

# Crea il canestro
basket = create_basket()
# Crea la prima palla
ball = create_ball()

# ============================================================
# GAME LOOP
# ============================================================
basket_body = basket["body"]
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
    
    # Aggiorno la fisica
    space.step(1 / FPS)


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
    draw_basket(screen, basket)
    pos = ball["body"].position
    pygame.draw.circle(screen, ball["color"],
                       (int(pos.x), int(pos.y)), BALL_RADIUS)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()