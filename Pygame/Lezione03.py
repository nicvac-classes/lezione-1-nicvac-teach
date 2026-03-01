import pygame
import pymunk
import sys
import random
import math

# ============================================================
# COSTANTI
# ============================================================
# Dimensione dell'area di gioco e FPS
WIDTH, HEIGHT = 600, 700
FPS = 60

# Colori usati per disegnare gli oggetti
RED    = (220, 50, 50)
GREEN  = (50, 200, 50)
BLUE   = (50, 100, 220)
YELLOW = (240, 220, 50)
DARK_BG = (30, 30, 50)

# I colori del canestro e della palla
COLORS = [RED, GREEN, BLUE, YELLOW]

# Palla
BALL_RADIUS = 15
BALL_START_Y = 50

# Canestro
BASKET_CENTER = (WIDTH // 2, HEIGHT - 150)
BASKET_RADIUS = BALL_RADIUS * 1.9  # proporzionato alla pallina come NBA (rim/ball ≈ 1.9)
BASKET_ROTATION_STEP = math.pi / 20  # rad/frame – Quanto deve ruotare per ogni frame

# Gestione delle Collisioni
# Uso la notazione binaria per comodità gestione collisioni
COLLISION_TYPE_BALL = 0b01
COLLISION_TYPE_BASKET = 0b10

# ============================================================
# INIZIALIZZAZIONE
# ============================================================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Basket")
clock = pygame.time.Clock()

# Spazio fisico
space = pymunk.Space()
space.gravity = (0, 500)

# ============================================================
# Creazione e disegno degli oggetti
# ============================================================

# Canestro
def create_basket():
    # DISEGNO
    # Creo la superficie di disegno dell'oggetto
    size = BASKET_RADIUS * 2
    center = (size//2, size//2)
    basket_surface = pygame.Surface((size,size), pygame.SRCALPHA) # sfondo trasparente
    # Disegna il canestro con i 4 colori, il primo colore in alto
    #L'angolo 0 è alle ore 15:00 e cresce in senso antiorario
    angle_step = math.pi/2 # 90 gradi
    angle_start = math.pi/4 # Parto da 45 gradi
    angle_stop  = angle_start + angle_step
    for i in range(4):
        pygame.draw.arc(basket_surface, COLORS[i], basket_surface.get_rect(), angle_start, angle_stop, 8 )
        angle_start = angle_stop
        angle_stop += angle_step
    # Interno del canestro
    pygame.draw.circle(basket_surface, DARK_BG, center, BASKET_RADIUS - 8)

    # BODY
    # Definiamo il Body del canestro (oggetto fisico)
    # KINEMATIC: non soggetto alla gravità, interagisce con gli altri body
    basket_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    basket_body.position = BASKET_CENTER

    # SHAPE
    # Definiamo la forma fisica
    basket_shape = pymunk.Circle(basket_body, BASKET_RADIUS)
    basket_shape.elasticity = 0.4
    basket_shape.collision_type = COLLISION_TYPE_BASKET
    # mask: oggetti con cui interagire fisicamente
    basket_shape.filter = pymunk.ShapeFilter(categories=COLLISION_TYPE_BASKET,
                                             mask=COLLISION_TYPE_BALL)

    # Aggiungo il canestro allo spazio fisico
    space.add(basket_body, basket_shape)

    return {"body": basket_body, "shape": basket_shape, "surface": basket_surface}


def draw_basket(screen, basket):
    """Ruota la superficie pre-disegnata in base all'angolo del body e la disegna."""
    basket_body = basket["body"]
    basket_surface = basket["surface"]
    # Ridisegno il canestro, considerando la rotazione corrente di basket_body
    angle_deg = math.degrees(basket_body.angle) # da radianti a gradi
    surface_rotated = pygame.transform.rotate(basket_surface, angle_deg)
    # Calcolo il nuovo riquadro da disegnare
    rect_new = surface_rotated.get_rect(center=basket_body.position)
    # Scrivo la surface ridisegnata nel nuovo riquadro
    screen.blit(surface_rotated, rect_new)

# Palla
def create_ball():
    """Crea una pallina con colore casuale che cade dall'alto."""
    # DISEGNO
    # Creo la superficie di disegno dell'oggetto
    size = BALL_RADIUS * 2
    center = (size//2, size//2)
    ball_surface = pygame.Surface((size,size), pygame.SRCALPHA)
    # Disegno la palla con un colore random
    color = random.choice(COLORS)
    pygame.draw.circle(ball_surface, color, center, BALL_RADIUS)

    # BODY
    # Definiamo il Body della palla (oggetto fisico)
    # DYNAMIC: soggetto alla gravità, interagisce con gli altri body
    mass = 1
    moment = pymunk.moment_for_circle(mass, 0, BALL_RADIUS)
    ball_body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
    ball_body.position = (BASKET_CENTER[0], BALL_START_Y)

    # SHAPE
    # Definiamo la forma fisica
    ball_shape = pymunk.Circle(ball_body, BALL_RADIUS)
    ball_shape.elasticity = 0.7
    ball_shape.friction = 0.5
    ball_shape.collision_type = COLLISION_TYPE_BALL
    # mask: oggetti con cui interagire fisicamente
    ball_shape.filter = pymunk.ShapeFilter(categories=COLLISION_TYPE_BALL,
                                           mask=COLLISION_TYPE_BALL | COLLISION_TYPE_BASKET)

    # Aggiungo la palla allo spazio fisico
    space.add(ball_body, ball_shape)

    return {"body": ball_body, "shape": ball_shape, "surface": ball_surface, "color": color}

def draw_ball( screen, ball):
    ball_body = ball["body"]
    ball_surface = ball["surface"]
    # Calcolo il nuovo riquadro da disegnare
    rect_new = ball_surface.get_rect(center=ball_body.position)
    # Scrivo la surface nel nuovo riquadro
    screen.blit(ball_surface, rect_new)


def reset_ball(ball):
    """Rimuove la pallina corrente e ne crea una nuova."""
    global caught, missed
    caught = False
    missed = False

    # Rimuove la palla dallo spazio fisico.
    space.remove(ball["shape"], ball["body"])
    # Ritorna la nuova palla
    return create_ball()


# ============================================================
# COLLISION HANDLER
# ============================================================
caught = False # La palla entra nel canestro
missed = False # La palla non entra nel canestro
basket_top_color_index = 0  # indice del colore in alto al canestro
target_rotation_angle = 0.0 # angolo attuale del canestro


def on_ball_enter_basket(arbiter, space, data):
    """Callback: la pallina ha toccato il canestro."""

    # Colore del canestro
    basket_top_color = COLORS[basket_top_color_index]

    global caught, missed
    if caught or missed:
        return True

    if ball["color"] == basket_top_color:
        caught = True
        # Modificando la maschera di collisione, la pallina non interagisce più con il canestro, attraversandolo
        ball["shape"].filter = pymunk.ShapeFilter(categories=COLLISION_TYPE_BALL,
                                                  mask=COLLISION_TYPE_BALL)
        ball["body"].velocity = (0, 80)   # rallenta la pallina
    else:
        missed = True
        # Applico una forza su x per far rimbalzare la pallina lateralmente
        direction = random.choice([-1, 1])
        ball["body"].apply_impulse_at_local_point((direction * 100, 0))

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
                basket_body.angular_velocity = BASKET_ROTATION_STEP * FPS
                basket_top_color_index = (basket_top_color_index - 1) % 4
            elif event.key == pygame.K_RIGHT:
                target_rotation_angle -= math.pi / 2
                basket_body.angular_velocity = -BASKET_ROTATION_STEP * FPS
                basket_top_color_index = (basket_top_color_index + 1) % 4

    screen.fill(DARK_BG)

    # Aggiorno la fisica
    space.step(1 / FPS)

    # --- Rotazione smooth via pymunk ---
    if basket_body.angular_velocity != 0:
        diff = target_rotation_angle - basket_body.angle
        if abs(diff) <= BASKET_ROTATION_STEP:
            basket_body.angle = target_rotation_angle
            basket_body.angular_velocity = 0

    # --- Logica di gioco ---
    if caught:
        # La pallina continua a cadere; quando supera il centro del canestro, reset
        by = ball["body"].position.y
        if by >= BASKET_CENTER[1]:
            ball = reset_ball(ball)
    elif missed:
        # Aspetta che la pallina esca dallo schermo, poi crea una nuova
        bx, by = ball["body"].position
        if by > HEIGHT + 50 or bx < -50 or bx > WIDTH + 50:
            ball = reset_ball(ball)
    else:
        # Pallina uscita dallo schermo senza toccare il canestro
        bx, by = ball["body"].position
        if by > HEIGHT + 50:
            ball = reset_ball(ball)

    # --- Disegno gli oggetti ---
    draw_basket(screen, basket)
    draw_ball(screen, ball)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()