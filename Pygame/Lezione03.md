# [POC26][Pygame] Lezione 03 — Color Basket 🎯

Costruiamo un gioco di riflessi e logica: una pallina colorata cade dall'alto con gravità reale e dobbiamo catturarla ruotando un canestro circolare diviso in quattro spicchi colorati. Solo lo spicchio giusto la cattura — quello sbagliato la rimbalza via lateralmente. Dietro questo gioco si nascondono nuovi concetti: il disegno di archi, la rotazione smooth con angoli, il rilevamento delle collisioni e la gestione dello stato di gioco.

---

## Cosa costruiremo

Un gioco chiamato **Color Basket** in cui:

- Una pallina di colore casuale (tra 4 possibili) cade dall'alto con la gravità di Pymunk (v. Lezione 02)
- In basso c'è un **canestro circolare** diviso in **4 spicchi colorati**, proporzionato alla pallina come un canestro NBA
- Con le **frecce SX/DX** possiamo **ruotare il canestro di 90°** con un'animazione fluida a velocità costante, cambiando quale colore si trova in alto
- Se lo **spicchio in alto corrisponde** al colore della palla → **presa!** La palla si muove verso il centro del canestro, si rimpicciolisce e si dissolve (+1 punto)
- Se il colore **non corrisponde** → la palla **rimbalza via lateralmente** (-1 vita)
- Il gioco termina quando le vite finiscono

---

## Concetti riutilizzati dalle lezioni precedenti

| Concetto | Lezione |
|----------|---------|
| Finestra, game loop, eventi, clock | Lezione 01 |
| `pygame.key.get_pressed()` per le frecce | Lezione 01 |
| Spazio fisico `pymunk.Space()` e gravità | Lezione 02 |
| Creare body e shape (pallina) | Lezione 02 |
| `space.step()` per avanzare la simulazione | Lezione 02 |
| Pavimento/barriere statiche | Lezione 02 |

## Concetti nuovi in questa lezione

| Concetto | Descrizione |
|----------|-------------|
| `pygame.draw.arc()` | Disegnare archi (spicchi del canestro) |
| `pygame.draw.circle()` con spessore | Disegnare cerchi vuoti |
| Rotazione smooth con angoli float | Ruotare il canestro in modo fluido a velocità costante |
| Collisioni Pymunk con `on_collision` | Reagire quando la palla tocca il canestro |
| `pygame.font.SysFont()` | Scrivere testo a schermo (punteggio, vite) |
| Effetto fade con rimpicciolimento | Far scomparire gradualmente la palla nel canestro |

---

## Blocco 1 — La finestra, lo spazio fisico e le costanti di gioco

### Obiettivo

Preparare la struttura base: finestra Pygame, spazio Pymunk con gravità e tutte le costanti che useremo nel gioco.

### Ingredienti

Tutto già noto! (v. Lezione 01, Lezione 02)

Nuovi solo i **colori del gioco** che definiamo come costanti.

| Elemento | Descrizione |
|----------|-------------|
| `COLORS = [ROSSO, VERDE, BLU, GIALLO]` | I 4 colori del gioco, come tuple RGB |
| `WIDTH, HEIGHT` | Dimensioni della finestra |
| `BASKET_CENTER` | Posizione del canestro |
| `BASKET_RADIUS` | Raggio del canestro (proporzionato alla pallina come NBA: rim/ball ≈ 1.9) |
| `ROTATION_SPEED` | 🆕 Velocità di rotazione del canestro in radianti/frame |

### Come combinarli

1. Importa `pygame`, `pymunk`, `sys`, `random` e `math`
2. Definisci le costanti della finestra e del gioco:
   - Dimensioni finestra: `WIDTH, HEIGHT = 600, 700`
   - FPS: `FPS = 60`
   - Colori: `RED = (220, 50, 50)`, `GREEN = (50, 200, 50)`, `BLUE = (50, 100, 220)`, `YELLOW = (240, 220, 50)`, `BLACK = (0, 0, 0)`, `WHITE = (255, 255, 255)`, `DARK_BG = (30, 30, 50)`
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
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
DARK_BG = (30, 30, 50)

COLORS = [RED, GREEN, BLUE, YELLOW]

# Canestro
BASKET_CENTER = (WIDTH // 2, HEIGHT - 150)
BASKET_RADIUS = 29  # proporzionato alla pallina come NBA (rim/ball ≈ 1.9)  # 🆕

# Pallina
BALL_RADIUS = 15
BALL_START_Y = 50
ROTATION_SPEED = math.pi / 20  # rad/frame – 90° in ~0.33 s               # 🆕

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

Disegnare il canestro come un cerchio diviso in **4 spicchi colorati**. Ogni spicchio è un arco di 90°. Lo spicchio in alto deve essere **centrato sulla verticale** (da −45° a +45° rispetto alla verticale), così che guardando il canestro si veda un solo colore chiaramente in cima.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `pygame.draw.arc(surface, colore, rect, angolo_inizio, angolo_fine, spessore)` | 🆕 Disegna un arco. Gli angoli sono in **radianti**. Il `rect` è il rettangolo che contiene il cerchio. |
| `math.pi` | 🆕 Il valore di π (pi greco), serve per calcolare gli angoli in radianti. |
| `rotation_angle` | 🆕 Variabile float che tiene traccia dell'angolo di rotazione attuale del canestro (in radianti). |

### Come combinarli

Il canestro è un cerchio diviso in 4 parti. Ogni parte copre 90° (cioè π/2 radianti).

Gli angoli in Pygame partono da **destra** e vanno in **senso antiorario**. Per avere lo spicchio centrato in alto, applichiamo un **offset di −π/4** (−45°) a ogni spicchio:

- Spicchio 0: da −45° a 45° (centrato in alto)
- Spicchio 1: da 45° a 135° (centrato a sinistra)
- Spicchio 2: da 135° a 225° (centrato in basso)
- Spicchio 3: da 225° a 315° (centrato a destra)

Usiamo `rotation_angle` (un angolo float in radianti) per ruotare tutti gli spicchi. Il colore di ogni spicchio è indicizzato direttamente da `i` — la rotazione è gestita dall'angolo, non dall'indice del colore.

1. Crea una funzione `draw_basket(surface, center, radius, colors, rotation_angle)`
2. Calcola il `rect` del cerchio: `pygame.Rect(cx - r, cy - r, r*2, r*2)`
3. Per ogni spicchio `i` (da 0 a 3):
   - L'angolo di inizio è `i * math.pi / 2 - math.pi / 4 + rotation_angle`
   - L'angolo di fine è `(i + 1) * math.pi / 2 - math.pi / 4 + rotation_angle`
   - Il colore è `colors[i]` (la rotazione è nell'angolo, non nell'indice)
   - Disegna l'arco con spessore 8
4. Disegna un cerchio nero pieno al centro (l'interno del canestro)

### Esercizio

Crea la funzione `draw_basket(surface, center, radius, colors, rotation_angle)` e chiamala nel game loop dopo `screen.fill()`. Inizializza `rotation_angle = 0.0`.

Valori da usare:
- Spessore arco: `8` pixel
- Raggio cerchio interno (sfondo): `radius - 8` (così copre l'interno senza sovrapporre gli archi)
- Colore cerchio interno: `DARK_BG` (lo sfondo)
- Offset iniziale di ogni spicchio: `-math.pi / 4` (−45°)

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
# --- Variabili di gioco ---
rotation_angle = 0.0  # 🆕 angolo di rotazione del canestro (in radianti)

def draw_basket(surface, center, radius, colors, rotation_angle):          # 🆕
    """Disegna il canestro con 4 spicchi colorati (spicchio centrato in alto)."""  # 🆕
    cx, cy = center                                                        # 🆕
    rect = pygame.Rect(cx - radius, cy - radius, radius * 2, radius * 2)  # 🆕
                                                                           # 🆕
    for i in range(4):                                                     # 🆕
        start_angle = i * math.pi / 2 - math.pi / 4 + rotation_angle      # 🆕
        end_angle = (i + 1) * math.pi / 2 - math.pi / 4 + rotation_angle  # 🆕
        pygame.draw.arc(surface, colors[i],                                # 🆕
                        rect, start_angle, end_angle, 8)                   # 🆕
                                                                           # 🆕
    # Interno nero del canestro                                            # 🆕
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

Usare le frecce SX e DX per ruotare il canestro di 90° alla volta, con un'**animazione fluida a velocità costante** (non un salto istantaneo).

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `pygame.KEYDOWN` | 🆕 Evento che si attiva **una sola volta** quando un tasto viene premuto (a differenza di `get_pressed()` che rileva la pressione continua, v. Lezione 01). |
| `event.key` | 🆕 Il tasto specifico associato all'evento `KEYDOWN`. |
| `pygame.K_LEFT`, `pygame.K_RIGHT` | Le costanti per i tasti freccia (v. Lezione 01). |
| `target_rotation_angle` | 🆕 L'angolo obiettivo verso cui `rotation_angle` si muove progressivamente. |
| `ROTATION_SPEED` | 🆕 La velocità costante (radianti/frame) con cui l'angolo si avvicina all'obiettivo. |

### Come combinarli

In Lezione 01 abbiamo usato `pygame.key.get_pressed()` per il movimento continuo del cerchio. Qui vogliamo qualcosa di diverso: **una sola rotazione per ogni pressione del tasto**, ma con un'**animazione fluida**.

Il meccanismo è:
1. Alla pressione del tasto, aggiorniamo `target_rotation_angle` di ±π/2 (90°)
2. Ad ogni frame, `rotation_angle` si avvicina a `target_rotation_angle` con velocità costante `ROTATION_SPEED`
3. Quando la differenza è minore di `ROTATION_SPEED`, `rotation_angle` viene impostato esattamente a `target_rotation_angle`

Usiamo l'evento `KEYDOWN` invece di `get_pressed()`:
- `KEYDOWN` si attiva **una volta** quando il tasto viene premuto
- `get_pressed()` si attiva **ogni frame** finché il tasto è tenuto premuto

1. Nel ciclo degli eventi, controlla se `event.type == pygame.KEYDOWN`
2. Se `event.key == pygame.K_LEFT` → incrementa `target_rotation_angle` di `math.pi / 2`
3. Se `event.key == pygame.K_RIGHT` → decrementa `target_rotation_angle` di `math.pi / 2`
4. Nel game loop, ad ogni frame, avvicina `rotation_angle` a `target_rotation_angle`:
   - Calcola la differenza `diff`
   - Se `abs(diff) <= ROTATION_SPEED` → imposta direttamente al target
   - Altrimenti → incrementa/decrementa di `ROTATION_SPEED`

### Esercizio

Aggiungi la gestione della rotazione smooth nel ciclo degli eventi e nel game loop. Prova a premere le frecce e verifica che gli spicchi ruotino in modo fluido.

Valori da usare:
- Inizializza `target_rotation_angle = 0.0`
- Incremento/decremento per ogni pressione: `math.pi / 2` (90°)
- Velocità di avvicinamento: `ROTATION_SPEED` (definita nel Blocco 1 come `math.pi / 20`)

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
# --- Variabili di gioco ---
rotation_angle = 0.0                                                       # 🆕
target_rotation_angle = 0.0                                                # 🆕

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:                                   # 🆕
            if event.key == pygame.K_LEFT:                                 # 🆕
                target_rotation_angle += math.pi / 2                       # 🆕
            elif event.key == pygame.K_RIGHT:                              # 🆕
                target_rotation_angle -= math.pi / 2                       # 🆕

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
   - Crea un body Pymunk con massa 1, posizionato in alto al centro del canestro (`BASKET_CENTER[0]`)
   - Crea una shape `pymunk.Circle` con raggio `BALL_RADIUS`
   - Imposta elasticità a `0.7` (la palla rimbalza un po')
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

In Lezione 02 abbiamo usato `debug_draw` per disegnare tutto automaticamente. Questa volta **disegniamo a mano** perché vogliamo controllare i colori.

1. Nel game loop, dopo `draw_basket()`:
   - Leggi la posizione dal body Pymunk: `ball["body"].position`
   - Converti le coordinate in interi (Pygame vuole interi)
   - Leggi il colore (eventualmente modificato dal fade) con `ball.get("draw_color", ball["color"])`
   - Leggi il raggio (eventualmente modificato dal rimpicciolimento) con `ball.get("draw_radius", BALL_RADIUS)`
   - Disegna il cerchio con `pygame.draw.circle()`
2. Chiama `space.step(1/FPS)` per far avanzare la fisica (v. Lezione 02)

### Esercizio

Aggiorna il game loop per disegnare la pallina. La pallina dovrebbe cadere verso il basso!

Valori da usare:
- `space.step(1 / FPS)` per avanzare la simulazione (usa `1/FPS` come dt, v. Lezione 02)
- Per il colore, usa `ball.get("draw_color", ball["color"])` — servirà quando aggiungeremo il fade
- Per il raggio, usa `ball.get("draw_radius", BALL_RADIUS)` — servirà quando aggiungeremo il rimpicciolimento
- Converti le coordinate in interi con `int(pos.x)`, `int(pos.y)` perché Pygame vuole interi

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
            elif event.key == pygame.K_RIGHT:
                target_rotation_angle -= math.pi / 2

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
    draw_color = ball.get("draw_color", ball["color"])                     # 🆕
    draw_radius = ball.get("draw_radius", BALL_RADIUS)                     # 🆕
    pos = ball["body"].position                                            # 🆕
    pygame.draw.circle(screen, draw_color,                                 # 🆕
                       (int(pos.x), int(pos.y)), draw_radius)              # 🆕

    space.step(1 / FPS)                                                    # 🆕
    pygame.display.flip()
    clock.tick(FPS)
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

Il canestro usa un **unico sensore** grande quanto il cerchio visivo. Essendo un sensore, non blocca fisicamente la pallina — saremo noi a gestire cosa succede nel callback della collisione:
- Se il colore corrisponde → la palla passa attraverso e viene catturata
- Se non corrisponde → la palla viene lanciata via lateralmente nel callback

Usiamo `collision_type` per identificare gli oggetti:
- `collision_type = 1` → pallina
- `collision_type = 2` → sensore del canestro

1. Crea un body cinematico per il canestro
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

## Blocco 7 — Gestire la collisione: cattura o rimbalzo?

### Obiettivo

Quando la pallina entra nel sensore del canestro, controlliamo se il colore corrisponde allo spicchio in alto. Se sì → cattura! Se no → la palla viene lanciata via lateralmente.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `space.on_collision(tipo_a, tipo_b, begin=funzione)` | 🆕 Registra una funzione callback che viene chiamata quando due oggetti con i `collision_type` specificati si toccano. |
| Valore di ritorno del callback | 🆕 Il callback restituisce `True` per elaborare la collisione normalmente o `False` per ignorarla (l'oggetto attraversa). |
| `body.velocity` | 🆕 La velocità del corpo Pymunk. Si può impostare per lanciare la palla in una direzione. |

### Come combinarli

Per determinare quale colore è **in alto** nel canestro, usiamo una formula trigonometrica basata su `rotation_angle`: calcoliamo `beta = (3π/4 − rotation_angle) mod 2π` e dividiamo per π/2 per ottenere l'indice del colore.

Nel callback della collisione:
- Se il colore corrisponde → salviamo la posizione di cattura e restituiamo `False` (la palla attraversa il sensore)
- Se non corrisponde → impostiamo la velocità della pallina per lanciarla via lateralmente (in una direzione casuale destra o sinistra) e restituiamo `False`

1. Crea una funzione `get_top_color(rotation_angle)` che calcola quale colore è in alto
2. Definisci una funzione callback `on_ball_enter_basket(arbiter, space, data)` che:
   - Controlla se il colore della pallina corrisponde al colore dello spicchio in alto
   - Se corrisponde → `caught = True`, salva la posizione di cattura, ritorna `False`
   - Se non corrisponde → `missed = True`, lancia la palla via lateralmente, ritorna `False`
3. Registra il callback con `space.on_collision(1, 2, begin=on_ball_enter_basket)`

Usiamo variabili di stato per gestire cosa succede dopo la collisione:
- `caught` → la palla è stata catturata
- `missed` → colore sbagliato

### Esercizio

Crea il collision handler e le variabili di stato.

Valori iniziali delle variabili di stato:
- `score = 0`, `lives = 3`
- `caught = False`, `missed = False`

Formula per `get_top_color()`: `beta = (3 * math.pi / 4 - rotation_angle) % (2 * math.pi)`, poi `index = int(beta / (math.pi / 2)) % 4`

Velocità rimbalzo laterale (colore sbagliato): `(direction * 400, -300)` con `direction = random.choice([-1, 1])`

Registra il callback con: `space.on_collision(1, 2, begin=on_ball_enter_basket)`

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
# --- Variabili di stato ---
score = 0                                                                  # 🆕
lives = 3                                                                  # 🆕
caught = False                                                             # 🆕
missed = False                                                             # 🆕

def get_top_color(rotation_angle):                                         # 🆕
    """Restituisce il colore dello spicchio in alto del canestro."""        # 🆕
    beta = (3 * math.pi / 4 - rotation_angle) % (2 * math.pi)             # 🆕
    index = int(beta / (math.pi / 2)) % 4                                 # 🆕
    return COLORS[index]                                                   # 🆕

def on_ball_enter_basket(arbiter, space, data):                            # 🆕
    """Callback: la pallina ha toccato il sensore del canestro."""          # 🆕
    global caught, missed                                                  # 🆕
    if caught or missed:                                                   # 🆕
        return True                                                        # 🆕
    top_color = get_top_color(rotation_angle)                              # 🆕
    if ball["color"] == top_color:                                         # 🆕
        caught = True                                                      # 🆕
        ball["catch_pos"] = tuple(ball["body"].position)                   # 🆕
        return False  # la palla attraversa il sensore                     # 🆕
    else:                                                                  # 🆕
        missed = True                                                      # 🆕
        # Lancia la pallina via lateralmente                               # 🆕
        direction = random.choice([-1, 1])                                 # 🆕
        ball["body"].velocity = (direction * 400, -300)                    # 🆕
        return False  # non bloccare, lascia volare via                    # 🆕

space.on_collision(1, 2, begin=on_ball_enter_basket)                       # 🆕
```

</details>

---

## Blocco 8 — Effetto fade, rimpicciolimento e nuova pallina

### Obiettivo

Quando la palla viene catturata, la facciamo muovere verso il centro del canestro con interpolazione lineare, si rimpicciolisce e si dissolve nello sfondo — dando l'effetto di cadere dentro il canestro. Se viene mancata, aspettiamo che la palla esca dallo schermo prima di togliere una vita.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| Interpolazione lineare (lerp) | 🆕 Per calcolare il colore intermedio tra il colore della palla e lo sfondo, e per la posizione dal punto di cattura al centro del canestro. |
| `ball["catch_pos"]` | 🆕 La posizione in cui la palla è stata catturata, salvata nel callback. |
| `ball["draw_radius"]` | 🆕 Il raggio attuale della palla durante l'animazione di rimpicciolimento. |

### Come combinarli

L'effetto fade con rimpicciolimento funziona così:
1. Quando `caught = True`, iniziamo un timer di fade (es. 30 frame)
2. Ad ogni frame, calcoliamo `progress = fade_timer / fade_duration`
3. La pallina si muove **linearmente** dalla posizione di cattura (`catch_pos`) al centro del canestro
4. Il colore della pallina si avvicina al colore dello sfondo (interpolazione)
5. Il raggio della pallina diminuisce fino a 1 pixel
6. Quando il fade è completo, rimuoviamo la pallina dallo spazio e ne creiamo una nuova

Per la palla mancata, **aspettiamo che esca dallo schermo** (così si vede l'animazione del rimbalzo laterale) prima di togliere una vita.

1. Aggiungi le variabili `fade_timer` e `fade_duration`
2. Quando `caught`, ad ogni frame:
   - Calcola `progress = min(fade_timer / fade_duration, 1.0)`
   - Calcola la posizione interpolata: `x = sx + (cx - sx) * progress`
   - Calcola il colore interpolato verso lo sfondo
   - Calcola il raggio: `max(1, int(BALL_RADIUS * (1 - progress)))`
   - Incrementa il timer
3. Quando `missed`:
   - Controlla se la palla è uscita dallo schermo
   - Se sì → togli vita e crea nuova pallina

### Esercizio

Implementa la logica di fade e reset. Crea una funzione `reset_ball()` che rimuove la pallina corrente e ne crea una nuova.

Valori da usare:
- `fade_timer = 0` (contatore di frame dall'inizio del fade)
- `fade_duration = 30` (il fade dura 30 frame, cioè 0.5 secondi a 60 FPS)
- `progress = min(fade_timer / fade_duration, 1.0)` (va da 0.0 a 1.0)
- Raggio durante il fade: `max(1, int(BALL_RADIUS * (1 - progress)))` (da 15 a 1)
- Margine per "uscita dallo schermo": `±50` pixel oltre i bordi (`bx < -50`, `bx > WIDTH + 50`, `by > HEIGHT + 50`)

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
# --- Variabili di stato --- (aggiorna quelle esistenti)
score = 0
lives = 3
caught = False
missed = False
fade_timer = 0                                                             # 🆕
fade_duration = 30                                                         # 🆕

def lerp_color(color, target, progress):                                   # 🆕
    """Interpola linearmente tra due colori."""                             # 🆕
    r = int(color[0] + (target[0] - color[0]) * progress)                  # 🆕
    g = int(color[1] + (target[1] - color[1]) * progress)                  # 🆕
    b = int(color[2] + (target[2] - color[2]) * progress)                  # 🆕
    return (max(0, min(255, r)),                                           # 🆕
            max(0, min(255, g)),                                           # 🆕
            max(0, min(255, b)))                                           # 🆕

def remove_ball(ball):                                                     # 🆕
    """Rimuove la pallina dallo spazio fisico."""                           # 🆕
    space.remove(ball["shape"], ball["body"])                               # 🆕

def reset_ball():                                                          # 🆕
    """Rimuove la pallina corrente e ne crea una nuova."""                  # 🆕
    global ball, caught, missed, fade_timer                                # 🆕
    remove_ball(ball)                                                      # 🆕
    ball = create_ball()                                                   # 🆕
    caught = False                                                         # 🆕
    missed = False                                                         # 🆕
    fade_timer = 0                                                         # 🆕

# --- Aggiorna il game loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                target_rotation_angle += math.pi / 2
            elif event.key == pygame.K_RIGHT:
                target_rotation_angle -= math.pi / 2

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

    # --- Logica di gioco ---                                              # 🆕
    if caught:                                                             # 🆕
        fade_timer += 1                                                    # 🆕
        progress = min(fade_timer / fade_duration, 1.0)                    # 🆕
        # Posizione: interpolazione lineare dalla cattura al centro        # 🆕
        sx, sy = ball["catch_pos"]                                         # 🆕
        cx, cy = BASKET_CENTER                                             # 🆕
        ball["body"].velocity = (0, 0)                                     # 🆕
        ball["body"].position = (                                          # 🆕
            sx + (cx - sx) * progress,                                     # 🆕
            sy + (cy - sy) * progress                                      # 🆕
        )                                                                  # 🆕
        # Colore: dissolvi verso sfondo                                    # 🆕
        ball["draw_color"] = lerp_color(ball["color"], DARK_BG, progress)  # 🆕
        # Raggio: rimpicciolisci                                           # 🆕
        ball["draw_radius"] = max(1, int(BALL_RADIUS * (1 - progress)))    # 🆕
        if fade_timer >= fade_duration:                                    # 🆕
            score += 1                                                     # 🆕
            reset_ball()                                                   # 🆕
    elif missed:                                                           # 🆕
        # Aspetta che la pallina esca dallo schermo                        # 🆕
        bx, by = ball["body"].position                                     # 🆕
        if by > HEIGHT + 50 or bx < -50 or bx > WIDTH + 50:               # 🆕
            lives -= 1                                                     # 🆕
            reset_ball()                                                   # 🆕
    else:                                                                  # 🆕
        # Controlla se la palla è uscita dallo schermo                     # 🆕
        bx, by = ball["body"].position                                     # 🆕
        if by > HEIGHT + 50 or bx < -50 or bx > WIDTH + 50:               # 🆕
            lives -= 1                                                     # 🆕
            reset_ball()                                                   # 🆕

    # --- Disegno ---
    draw_basket(screen, BASKET_CENTER, BASKET_RADIUS, COLORS, rotation_angle)

    # Disegna la pallina con eventuale colore/raggio fade                  # 🆕
    draw_color = ball.get("draw_color", ball["color"])                     # 🆕
    draw_radius = ball.get("draw_radius", BALL_RADIUS)                     # 🆕
    pos = ball["body"].position                                            # 🆕
    pygame.draw.circle(screen, draw_color,                                 # 🆕
                       (int(pos.x), int(pos.y)), draw_radius)              # 🆕

    space.step(1 / FPS)
    pygame.display.flip()
    clock.tick(FPS)
```

</details>

---

## Blocco 9 — Punteggio, vite e Game Over

### Obiettivo

Mostrare il punteggio e le vite a schermo e gestire la schermata di Game Over.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `pygame.font.SysFont(nome, dimensione)` | 🆕 Crea un font di sistema. Usa `None` per il font predefinito. |
| `font.render(testo, antialias, colore)` | 🆕 Trasforma una stringa in una surface da disegnare. |
| `surface.blit(source, (x, y))` | 🆕 Disegna una surface sopra un'altra nella posizione specificata. |

### Come combinarli

1. Crea il font all'inizio del programma (fuori dal game loop)
2. Crea una funzione `draw_hud(surface, score, lives)` che:
   - Renderizza il testo del punteggio e delle vite
   - Li posiziona in alto a sinistra e a destra
3. Crea una funzione `draw_game_over(surface, score)` che:
   - Mostra "GAME OVER" al centro dello schermo
   - Mostra il punteggio finale
   - Mostra "Premi R per ricominciare"
4. Aggiungi una variabile `game_over` e controlla se `lives <= 0`
5. Aggiungi il tasto R per ricominciare

### Esercizio

Implementa l'HUD e la schermata di Game Over. Aggiungi il tasto R per resettare il gioco.

Valori da usare:
- Font piccolo: `pygame.font.SysFont(None, 36)` — per punteggio, vite e testo restart
- Font grande: `pygame.font.SysFont(None, 72)` — per "GAME OVER"
- Punteggio: in alto a sinistra `(10, 10)`
- Vite: in alto a destra, allineate a `WIDTH - larghezza_testo - 10`
- Formato vite: `f"Vite: {'❤' * lives}"`
- "GAME OVER" centrato orizzontalmente, a `HEIGHT // 2 - 80`
- Punteggio finale centrato a `HEIGHT // 2`
- "Premi R per ricominciare" centrato a `HEIGHT // 2 + 50`
- Nella `reset_game()`, resetta `rotation_angle = 0.0` e `target_rotation_angle = 0.0`

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
# --- Font --- 🆕
font = pygame.font.SysFont(None, 36)                                      # 🆕
font_big = pygame.font.SysFont(None, 72)                                  # 🆕

# --- Variabili di stato --- (aggiorna)
game_over = False                                                          # 🆕

def draw_hud(surface, score, lives):                                       # 🆕
    """Disegna il punteggio e le vite."""                                   # 🆕
    score_text = font.render(f"Punti: {score}", True, WHITE)               # 🆕
    lives_text = font.render(f"Vite: {'❤' * lives}", True, WHITE)         # 🆕
    surface.blit(score_text, (10, 10))                                     # 🆕
    surface.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))    # 🆕

def draw_game_over(surface, score):                                        # 🆕
    """Disegna la schermata di Game Over."""                                # 🆕
    go_text = font_big.render("GAME OVER", True, RED)                      # 🆕
    score_text = font.render(f"Punteggio finale: {score}", True, WHITE)    # 🆕
    restart_text = font.render("Premi R per ricominciare", True, WHITE)    # 🆕
                                                                           # 🆕
    surface.blit(go_text,                                                  # 🆕
        (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 80))        # 🆕
    surface.blit(score_text,                                               # 🆕
        (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))           # 🆕
    surface.blit(restart_text,                                             # 🆕
        (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))    # 🆕

def reset_game():                                                          # 🆕
    """Resetta tutto il gioco."""                                           # 🆕
    global ball, score, lives, rotation_angle, target_rotation_angle, game_over  # 🆕
    global caught, missed, fade_timer                                      # 🆕
    # Rimuovi la pallina corrente se esiste                                # 🆕
    try:                                                                   # 🆕
        remove_ball(ball)                                                  # 🆕
    except:                                                                # 🆕
        pass                                                               # 🆕
    score = 0                                                              # 🆕
    lives = 3                                                              # 🆕
    rotation_angle = 0.0                                                   # 🆕
    target_rotation_angle = 0.0                                            # 🆕
    game_over = False                                                      # 🆕
    caught = False                                                         # 🆕
    missed = False                                                         # 🆕
    fade_timer = 0                                                         # 🆕
    ball = create_ball()                                                   # 🆕

# --- Game loop aggiornato ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_over:                                                  # 🆕
                if event.key == pygame.K_r:                                # 🆕
                    reset_game()                                           # 🆕
            else:
                if event.key == pygame.K_LEFT:
                    target_rotation_angle += math.pi / 2
                elif event.key == pygame.K_RIGHT:
                    target_rotation_angle -= math.pi / 2

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

    if game_over:                                                          # 🆕
        draw_game_over(screen, score)                                      # 🆕
    else:
        # Logica di gioco
        if caught:
            fade_timer += 1
            progress = min(fade_timer / fade_duration, 1.0)
            sx, sy = ball["catch_pos"]
            cx, cy = BASKET_CENTER
            ball["body"].velocity = (0, 0)
            ball["body"].position = (
                sx + (cx - sx) * progress,
                sy + (cy - sy) * progress
            )
            ball["draw_color"] = lerp_color(ball["color"], DARK_BG, progress)
            ball["draw_radius"] = max(1, int(BALL_RADIUS * (1 - progress)))
            if fade_timer >= fade_duration:
                score += 1
                reset_ball()
        elif missed:
            # Aspetta che la pallina esca dallo schermo                    # 🆕
            bx, by = ball["body"].position                                 # 🆕
            if by > HEIGHT + 50 or bx < -50 or bx > WIDTH + 50:           # 🆕
                lives -= 1
                if lives <= 0:                                             # 🆕
                    game_over = True                                       # 🆕
                else:
                    reset_ball()
        else:
            bx, by = ball["body"].position
            if by > HEIGHT + 50 or bx < -50 or bx > WIDTH + 50:
                lives -= 1
                if lives <= 0:                                             # 🆕
                    game_over = True                                       # 🆕
                else:
                    reset_ball()

        # Disegno
        draw_basket(screen, BASKET_CENTER, BASKET_RADIUS, COLORS, rotation_angle)
        if not game_over:                                                  # 🆕
            draw_color = ball.get("draw_color", ball["color"])
            draw_radius = ball.get("draw_radius", BALL_RADIUS)
            pos = ball["body"].position
            pygame.draw.circle(screen, draw_color,
                               (int(pos.x), int(pos.y)), draw_radius)
        draw_hud(screen, score, lives)                                     # 🆕

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
```

---

## Esercizi extra

Mettiti alla prova con queste modifiche!

### 1. Difficoltà crescente
Man mano che il punteggio sale, aumenta la gravità per far cadere le palline più velocemente.

<details>
<summary>Suggerimento</summary>

Modifica `space.gravity` nel game loop in base allo score. Ad esempio: `space.gravity = (0, 400 + score * 20)`.

</details>

<details>
<summary>Soluzione</summary>

Aggiungi questa riga nel game loop, prima di `space.step()`:

```python
space.gravity = (0, 400 + score * 20)
```

</details>

### 2. Palline più grandi e più piccole
Fai variare casualmente il raggio della pallina tra 10 e 25.

<details>
<summary>Suggerimento</summary>

Usa `random.randint(10, 25)` nella funzione `create_ball()` e salva il raggio nel dizionario.

</details>

<details>
<summary>Soluzione</summary>

Modifica `create_ball()`:

```python
def create_ball():
    color = random.choice(COLORS)
    x = BASKET_CENTER[0]
    radius = random.randint(10, 25)       # 🆕
    mass = 1
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = (x, BALL_START_Y)
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.7
    shape.friction = 0.5
    shape.collision_type = 1
    space.add(body, shape)
    return {"body": body, "shape": shape, "color": color, "radius": radius}  # 🆕
```

E nella sezione di disegno, usa `ball.get("radius", BALL_RADIUS)` al posto di `BALL_RADIUS`.

</details>

### 3. Bonus combo
Se catturi 3 palline consecutive, guadagni una vita extra.

<details>
<summary>Suggerimento</summary>

Aggiungi una variabile `combo` che si incrementa ad ogni cattura e si resetta a 0 quando manchi. Quando `combo` raggiunge 3, aggiungi una vita e resetta il combo.

</details>

<details>
<summary>Soluzione</summary>

Aggiungi `combo = 0` alle variabili di stato, poi:

```python
# Quando la palla è catturata (fade_timer >= fade_duration):
score += 1
combo += 1                        # 🆕
if combo >= 3:                    # 🆕
    lives += 1                    # 🆕
    combo = 0                     # 🆕

# Quando la palla è mancata:
combo = 0                         # 🆕
lives -= 1
```

</details>

### 4. Suoni
Aggiungi un suono quando la palla viene catturata e un suono diverso quando viene mancata.

<details>
<summary>Suggerimento</summary>

Usa `pygame.mixer.Sound("file.wav")` per caricare un suono e `sound.play()` per riprodurlo. Puoi generare suoni semplici con `pygame.sndarray` oppure scaricare file .wav gratuiti.

</details>

### 5. Posizione casuale della pallina
Fai cadere la pallina da posizioni X casuali, non sempre dal centro. Aumenta il range man mano che il punteggio cresce.

<details>
<summary>Suggerimento</summary>

Modifica `create_ball()` per usare un range dipendente dallo score: `x = BASKET_CENTER[0] + random.randint(-range, range)`.

</details>

<details>
<summary>Soluzione</summary>

```python
def create_ball():
    color = random.choice(COLORS)
    x_range = min(score * 5, 150)                                          # 🆕
    x = BASKET_CENTER[0] + random.randint(-x_range, x_range)              # 🆕
    x = max(BALL_RADIUS, min(WIDTH - BALL_RADIUS, x))                     # 🆕
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
```

</details>
