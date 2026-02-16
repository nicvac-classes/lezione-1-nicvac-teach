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
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
DARK_BG = (30, 30, 50)

COLORS = [RED, GREEN, BLUE, YELLOW]

# Canestro
BASKET_CENTER = (WIDTH // 2, HEIGHT - 150)
BASKET_RADIUS = 29  # proporzionato alla pallina come NBA (rim/ball ≈ 1.9)

# Pallina
BALL_RADIUS = 15
BALL_START_Y = 50
ROTATION_SPEED = math.pi / 20  # rad/frame – 90° in ~0.33 s

# ============================================================
# INIZIALIZZAZIONE
# ============================================================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Basket")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 36)
font_big = pygame.font.SysFont(None, 72)

# Spazio fisico
space = pymunk.Space()
space.gravity = (0, 400)

# ============================================================
# FUNZIONI DI DISEGNO
# ============================================================
def draw_basket(surface, center, radius, colors, rotation_angle):
    """Disegna il canestro con 4 spicchi colorati (spicchio 1 centrato in alto)."""
    cx, cy = center
    rect = pygame.Rect(cx - radius, cy - radius, radius * 2, radius * 2)

    for i in range(4):
        start_angle = i * math.pi / 2 - math.pi / 4 + rotation_angle
        end_angle = (i + 1) * math.pi / 2 - math.pi / 4 + rotation_angle
        pygame.draw.arc(surface, colors[i],
                        rect, start_angle, end_angle, 8)

    # Interno nero del canestro
    pygame.draw.circle(surface, DARK_BG, center, radius - 8)


def draw_hud(surface, score, lives):
    """Disegna il punteggio e le vite."""
    score_text = font.render(f"Punti: {score}", True, WHITE)
    lives_text = font.render(f"Vite: {'❤' * lives}", True, WHITE)
    surface.blit(score_text, (10, 10))
    surface.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))


def draw_game_over(surface, score):
    """Disegna la schermata di Game Over."""
    go_text = font_big.render("GAME OVER", True, RED)
    score_text = font.render(f"Punteggio finale: {score}", True, WHITE)
    restart_text = font.render("Premi R per ricominciare", True, WHITE)

    surface.blit(go_text,
        (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 80))
    surface.blit(score_text,
        (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    surface.blit(restart_text,
        (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

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


def lerp_color(color, target, progress):
    """Interpola linearmente tra due colori."""
    r = int(color[0] + (target[0] - color[0]) * progress)
    g = int(color[1] + (target[1] - color[1]) * progress)
    b = int(color[2] + (target[2] - color[2]) * progress)
    return (max(0, min(255, r)),
            max(0, min(255, g)),
            max(0, min(255, b)))


def get_top_color(rotation_angle):
    """Restituisce il colore dello spicchio in alto del canestro."""
    beta = (3 * math.pi / 4 - rotation_angle) % (2 * math.pi)
    index = int(beta / (math.pi / 2)) % 4
    return COLORS[index]


def reset_ball():
    """Rimuove la pallina corrente e ne crea una nuova."""
    global ball, caught, missed, fade_timer
    remove_ball(ball)
    ball = create_ball()
    caught = False
    missed = False
    fade_timer = 0


def reset_game():
    """Resetta tutto il gioco."""
    global ball, score, lives, rotation_angle, target_rotation_angle, game_over
    global caught, missed, fade_timer
    try:
        remove_ball(ball)
    except:
        pass
    score = 0
    lives = 3
    rotation_angle = 0.0
    target_rotation_angle = 0.0
    game_over = False
    caught = False
    missed = False
    fade_timer = 0
    ball = create_ball()

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

# ============================================================
# COLLISION HANDLER
# ============================================================
score = 0
lives = 3
caught = False
missed = False
fade_timer = 0
fade_duration = 30
game_over = False
rotation_angle = 0.0
target_rotation_angle = 0.0

def on_ball_enter_basket(arbiter, space, data):
    """Callback: la pallina ha toccato il sensore del canestro."""
    global caught, missed
    if caught or missed:
        return True
    top_color = get_top_color(rotation_angle)
    if ball["color"] == top_color:
        caught = True
        ball["catch_pos"] = tuple(ball["body"].position)
        return False  # lascia passare la pallina
    else:
        missed = True
        # Lancia la pallina via lateralmente
        direction = random.choice([-1, 1])
        ball["body"].velocity = (direction * 400, -300)
        return False  # non bloccare, lascia volare via

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
            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
            else:
                if event.key == pygame.K_LEFT:
                    target_rotation_angle += math.pi / 2
                elif event.key == pygame.K_RIGHT:
                    target_rotation_angle -= math.pi / 2

    screen.fill(DARK_BG)

    # --- Rotazione smooth a velocità costante ---
    if rotation_angle != target_rotation_angle:
        diff = target_rotation_angle - rotation_angle
        if abs(diff) <= ROTATION_SPEED:
            rotation_angle = target_rotation_angle
        elif diff > 0:
            rotation_angle += ROTATION_SPEED
        else:
            rotation_angle -= ROTATION_SPEED

    if game_over:
        draw_game_over(screen, score)
    else:
        # --- Logica di gioco ---
        if caught:
            fade_timer += 1
            progress = min(fade_timer / fade_duration, 1.0)
            # Posizione: interpolazione lineare dalla posizione di cattura al centro canestro
            sx, sy = ball["catch_pos"]
            cx, cy = BASKET_CENTER
            ball["body"].velocity = (0, 0)
            ball["body"].position = (
                sx + (cx - sx) * progress,
                sy + (cy - sy) * progress
            )
            # Colore: dissolvi verso sfondo
            ball["draw_color"] = lerp_color(ball["color"], DARK_BG, progress)
            # Raggio: rimpicciolisci
            ball["draw_radius"] = max(1, int(BALL_RADIUS * (1 - progress)))
            if fade_timer >= fade_duration:
                score += 1
                reset_ball()
        elif missed:
            # Aspetta che la pallina esca dallo schermo prima di togliere vita
            bx, by = ball["body"].position
            if by > HEIGHT + 50 or bx < -50 or bx > WIDTH + 50:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    reset_ball()
        else:
            bx, by = ball["body"].position
            if by > HEIGHT + 50 or bx < -50 or bx > WIDTH + 50:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    reset_ball()

        # --- Disegno ---
        draw_basket(screen, BASKET_CENTER, BASKET_RADIUS, COLORS, rotation_angle)
        if not game_over:
            draw_color = ball.get("draw_color", ball["color"])
            draw_radius = ball.get("draw_radius", BALL_RADIUS)
            pos = ball["body"].position
            pygame.draw.circle(screen, draw_color,
                               (int(pos.x), int(pos.y)), draw_radius)
        draw_hud(screen, score, lives)

    space.step(1 / FPS)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()