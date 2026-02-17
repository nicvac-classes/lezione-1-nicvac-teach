# [POC26][Pygame] Lezione 03 — Color Basket 🎯

Costruiamo un gioco di riflessi e logica: una pallina colorata cade dall'alto con gravità reale e dobbiamo catturarla ruotando un canestro circolare diviso in quattro spicchi colorati. Solo lo spicchio giusto la cattura — quello sbagliato la rimbalza via lateralmente. Dietro questo gioco si nascondono nuovi concetti: il disegno di archi, la rotazione smooth con angoli e il rilevamento delle collisioni.

---

## Cosa costruiremo

Un gioco chiamato **Color Basket** in cui:

- Una pallina di colore casuale (tra 4 possibili) cade dall'alto con la gravità di Pymunk (v. Lezione 02)
- In basso c'è un **canestro circolare** diviso in **4 spicchi colorati**, proporzionato alla pallina come un canestro NBA
- Con le **frecce SX/DX** possiamo **ruotare il canestro di 90°** con un'animazione fluida a velocità costante, cambiando quale colore si trova in alto
- Se lo **spicchio in alto corrisponde** al colore della palla → **presa!** La palla rallenta, scende nel canestro e scompare
- Se il colore **non corrisponde** → la palla **rimbalza via lateralmente**
- Dopo ogni palla (catturata o mancata), ne viene generata una nuova

---

## Concetti riutilizzati dalle lezioni precedenti

| Concetto | Lezione |
|----------|---------|
| Finestra, game loop, eventi, clock | Lezione 01 |
| Spazio fisico `pymunk.Space()` e gravità | Lezione 02 |
| Creare body e shape (pallina) | Lezione 02 |
| `space.step()` per avanzare la simulazione | Lezione 02 |

## Concetti nuovi in questa lezione

| Concetto | Descrizione |
|----------|-------------|
| `pygame.draw.arc()` | Disegnare archi (spicchi del canestro) |
| `pygame.draw.circle()` con spessore | Disegnare cerchi vuoti |
| Rotazione smooth con angoli float | Ruotare il canestro in modo fluido a velocità costante |
| `pygame.KEYDOWN` | Reagire alla singola pressione di un tasto |
| Collisioni Pymunk con `on_collision` | Reagire quando la palla tocca il canestro |
| `shape.sensor` | Shape che rileva collisioni senza bloccare fisicamente |
| `body.velocity` | Impostare la velocità di un corpo Pymunk |

---

## Blocco 1 — La finestra, lo spazio fisico e le costanti di gioco

### Obiettivo

Preparare la struttura base: finestra Pygame, spazio Pymunk con gravità e tutte le costanti che useremo nel gioco.

### Ingredienti

Tutto già noto! (v. Lezione 01, Lezione 02)

Nuovi solo i **colori del gioco** che definiamo come costanti.

| Elemento | Descrizione |
|----------|-------------|
| `COLORS = [RED, GREEN, BLUE, YELLOW]` | I 4 colori del gioco, come tuple RGB |
| `WIDTH, HEIGHT` | Dimensioni della finestra |
| `BASKET_CENTER` | Posizione del canestro |
| `BASKET_RADIUS` | Raggio del canestro (proporzionato alla pallina come NBA: rim/ball ≈ 1.9) |
| `ROTATION_SPEED` | 🆕 Velocità di rotazione del canestro in radianti/frame |

### Come combinarli

1. Importa `pygame`, `pymunk`, `sys`, `random` e `math`
2. Definisci le costanti della finestra e del gioco:
   - Dimensioni finestra: `WIDTH, HEIGHT = 600, 700`
   - FPS: `FPS = 60`
   - Colori: `RED = (220, 50, 50)`, `GREEN = (50, 200, 50)`, `BLUE = (50, 100, 220)`, `YELLOW = (240, 220, 50)`, `DARK_BG = (30, 30, 50)`
   - Lista colori: `COLORS = [RED, GREEN, BLUE, YELLOW]`
3. Definisci le costanti del canestro:
   - Centro: `BASKET_CENTER = (WIDTH // 2, HEIGHT - 150)` — centrato orizzontalmente, in basso
   - Raggio: `BASKET_RADIUS = 29` — proporzionato alla pallina come NBA (diametro canestro NBA ≈ 46 cm, pallone ≈ 24 cm → rapporto ≈ 1.9, quindi 15 × 1.9 ≈ 29)
4. Definisci le costanti della pallina:
   - Raggio: `BALL_RADIUS = 15`
   - Posizione di partenza: `BALL_START_Y = 50` — poco sotto il bordo superiore
   - Velocità di rotazione: `ROTATION_SPEED = math.pi / 20` — circa 9° per frame, una rotazione completa di 90° in circa 10 frame (~0.17 secondi a 60 FPS)
5. Inizializza Pygame, crea la finestra e il clock (v. Lezione 01)
6. Crea lo spazio Pymunk con gravità `(0, 400)` — più lenta della Lezione 02, così il giocatore ha tempo di reagire (v. Lezione 02)

### Esercizio

Scrivi il codice di setup con tutte le costanti elencate sopra e la finestra. Crea anche il game loop vuoto con solo `screen.fill(DARK_BG)` (v. Lezione 01).

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
import pygame
import pymunk
import sys
import random
import math

# --- Costanti ---
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

# --- Inizializzazione Pygame --- (v. Lezione 01)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Basket")
clock = pygame.time.Clock()

# --- Spazio fisico Pymunk --- (v. Lezione 02)
space = pymunk.Space()
space.gravity = (0, 400)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(DARK_BG)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
```

</details>

---

## Blocco 2 — Disegnare il canestro (archi colorati)

### Obiettivo

Disegnare il canestro come un cerchio diviso in **4 spicchi colorati**. Ogni spicchio è un arco di 90°. Lo spicchio `COLORS[0]` deve essere **centrato in alto** sulla verticale (da −45° a +45° rispetto alla verticale), così che guardando il canestro si veda un solo colore chiaramente in cima.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `pygame.draw.arc(surface, colore, rect, angolo_inizio, angolo_fine, spessore)` | 🆕 Disegna un arco. Gli angoli sono in **radianti**. Il `rect` è il rettangolo che contiene il cerchio. |
| `math.pi` | 🆕 Il valore di π (pi greco), serve per calcolare gli angoli in radianti. |
| `rotation_angle` | 🆕 Variabile float che tiene traccia dell'angolo di rotazione attuale del canestro (in radianti). |

### Come combinarli

Il canestro è un cerchio diviso in 4 parti. Ogni parte copre 90° (cioè π/2 radianti).

Gli angoli in Pygame partono da **destra** e vanno in **senso antiorario**. Per avere lo spicchio `COLORS[0]` centrato in alto, applichiamo un **offset di +π/4** (+45°) a ogni spicchio. In questo modo:

- Spicchio 0 (`COLORS[0]`): da +45° a +135° → centrato in alto (90°)
- Spicchio 1 (`COLORS[1]`): da +135° a +225° → centrato a sinistra (180°)
- Spicchio 2 (`COLORS[2]`): da +225° a +315° → centrato in basso (270°)
- Spicchio 3 (`COLORS[3]`): da +315° a +405° → centrato a destra (0°/360°)

Usiamo `rotation_angle` (un angolo float in radianti) per ruotare tutti gli spicchi. Il colore di ogni spicchio è indicizzato direttamente da `i` — la rotazione è gestita dall'angolo, non dall'indice del colore.

1. Crea una funzione `draw_basket(surface, center, radius, colors, rotation_angle)`
2. Calcola il `rect` del cerchio: `pygame.Rect(cx - r, cy - r, r*2, r*2)`
3. Per ogni spicchio `i` (da 0 a 3):
   - L'angolo di inizio è `i * math.pi / 2 + math.pi / 4 + rotation_angle`
   - L'angolo di fine è `(i + 1) * math.pi / 2 + math.pi / 4 + rotation_angle`
   - Il colore è `colors[i]` (la rotazione è nell'angolo, non nell'indice)
   - Disegna l'arco con spessore `8`
4. Disegna un cerchio color `DARK_BG` pieno al centro con raggio `radius - 8` (l'interno del canestro)

### Esercizio

Crea la funzione `draw_basket(surface, center, radius, colors, rotation_angle)` e chiamala nel game loop dopo `screen.fill()`. Inizializza `rotation_angle = 0.0`.

Valori da usare:
- Spessore arco: `8` pixel
- Raggio cerchio interno (sfondo): `radius - 8` (così copre l'interno senza sovrapporre gli archi)
- Colore cerchio interno: `DARK_BG` (lo sfondo)
- Offset iniziale di ogni spicchio: `+math.pi / 4` (+45°) — così `COLORS[0]` è centrato in alto

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
# --- Variabili di gioco ---
rotation_angle = 0.0                                                       # 🆕

def draw_basket(surface, center, radius, colors, rotation_angle):          # 🆕
    """Disegna il canestro con 4 spicchi colorati (spicchio centrato in alto)."""
    cx, cy = center                                                        # 🆕
    rect = pygame.Rect(cx - radius, cy - radius, radius * 2, radius * 2)  # 🆕
                                                                           # 🆕
    for i in range(4):                                                     # 🆕
        start_angle = i * math.pi / 2 + math.pi / 4 + rotation_angle      # 🆕
        end_angle = (i + 1) * math.pi / 2 + math.pi / 4 + rotation_angle  # 🆕
        pygame.draw.arc(surface, colors[i],                                # 🆕
                        rect, start_angle, end_angle, 8)                   # 🆕
                                                                           # 🆕
    # Interno del canestro                                                 # 🆕
    pygame.draw.circle(surface, DARK_BG, center, radius - 8)              # 🆕

# --- Game loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(DARK_BG)
    draw_basket(screen, BASKET_CENTER, BASKET_RADIUS, COLORS, rotation_angle)  # 🆕
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
```

</details>

---

## Blocco 3 — Ruotare il canestro con le frecce (animazione smooth)

### Obiettivo

Usare le frecce SX e DX per ruotare il canestro di 90° alla volta, con un'**animazione fluida a velocità costante** (non un salto istantaneo). Tenere traccia di quale colore è in alto con un semplice indice.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `pygame.KEYDOWN` | 🆕 Evento che si attiva **una sola volta** quando un tasto viene premuto (a differenza di `get_pressed()` che rileva la pressione continua, v. Lezione 01). |
| `event.key` | 🆕 Il tasto specifico associato all'evento `KEYDOWN`. |
| `pygame.K_LEFT`, `pygame.K_RIGHT` | Le costanti per i tasti freccia (v. Lezione 01). |
| `target_rotation_angle` | 🆕 L'angolo obiettivo verso cui `rotation_angle` si muove progressivamente. |
| `basket_top_index` | 🆕 L'indice in `COLORS` del colore attualmente in alto nel canestro. |
| `ROTATION_SPEED` | La velocità costante (radianti/frame) con cui l'angolo si avvicina all'obiettivo. |

### Come combinarli

In Lezione 01 abbiamo usato `pygame.key.get_pressed()` per il movimento continuo del cerchio. Qui vogliamo qualcosa di diverso: **una sola rotazione per ogni pressione del tasto**, ma con un'**animazione fluida**.

Il meccanismo è:
1. Alla pressione del tasto, aggiorniamo `target_rotation_angle` di ±π/2 (90°)
2. Contemporaneamente aggiorniamo `basket_top_index` per tenere traccia di quale colore è in alto
3. Ad ogni frame, `rotation_angle` si avvicina a `target_rotation_angle` con velocità costante `ROTATION_SPEED`
4. Quando la differenza è minore di `ROTATION_SPEED`, `rotation_angle` viene impostato esattamente a `target_rotation_angle`

Per il colore in alto usiamo un semplice indice:
- All'inizio `basket_top_index = 0` → il colore in alto è `COLORS[0]` (RED)
- LEFT ruota in senso antiorario → il colore successivo sale in alto → `basket_top_index = (basket_top_index - 1) % 4`
- RIGHT ruota in senso orario → il colore precedente sale → `basket_top_index = (basket_top_index + 1) % 4`

Implementazione:
1. Nel ciclo degli eventi, controlla se `event.type == pygame.KEYDOWN`
2. Se `event.key == pygame.K_LEFT`:
   - `target_rotation_angle += math.pi / 2`
   - `basket_top_index = (basket_top_index - 1) % 4`
   - `basket_top_color = COLORS[basket_top_index]`
3. Se `event.key == pygame.K_RIGHT`:
   - `target_rotation_angle -= math.pi / 2`
   - `basket_top_index = (basket_top_index + 1) % 4`
   - `basket_top_color = COLORS[basket_top_index]`
4. Nel game loop, ad ogni frame, avvicina `rotation_angle` a `target_rotation_angle`:
   - Calcola la differenza `diff`
   - Se `abs(diff) <= ROTATION_SPEED` → imposta direttamente al target
   - Altrimenti → incrementa/decrementa di `ROTATION_SPEED`

### Esercizio

Aggiungi la gestione della rotazione smooth nel ciclo degli eventi e nel game loop. Prova a premere le frecce e verifica che gli spicchi ruotino in modo fluido.

Valori da usare:
- Inizializza `target_rotation_angle = 0.0`
- Inizializza `basket_top_index = 0` e `basket_top_color = COLORS[0]`
- Incremento/decremento dell'angolo per ogni pressione: `math.pi / 2` (90°)
- Velocità di avvicinamento: `ROTATION_SPEED` (definita nel Blocco 1 come `math.pi / 20`)

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
# --- Variabili di gioco ---
rotation_angle = 0.0
target_rotation_angle = 0.0                                                # 🆕
basket_top_index = 0                                                       # 🆕
basket_top_color = COLORS[basket_top_index]                                # 🆕

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:                                   # 🆕
            if event.key == pygame.K_LEFT:                                 # 🆕
                target_rotation_angle += math.pi / 2                       # 🆕
                basket_top_index = (basket_top_index - 1) % 4              # 🆕
                basket_top_color = COLORS[basket_top_index]                # 🆕
            elif event.key == pygame.K_RIGHT:                              # 🆕
                target_rotation_angle -= math.pi / 2                       # 🆕
                basket_top_index = (basket_top_index + 1) % 4              # 🆕
                basket_top_color = COLORS[basket_top_index]                # 🆕

    screen.fill(DARK_BG)

    # --- Rotazione smooth a velocità costante ---                         # 🆕
    if rotation_angle != target_rotation_angle:                            # 🆕
        diff = target_rotation_angle - rotation_angle                      # 🆕
        if abs(diff) <= ROTATION_SPEED:                                    # 🆕
            rotation_angle = target_rotation_angle                         # 🆕
        elif diff > 0:                                                     # 🆕
            rotation_angle += ROTATION_SPEED                               # 🆕
        else:                                                              # 🆕
            rotation_angle -= ROTATION_SPEED                               # 🆕

    draw_basket(screen, BASKET_CENTER, BASKET_RADIUS, COLORS, rotation_angle)
    pygame.display.flip()
    clock.tick(FPS)
```

</details>

---

## Blocco 4 — Creare la pallina che cade

### Obiettivo

Creare una pallina Pymunk con un colore casuale che cade dall'alto verso il canestro, sempre allineata al centro del canestro.

### Ingredienti

Tutto già noto dalla Lezione 02! La novità è solo l'associazione di un **colore** alla pallina.

| Elemento | Descrizione |
|----------|-------------|
| `pymunk.Body(massa, momento)` | Crea un corpo dinamico (v. Lezione 02) |
| `pymunk.Circle(body, raggio)` | Crea la forma circolare (v. Lezione 02) |
| `pymunk.moment_for_circle(massa, 0, raggio)` | Calcola il momento d'inerzia (v. Lezione 02) |
| `random.choice(lista)` | 🆕 Sceglie un elemento casuale da una lista. |

### Come combinarli

1. Crea una funzione `create_ball()` che:
   - Sceglie un colore casuale con `random.choice(COLORS)`
   - Crea un body Pymunk con massa `1`, posizionato in alto al centro del canestro (`BASKET_CENTER[0]`, `BALL_START_Y`)
   - Crea una shape `pymunk.Circle` con raggio `BALL_RADIUS`
   - Imposta elasticità a `0.7` e frizione a `0.5`
   - Aggiunge body e shape allo spazio
   - Restituisce un **dizionario** con `body`, `shape` e `color`
2. Crea la prima pallina all'inizio del gioco

### Esercizio

Scrivi la funzione `create_ball()` e crea la prima pallina. Per ora non la disegniamo ancora — ci penseremo nel prossimo blocco.

Valori da usare:
- Massa: `1`
- Posizione X: `BASKET_CENTER[0]` (centrata sul canestro)
- Posizione Y: `BALL_START_Y` (`50`)
- Raggio: `BALL_RADIUS` (`15`)
- Elasticità: `0.7`
- Frizione: `0.5`
- La funzione deve restituire un dizionario con chiavi `"body"`, `"shape"` e `"color"`

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
def create_ball():                                                          # 🆕
    """Crea una pallina con colore casuale che cade dall'alto."""            # 🆕
    color = random.choice(COLORS)                                           # 🆕
    x = BASKET_CENTER[0]                                                    # 🆕
    mass = 1                                                                # 🆕
    moment = pymunk.moment_for_circle(mass, 0, BALL_RADIUS)                 # 🆕
    body = pymunk.Body(mass, moment)                                        # 🆕
    body.position = (x, BALL_START_Y)                                       # 🆕
    shape = pymunk.Circle(body, BALL_RADIUS)                                # 🆕
    shape.elasticity = 0.7                                                  # 🆕
    shape.friction = 0.5                                                    # 🆕
    shape.collision_type = 1                                                # 🆕
    space.add(body, shape)                                                  # 🆕
    return {"body": body, "shape": shape, "color": color}                   # 🆕

# Crea la prima pallina                                                     # 🆕
ball = create_ball()                                                        # 🆕
```

</details>

---

## Blocco 5 — Disegnare la pallina e far avanzare la fisica

### Obiettivo

Disegnare la pallina con il suo colore e far avanzare la simulazione Pymunk, così la palla cade per gravità.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `pygame.draw.circle(surface, colore, (x, y), raggio)` | Disegna un cerchio (v. Lezione 01) |
| `body.position` | La posizione attuale del corpo Pymunk (v. Lezione 02) |
| `space.step(dt)` | Avanza la simulazione fisica (v. Lezione 02) |

### Come combinarli

In Lezione 02 abbiamo usato `debug_draw` per disegnare le palline automaticamente. Questa volta **disegniamo a mano** con `pygame.draw.circle` perché vogliamo assegnare a ogni pallina il suo colore specifico, ma continuiamo a far calcolare le coordinate da Pymunk ad ogni loop.

1. Nel game loop, dopo `draw_basket()`:
   - Leggi la posizione dal body Pymunk: `ball["body"].position`
   - Converti le coordinate in interi (Pygame vuole interi): `int(pos.x)`, `int(pos.y)`
   - Disegna il cerchio con `pygame.draw.circle(screen, ball["color"], (int(pos.x), int(pos.y)), BALL_RADIUS)`
2. Chiama `space.step(1/FPS)` per far avanzare la fisica (v. Lezione 02)

### Esercizio

Aggiorna il game loop per disegnare la pallina e far avanzare la fisica. La pallina dovrebbe cadere verso il basso!

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
# --- Game loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                target_rotation_angle += math.pi / 2
                basket_top_index = (basket_top_index - 1) % 4
                basket_top_color = COLORS[basket_top_index]
            elif event.key == pygame.K_RIGHT:
                target_rotation_angle -= math.pi / 2
                basket_top_index = (basket_top_index + 1) % 4
                basket_top_color = COLORS[basket_top_index]

    screen.fill(DARK_BG)

    # Rotazione smooth
    if rotation_angle != target_rotation_angle:
        diff = target_rotation_angle - rotation_angle
        if abs(diff) <= ROTATION_SPEED:
            rotation_angle = target_rotation_angle
        elif diff > 0:
            rotation_angle += ROTATION_SPEED
        else:
            rotation_angle -= ROTATION_SPEED

    draw_basket(screen, BASKET_CENTER, BASKET_RADIUS, COLORS, rotation_angle)

    # Disegna la pallina                                                   # 🆕
    pos = ball["body"].position                                            # 🆕
    pygame.draw.circle(screen, ball["color"],                              # 🆕
                       (int(pos.x), int(pos.y)), BALL_RADIUS)              # 🆕

    space.step(1 / FPS)                                                    # 🆕
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
```

</details>

---

## Blocco 6 — Il sensore del canestro (collisioni Pymunk)

### Obiettivo

Creare il canestro come oggetto fisico Pymunk con un **sensore**, così la pallina può collidere con esso e la collisione viene gestita dal nostro codice.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `pymunk.Body(body_type=pymunk.Body.KINEMATIC)` | 🆕 Un corpo **cinematico**: non è influenzato dalla gravità ma può muoversi e collidere. Perfetto per il canestro. |
| `pymunk.Circle(body, raggio)` | La forma circolare, usata qui come area del canestro (v. Lezione 02). |
| `shape.sensor` | 🆕 Se `True`, la shape rileva le collisioni ma **non** blocca fisicamente gli oggetti. Questo ci permette di decidere nel codice se la palla passa o rimbalza. |
| `shape.collision_type` | 🆕 Un numero identificativo per distinguere diversi tipi di oggetti nelle collisioni. |

### Come combinarli

Il canestro usa un **unico sensore** grande quanto il cerchio visivo. Essendo un sensore, non blocca fisicamente la pallina — saremo noi a gestire cosa succede nel callback della collisione.

Usiamo `collision_type` per identificare gli oggetti:
- `collision_type = 1` → pallina
- `collision_type = 2` → sensore del canestro

1. Crea un body cinematico per il canestro posizionato a `BASKET_CENTER`
2. Aggiungi una shape circolare come sensore (`sensor = True`) con raggio `BASKET_RADIUS`
3. Assegna `collision_type = 2` al sensore
4. Assegna `collision_type = 1` alla pallina (in `create_ball()`)

### Esercizio

Crea il sensore fisico del canestro. Aggiorna anche `create_ball()` per assegnare `collision_type = 1` alla pallina.

Valori da usare:
- Tipo body canestro: `pymunk.Body.KINEMATIC`
- Posizione: `BASKET_CENTER`
- Raggio sensore: `BASKET_RADIUS` (uguale al cerchio visivo)
- `sensor = True` (rileva collisioni senza bloccare)
- `collision_type = 2` per il canestro, `collision_type = 1` per la pallina

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
# --- Canestro fisico --- 🆕
basket_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)                 # 🆕
basket_body.position = BASKET_CENTER                                        # 🆕

# Sensore unico per rilevare la collisione con la pallina                   # 🆕
basket_sensor = pymunk.Circle(basket_body, BASKET_RADIUS)                   # 🆕
basket_sensor.sensor = True                                                 # 🆕
basket_sensor.collision_type = 2                                            # 🆕

space.add(basket_body, basket_sensor)                                       # 🆕
```

E aggiorna `create_ball()` aggiungendo prima di `space.add(...)`:

```python
    shape.collision_type = 1                                                # 🆕
```

</details>

---

## Blocco 7 — Gestire la collisione: cattura o rimbalzo

### Obiettivo

Quando la pallina entra nel sensore del canestro, controlliamo se il colore corrisponde allo spicchio in alto. Se sì → la pallina rallenta e scende nel canestro. Se no → la palla viene lanciata via lateralmente.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `space.on_collision(tipo_a, tipo_b, begin=funzione)` | 🆕 Registra una funzione callback che viene chiamata quando due oggetti con i `collision_type` specificati si toccano. |
| Valore di ritorno del callback | 🆕 Il callback restituisce `True` per elaborare la collisione normalmente o `False` per ignorarla (l'oggetto attraversa). |
| `body.velocity` | 🆕 La velocità del corpo Pymunk. Si può impostare per rallentare o lanciare la palla. |

### Come combinarli

Nel callback della collisione usiamo `basket_top_color` (calcolato nel Blocco 3) per sapere quale colore è in alto:
- Se il colore corrisponde → `caught = True`, reimpostiamo la velocità della pallina a `(0, 80)` per un effetto "satisfying" di entrata lenta nel canestro. Ritorniamo `False` (la palla attraversa il sensore).
- Se non corrisponde → `missed = True`, lanciamo la pallina via lateralmente con una velocità casuale. Ritorniamo `False`.

Usiamo due variabili di stato booleane:
- `caught` → la palla è stata catturata (colore giusto)
- `missed` → colore sbagliato, la palla vola via

1. Definisci una funzione callback `on_ball_enter_basket(arbiter, space, data)`
2. All'interno, controlla se la palla è già stata gestita (`caught or missed`) → se sì, ritorna `True`
3. Confronta `ball["color"]` con `basket_top_color`
4. Registra il callback con `space.on_collision(1, 2, begin=on_ball_enter_basket)`

### Esercizio

Crea il collision handler e le variabili di stato `caught` e `missed`.

Valori da usare:
- Velocità pallina al match: `(0, 80)` — scende lentamente nel canestro
- Velocità rimbalzo laterale (colore sbagliato): `(direction * 300, -350)` con `direction = random.choice([-1, 1])`
- Registra il callback con: `space.on_collision(1, 2, begin=on_ball_enter_basket)`

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
# --- Variabili di stato ---
caught = False                                                             # 🆕
missed = False                                                             # 🆕

def on_ball_enter_basket(arbiter, space, data):                            # 🆕
    """Callback: la pallina ha toccato il sensore del canestro."""          # 🆕
    global caught, missed                                                  # 🆕
    if caught or missed:                                                   # 🆕
        return True                                                        # 🆕
    if ball["color"] == basket_top_color:                                   # 🆕
        caught = True                                                      # 🆕
        ball["body"].velocity = (0, 80)                                    # 🆕
    else:                                                                  # 🆕
        missed = True                                                      # 🆕
        direction = random.choice([-1, 1])                                 # 🆕
        ball["body"].velocity = (direction * 300, -350)                    # 🆕
    return False                                                           # 🆕

space.on_collision(1, 2, begin=on_ball_enter_basket)                       # 🆕
```

</details>

---

## Blocco 8 — Reset della pallina

### Obiettivo

Dopo la cattura o il rimbalzo, la pallina deve essere rimossa e ne viene creata una nuova. Se catturata, la pallina scompare quando raggiunge il centro del canestro. Se mancata, scompare quando esce dallo schermo.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `space.remove(shape, body)` | 🆕 Rimuove un body e la sua shape dallo spazio fisico. |
| `body.position.y` | La coordinata Y del corpo, per controllare se ha superato il centro del canestro. |

### Come combinarli

1. Crea una funzione `remove_ball(ball)` che rimuove body e shape dallo spazio
2. Crea una funzione `reset_ball()` che:
   - Rimuove la pallina corrente
   - Crea una nuova pallina
   - Resetta `caught` e `missed` a `False`
3. Nel game loop, gestisci i tre casi:
   - `caught`: la pallina scende lentamente. Quando la sua Y supera `BASKET_CENTER[1]` → `reset_ball()`
   - `missed`: la pallina vola via. Quando esce dallo schermo (margine di 50 pixel) → `reset_ball()`
   - Altrimenti (nessuna collisione): se la pallina cade oltre lo schermo → `reset_ball()`

### Esercizio

Implementa `remove_ball()`, `reset_ball()` e la logica di reset nel game loop.

Valori da usare:
- Soglia cattura: `ball["body"].position.y >= BASKET_CENTER[1]` (il centro del canestro)
- Margine uscita schermo: `±50` pixel oltre i bordi (`bx < -50`, `bx > WIDTH + 50`, `by > HEIGHT + 50`)

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
def remove_ball(ball):                                                     # 🆕
    """Rimuove la pallina dallo spazio fisico."""                           # 🆕
    space.remove(ball["shape"], ball["body"])                               # 🆕

def reset_ball():                                                          # 🆕
    """Rimuove la pallina corrente e ne crea una nuova."""                  # 🆕
    global ball, caught, missed                                            # 🆕
    remove_ball(ball)                                                      # 🆕
    ball = create_ball()                                                   # 🆕
    caught = False                                                         # 🆕
    missed = False                                                         # 🆕

# --- Aggiorna il game loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                target_rotation_angle += math.pi / 2
                basket_top_index = (basket_top_index - 1) % 4
                basket_top_color = COLORS[basket_top_index]
            elif event.key == pygame.K_RIGHT:
                target_rotation_angle -= math.pi / 2
                basket_top_index = (basket_top_index + 1) % 4
                basket_top_color = COLORS[basket_top_index]

    screen.fill(DARK_BG)

    # Rotazione smooth a velocità costante
    if rotation_angle != target_rotation_angle:
        diff = target_rotation_angle - rotation_angle
        if abs(diff) <= ROTATION_SPEED:
            rotation_angle = target_rotation_angle
        elif diff > 0:
            rotation_angle += ROTATION_SPEED
        else:
            rotation_angle -= ROTATION_SPEED

    # --- Logica di gioco ---                                              # 🆕
    if caught:                                                             # 🆕
        by = ball["body"].position.y                                       # 🆕
        if by >= BASKET_CENTER[1]:                                         # 🆕
            reset_ball()                                                   # 🆕
    elif missed:                                                           # 🆕
        bx, by = ball["body"].position                                     # 🆕
        if by > HEIGHT + 50 or bx < -50 or bx > WIDTH + 50:               # 🆕
            reset_ball()                                                   # 🆕
    else:                                                                  # 🆕
        bx, by = ball["body"].position                                     # 🆕
        if by > HEIGHT + 50:                                               # 🆕
            reset_ball()                                                   # 🆕

    # --- Disegno ---
    draw_basket(screen, BASKET_CENTER, BASKET_RADIUS, COLORS, rotation_angle)
    pos = ball["body"].position
    pygame.draw.circle(screen, ball["color"],
                       (int(pos.x), int(pos.y)), BALL_RADIUS)

    space.step(1 / FPS)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
```

</details>

---

## Codice completo finale

Ecco il programma completo assemblato, con tutti i blocchi:

```python
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
def draw_basket(surface, center, radius, colors, rotation_angle):
    """Disegna il canestro con 4 spicchi colorati (spicchio centrato in alto)."""
    cx, cy = center
    rect = pygame.Rect(cx - radius, cy - radius, radius * 2, radius * 2)

    for i in range(4):
        start_angle = i * math.pi / 2 + math.pi / 4 + rotation_angle
        end_angle = (i + 1) * math.pi / 2 + math.pi / 4 + rotation_angle
        pygame.draw.arc(surface, colors[i],
                        rect, start_angle, end_angle, 8)

    # Interno del canestro
    pygame.draw.circle(surface, DARK_BG, center, radius - 8)

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

# ============================================================
# COLLISION HANDLER
# ============================================================
caught = False
missed = False
rotation_angle = 0.0
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
                basket_top_index = (basket_top_index - 1) % 4
                basket_top_color = COLORS[basket_top_index]
            elif event.key == pygame.K_RIGHT:
                target_rotation_angle -= math.pi / 2
                basket_top_index = (basket_top_index + 1) % 4
                basket_top_color = COLORS[basket_top_index]

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
    draw_basket(screen, BASKET_CENTER, BASKET_RADIUS, COLORS, rotation_angle)
    pos = ball["body"].position
    pygame.draw.circle(screen, ball["color"],
                       (int(pos.x), int(pos.y)), BALL_RADIUS)

    space.step(1 / FPS)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
```

---

## Esercizi extra

Mettiti alla prova con queste modifiche!

### 1. Punteggio e vite
Aggiungi un punteggio che aumenta di 1 a ogni pallina catturata e 3 vite che diminuiscono quando sbagli. Mostra entrambi a schermo.

<details>
<summary>Suggerimento</summary>

Usa `pygame.font.SysFont(None, 36)` per creare un font. Con `font.render(f"Punti: {score}", True, WHITE)` crei il testo, con `screen.blit(testo, (x, y))` lo disegni. Aggiungi le variabili `score` e `lives` e aggiornale in `reset_ball()`.

</details>

### 2. Game Over e Restart
Quando le vite finiscono, mostra "GAME OVER" e permetti di ricominciare premendo R.

<details>
<summary>Suggerimento</summary>

Aggiungi una variabile `game_over = False`. Quando `lives <= 0`, impostala a `True` e mostra la schermata con `font_big.render("GAME OVER", True, RED)`. Nel ciclo eventi, gestisci `pygame.K_r` per resettare tutto.

</details>

### 3. Difficoltà crescente
Man mano che il punteggio sale, aumenta la gravità per far cadere le palline più velocemente.

<details>
<summary>Suggerimento</summary>

Modifica `space.gravity` nel game loop in base allo score. Ad esempio: `space.gravity = (0, 400 + score * 20)`.

</details>

### 4. Posizione casuale della pallina
Fai cadere la pallina da posizioni X casuali, non sempre dal centro. Aumenta il range man mano che il punteggio cresce.

<details>
<summary>Suggerimento</summary>

Modifica `create_ball()` per usare un range dipendente dallo score: `x = BASKET_CENTER[0] + random.randint(-range, range)`.

</details>

### 5. Bonus combo
Se catturi 3 palline consecutive, guadagni una vita extra.

<details>
<summary>Suggerimento</summary>

Aggiungi una variabile `combo` che si incrementa ad ogni cattura e si resetta a 0 quando manchi. Quando raggiunge 3, aggiungi una vita.

</details>
