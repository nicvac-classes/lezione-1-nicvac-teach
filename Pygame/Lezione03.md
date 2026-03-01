| Attenzione |
| --- |
| Per leggere correttamente questo documento, click destro su questo file e selezionare Open Preview. |

# Lezione 03 - Color Basket

## Introduzione

In questa lezione costruiremo un piccolo gioco: **Color Basket**.

Una palla colorata cade dall'alto per effetto della gravità. In basso c'è un canestro il cui bordo è diviso in 4 colori. Il giocatore può ruotare il canestro con le frecce direzionali. Se il colore in alto sul canestro corrisponde a quello della palla, la palla entra nel canestro. Altrimenti, rimbalza via!

Utilizzeremo le conoscenze acquisite nelle lezioni precedenti:
- **Lezione 01**: finestra, game loop, gestione eventi, tastiera, frame rate, chiusura
- **Lezione 02**: spazio fisico Pymunk, gravità, body, shape, elasticità, attrito, `space.step()`

E impareremo concetti nuovi:
- Disegnare oggetti personalizzati con le **Surface** trasparenti
- Usare `pygame.draw.arc` per disegnare archi colorati
- Il body **KINEMATIC** (controllabile dal codice, non soggetto a gravità)
- Le **collisioni personalizzate** con maschere di collisione e callback
- La **rotazione** grafica e fisica degli oggetti

---

## Scaletta

| Blocco | Argomento |
|--------|-----------|
| 1 | Scheletro e costanti |
| 2 | Spazio fisico e gravità |
| 3 | Creare la palla: Surface trasparente e colore casuale |
| 4 | Dare fisicità alla palla: body dinamico e shape |
| 5 | Disegnare la palla con `blit` |
| 6 | Creare il canestro: archi colorati con `arc` |
| 7 | Dare fisicità al canestro: body KINEMATIC e maschere di collisione |
| 8 | Disegnare il canestro con rotazione |
| 9 | Ruotare il canestro con le frecce |
| 10 | Gestire le collisioni |
| 11 | Logica di gioco: caught, missed, reset |

---

## Blocco 1 - Scheletro e costanti

### Obiettivo

Ricreare lo scheletro base di un'applicazione Pygame (v. Lezione 01) e definire tutte le **costanti** che useremo nel gioco. Centralizzare i valori in costanti è una buona pratica: se vogliamo cambiare una dimensione o un colore, lo facciamo in un solo punto.

### Ingredienti

Già visti nella Lezione 01:

| Elemento | Descrizione |
|----------|-------------|
| `pygame.init()` | Inizializza Pygame |
| `pygame.display.set_mode((larghezza, altezza))` | Crea la finestra |
| `pygame.display.set_caption("titolo")` | Imposta il titolo |
| `pygame.time.Clock()` | Crea l'orologio per il frame rate |
| `pygame.event.get()` | Recupera gli eventi |
| `pygame.QUIT` | Evento di chiusura finestra |
| `screen.fill((R, G, B))` | Riempie lo sfondo |
| `pygame.display.flip()` | Aggiorna lo schermo |
| `clock.tick(FPS)` | Limita il frame rate |
| `pygame.quit()` / `sys.exit()` | Chiusura pulita |

Nuovo:

| Elemento | Descrizione |
|----------|-------------|
| `import math` | Libreria matematica, ci servirà per angoli e rotazioni |
| `import random` | Per scegliere colori casuali |
| Costanti (`WIDTH`, `HEIGHT`, `FPS`, colori, ecc.) | Valori fissi usati in tutto il programma, definiti una sola volta |
| Notazione binaria `0b01`, `0b10` | Modo comodo per scrivere costanti da usare come maschere di bit per le collisioni |

### Come combinarli

1. Importa `pygame`, `pymunk`, `sys`, `random` e `math`
2. Definisci le costanti per le dimensioni della finestra: `WIDTH, HEIGHT = 600, 700` e `FPS = 60`
3. Definisci i 4 colori come tuple RGB:
   - `RED = (220, 50, 50)`
   - `GREEN = (50, 200, 50)`
   - `BLUE = (50, 100, 220)`
   - `YELLOW = (240, 220, 50)`
   - `DARK_BG = (30, 30, 50)` per lo sfondo
   - `COLORS = [RED, GREEN, BLUE, YELLOW]` — la lista dei colori
4. Definisci le costanti per la palla: `BALL_RADIUS = 15` e `BALL_START_Y = 50`
5. Definisci le costanti per il canestro:
   - `BASKET_CENTER = (WIDTH // 2, HEIGHT - 150)` — posizione al centro in basso
   - `BASKET_RADIUS = BALL_RADIUS * 1.9` — proporzionato alla pallina (come nella NBA, il rapporto canestro/palla è circa 1.9)
   - `BASKET_ROTATION_STEP = math.pi / 20` — velocità di rotazione in radianti per frame
6. Definisci le costanti per le collisioni usando la **notazione binaria**:
   - `COLLISION_TYPE_BALL = 0b01` — bit 0
   - `COLLISION_TYPE_BASKET = 0b10` — bit 1
   
   La notazione `0b...` è comoda perché ogni oggetto ha un singolo bit attivo: questo torna utile quando useremo le maschere di collisione (ogni bit rappresenta una "categoria").
7. Inizializza Pygame con finestra, caption e clock (v. Lezione 01)
8. Scrivi il game loop base: gestione `QUIT`, `screen.fill(DARK_BG)`, `pygame.display.flip()`, `clock.tick(FPS)`
9. Chiusura pulita con `pygame.quit()` e `sys.exit()`

### Esercizio

Scrivi lo scheletro completo con tutte le costanti elencate sopra. Esegui il programma: dovresti vedere una finestra 600x700 con sfondo scuro.

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

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

RED    = (220, 50, 50)
GREEN  = (50, 200, 50)
BLUE   = (50, 100, 220)
YELLOW = (240, 220, 50)
DARK_BG = (30, 30, 50)

COLORS = [RED, GREEN, BLUE, YELLOW]

BALL_RADIUS = 15
BALL_START_Y = 50

BASKET_CENTER = (WIDTH // 2, HEIGHT - 150)
BASKET_RADIUS = BALL_RADIUS * 1.9
BASKET_ROTATION_STEP = math.pi / 20

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

# ============================================================
# GAME LOOP
# ============================================================
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

## Blocco 2 - Spazio fisico e gravità

### Obiettivo

Aggiungere lo spazio fisico Pymunk con la gravità, come fatto nella Lezione 02.

### Ingredienti (v. Lezione 02)

| Elemento | Descrizione |
|----------|-------------|
| `pymunk.Space()` | Crea lo spazio fisico |
| `space.gravity = (x, y)` | Imposta la gravità. Un valore positivo in y spinge verso il basso |

### Come combinarli

1. Dopo l'inizializzazione di Pygame, crea lo spazio fisico con `pymunk.Space()` e salvalo in `space`
2. Imposta la gravità: `space.gravity = (0, 500)`
3. Nel game loop, aggiungi `space.step(1 / FPS)` per far avanzare la simulazione (v. Lezione 02)

### Esercizio

Partendo dal codice del Blocco 1, aggiungi lo spazio fisico e la gravità.

Esegui il programma. Non vedrai nulla di diverso: lo spazio fisico è pronto ma vuoto. Lo riempiremo nei prossimi blocchi!

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

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

RED    = (220, 50, 50)
GREEN  = (50, 200, 50)
BLUE   = (50, 100, 220)
YELLOW = (240, 220, 50)
DARK_BG = (30, 30, 50)

COLORS = [RED, GREEN, BLUE, YELLOW]

BALL_RADIUS = 15
BALL_START_Y = 50

BASKET_CENTER = (WIDTH // 2, HEIGHT - 150)
BASKET_RADIUS = BALL_RADIUS * 1.9
BASKET_ROTATION_STEP = math.pi / 20

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
space = pymunk.Space()                                # 🆕
space.gravity = (0, 500)                              # 🆕

# ============================================================
# GAME LOOP
# ============================================================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(DARK_BG)

    # Aggiorno la fisica
    space.step(1 / FPS)                               # 🆕

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
```

</details>

---

## Blocco 3 - Creare la palla: Surface trasparente e colore casuale

### Obiettivo

Creare l'aspetto grafico della palla: un cerchio colorato su una **Surface trasparente**. In Lezione 02 usavamo `debug_draw` per disegnare automaticamente gli oggetti Pymunk. Ora disegniamo noi, in modo da avere il pieno controllo su colori e aspetto.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `pygame.Surface((larghezza, altezza), pygame.SRCALPHA)` | Crea una superficie con sfondo **trasparente**. È come un foglio lucido su cui disegniamo. |
| `pygame.draw.circle(surface, colore, centro, raggio)` | Disegna un cerchio su una surface (v. Lezione 01, ma ora su una surface dedicata e non sullo schermo) |
| `random.choice(lista)` | Sceglie un elemento casuale da una lista |

### Come combinarli

Creiamo una funzione `create_ball()` che per ora si occupa solo dell'aspetto grafico (la fisica la aggiungeremo nel blocco successivo):

1. Calcola `size = BALL_RADIUS * 2` e `center = (size//2, size//2)`
2. Crea una Surface quadrata di dimensione `size x size` con `pygame.SRCALPHA` per la trasparenza
3. Scegli un colore casuale dalla lista `COLORS` con `random.choice(COLORS)`
4. Disegna un cerchio pieno sulla surface con `pygame.draw.circle()`
5. Restituisci un dizionario con le informazioni della palla: `{"surface": ball_surface, "color": color}`

### Esercizio

Crea la funzione `create_ball()` come descritto sopra e chiamala per creare la prima palla: `ball = create_ball()`.

Esegui il programma. Non vedrai ancora la palla: l'abbiamo creata ma non disegnata sullo schermo. Lo faremo nel Blocco 5!

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

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

RED    = (220, 50, 50)
GREEN  = (50, 200, 50)
BLUE   = (50, 100, 220)
YELLOW = (240, 220, 50)
DARK_BG = (30, 30, 50)

COLORS = [RED, GREEN, BLUE, YELLOW]

BALL_RADIUS = 15
BALL_START_Y = 50

BASKET_CENTER = (WIDTH // 2, HEIGHT - 150)
BASKET_RADIUS = BALL_RADIUS * 1.9
BASKET_ROTATION_STEP = math.pi / 20

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

# Palla
def create_ball():                                                # 🆕
    """Crea una pallina con colore casuale che cade dall'alto."""  # 🆕
    # DISEGNO                                                     # 🆕
    # Creo la superficie di disegno dell'oggetto                  # 🆕
    size = BALL_RADIUS * 2                                        # 🆕
    center = (size//2, size//2)                                   # 🆕
    ball_surface = pygame.Surface((size,size), pygame.SRCALPHA)   # 🆕
    # Disegno la palla con un colore random                       # 🆕
    color = random.choice(COLORS)                                 # 🆕
    pygame.draw.circle(ball_surface, color, center, BALL_RADIUS)  # 🆕
                                                                  # 🆕
    return {"surface": ball_surface, "color": color}              # 🆕

# Crea la prima palla
ball = create_ball()                                              # 🆕

# ============================================================
# GAME LOOP
# ============================================================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(DARK_BG)

    # Aggiorno la fisica
    space.step(1 / FPS)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
```

</details>

---

## Blocco 4 - Dare fisicità alla palla: body dinamico e shape

### Obiettivo

Aggiungere il **body** e la **shape** alla palla, in modo che Pymunk ne gestisca il movimento e le collisioni (v. Lezione 02). Usamo anche una **maschera di collisione** per controllare con quali altri oggetti la palla interagisce fisicamente.

### Ingredienti (v. Lezione 02)

| Elemento | Descrizione |
|----------|-------------|
| `pymunk.moment_for_circle(mass, inner, outer)` | Calcola il momento d'inerzia per un cerchio |
| `pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)` | Crea un body **dinamico** (soggetto a gravità). Il tipo DYNAMIC è quello di default, ma specificarlo esplicitamente rende il codice più leggibile. |
| `body.position = (x, y)` | Imposta la posizione iniziale |
| `pymunk.Circle(body, radius)` | Crea una shape circolare associata al body |
| `shape.elasticity` | Quanto rimbalza (0 = niente, 1 = perfetto) |
| `shape.friction` | Quanto attrito ha |
| `shape.collision_type` | Un intero che identifica il "tipo" dell'oggetto per le collisioni |
| `shape.filter = pymunk.ShapeFilter(categories=..., mask=...)` | **Maschera di collisione**: `categories` è il "tipo" della shape, `mask` è l'insieme dei tipi con cui interagisce fisicamente. Si usano valori binari: la collisione avviene solo se `categories` dell'uno ha bit in comune con `mask` dell'altro. |
| `space.add(body, shape)` | Aggiunge body e shape allo spazio fisico |

### Come combinarli

Aggiungiamo la parte fisica alla funzione `create_ball()`:

1. Dopo il disegno, crea il body:
   - `mass = 1`
   - Calcola il momento con `pymunk.moment_for_circle(mass, 0, BALL_RADIUS)`
   - Crea il body con `pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)`
   - Imposta la posizione: `ball_body.position = (BASKET_CENTER[0], BALL_START_Y)` — la palla parte centrata sopra il canestro
2. Crea la shape:
   - `pymunk.Circle(ball_body, BALL_RADIUS)`
   - `shape.elasticity = 0.7`
   - `shape.friction = 0.5`
   - `shape.collision_type = COLLISION_TYPE_BALL`
   - `shape.filter = pymunk.ShapeFilter(categories=COLLISION_TYPE_BALL, mask=COLLISION_TYPE_BALL | COLLISION_TYPE_BASKET)` — la palla interagisce fisicamente sia con altre palle che con il canestro
3. Aggiungi body e shape allo spazio con `space.add(body, shape)`
4. Aggiungi `"body": ball_body` e `"shape": ball_shape` al dizionario restituito

### Esercizio

Modifica la funzione `create_ball()` aggiungendo body, shape e maschera di collisione come descritto.

Esegui il programma. Ancora niente di visibile: la palla cade nello spazio fisico, ma non la stiamo ancora disegnando sullo schermo!

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
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

    # BODY                                                                    # 🆕
    # Definiamo il Body della palla (oggetto fisico)                          # 🆕
    # DYNAMIC: soggetto alla gravità, interagisce con gli altri body          # 🆕
    mass = 1                                                                  # 🆕
    moment = pymunk.moment_for_circle(mass, 0, BALL_RADIUS)                   # 🆕
    ball_body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)      # 🆕
    ball_body.position = (BASKET_CENTER[0], BALL_START_Y)                     # 🆕
                                                                              # 🆕
    # SHAPE                                                                   # 🆕
    # Definiamo la forma fisica                                               # 🆕
    ball_shape = pymunk.Circle(ball_body, BALL_RADIUS)                        # 🆕
    ball_shape.elasticity = 0.7                                               # 🆕
    ball_shape.friction = 0.5                                                 # 🆕
    ball_shape.collision_type = COLLISION_TYPE_BALL                            # 🆕
    # mask: oggetti con cui interagire fisicamente                             # 🆕
    ball_shape.filter = pymunk.ShapeFilter(categories=COLLISION_TYPE_BALL,    # 🆕
                                           mask=COLLISION_TYPE_BALL | COLLISION_TYPE_BASKET)  # 🆕
                                                                              # 🆕
    # Aggiungo la palla allo spazio fisico                                    # 🆕
    space.add(ball_body, ball_shape)                                          # 🆕

    return {"body": ball_body, "shape": ball_shape, "surface": ball_surface, "color": color}  # 🆕
```

</details>

---

## Blocco 5 - Disegnare la palla con `blit`

### Obiettivo

Rendere finalmente visibile la palla! Impariamo a usare `blit` per disegnare una Surface sullo schermo, nella posizione gestita da Pymunk.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `surface.get_rect(center=posizione)` | Crea un rettangolo di riferimento centrato sulla posizione data. Serve per posizionare la surface. |
| `screen.blit(surface, rect)` | **Disegna** (incolla) una surface sullo schermo nella posizione del rettangolo |

### Come combinarli

Creiamo una funzione `draw_ball(screen, ball)`:

1. Recupera il body e la surface dal dizionario `ball`
2. Calcola il rettangolo di posizionamento: `rect_new = ball_surface.get_rect(center=ball_body.position)`
   - `ball_body.position` è aggiornata da Pymunk ad ogni `space.step()`
   - `get_rect(center=...)` crea un riquadro centrato su quel punto
3. Disegna la surface sullo schermo: `screen.blit(ball_surface, rect_new)`
4. Nel game loop, dopo `screen.fill()`, chiama `draw_ball(screen, ball)`

### Esercizio

Crea la funzione `draw_ball()` e chiamala nel game loop.

Esegui il programma. Finalmente! La palla colorata cade e... scompare fuori dallo schermo. Non c'è ancora nulla su cui rimbalzare!

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
def draw_ball( screen, ball):                                     # 🆕
    ball_body = ball["body"]                                      # 🆕
    ball_surface = ball["surface"]                                # 🆕
    # Calcolo il nuovo riquadro da disegnare                      # 🆕
    rect_new = ball_surface.get_rect(center=ball_body.position)   # 🆕
    # Scrivo la surface nel nuovo riquadro                        # 🆕
    screen.blit(ball_surface, rect_new)                           # 🆕
```

E nel game loop:

```python
    screen.fill(DARK_BG)

    # Aggiorno la fisica
    space.step(1 / FPS)

    # --- Disegno gli oggetti ---
    draw_ball(screen, ball)                                       # 🆕

    pygame.display.flip()
    clock.tick(FPS)
```

</details>

---

## Blocco 6 - Creare il canestro: archi colorati con `arc`

### Obiettivo

Creare l'aspetto grafico del canestro: un cerchio formato da 4 archi colorati, con l'interno scuro. Ogni arco copre 90° (un quarto di cerchio).

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `pygame.draw.arc(surface, colore, rect, angolo_inizio, angolo_fine, spessore)` | Disegna un arco di cerchio. Gli angoli sono in **radianti**. L'angolo 0 è a destra (ore 3) e cresce in **senso antiorario**. |
| `math.pi` | Il valore di π (≈ 3.14159). Un giro completo = 2π. Un quarto di giro = π/2. |
| `surface.get_rect()` | Restituisce il rettangolo che contiene la surface. Serve come area di disegno per `arc`. |

### Come combinarli

Creiamo una funzione `create_basket()` — per ora solo la parte grafica:

1. Calcola `size = BASKET_RADIUS * 2` e `center = (size//2, size//2)`
2. Crea una Surface quadrata con `pygame.SRCALPHA` (sfondo trasparente)
3. Disegna i 4 archi colorati con un ciclo `for`:
   - Ogni arco copre `angle_step = math.pi / 2` (90°)
   - L'angolo di partenza è `angle_start = math.pi / 4` (45°), così il primo colore è in alto
   - Per ogni colore: disegna l'arco con `pygame.draw.arc()`, spessore 8
   - Dopo ogni arco: sposta `angle_start` e `angle_stop` avanti di 90°
4. Disegna l'interno del canestro con `pygame.draw.circle()` in colore `DARK_BG` e raggio `BASKET_RADIUS - 8`
5. Restituisci un dizionario: `{"surface": basket_surface}`

### Esercizio

Crea la funzione `create_basket()` e chiamala: `basket = create_basket()`.

Esegui il programma. Non vedrai ancora il canestro: lo disegneremo sullo schermo nel Blocco 8.

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
# Canestro
def create_basket():                                                                      # 🆕
    # DISEGNO                                                                             # 🆕
    # Creo la superficie di disegno dell'oggetto                                          # 🆕
    size = BASKET_RADIUS * 2                                                              # 🆕
    center = (size//2, size//2)                                                           # 🆕
    basket_surface = pygame.Surface((size,size), pygame.SRCALPHA)                         # 🆕
    # Disegna il canestro con i 4 colori, il primo colore in alto                         # 🆕
    #L'angolo 0 è alle ore 15:00 e cresce in senso antiorario                            # 🆕
    angle_step = math.pi/2                                                                # 🆕
    angle_start = math.pi/4                                                               # 🆕
    angle_stop  = angle_start + angle_step                                                # 🆕
    for i in range(4):                                                                    # 🆕
        pygame.draw.arc(basket_surface, COLORS[i], basket_surface.get_rect(), angle_start, angle_stop, 8 )  # 🆕
        angle_start = angle_stop                                                          # 🆕
        angle_stop += angle_step                                                          # 🆕
    # Interno del canestro                                                                # 🆕
    pygame.draw.circle(basket_surface, DARK_BG, center, BASKET_RADIUS - 8)                # 🆕
                                                                                          # 🆕
    return {"surface": basket_surface}                                                    # 🆕
```

E subito prima della creazione della palla:

```python
# Crea il canestro
basket = create_basket()                                                                  # 🆕
# Crea la prima palla
ball = create_ball()
```

</details>

---

## Blocco 7 - Dare fisicità al canestro: body KINEMATIC e maschere di collisione

### Obiettivo

Aggiungere un body e una shape al canestro. A differenza della palla, il canestro:
- Non deve cadere → useremo un body **KINEMATIC** (controllabile dal codice, non soggetto a gravità)
- Deve interagire fisicamente con la palla (rimbalzarla) ma solo in certi casi → useremo le **maschere di collisione** (`ShapeFilter`) per controllare quali oggetti interagiscono tra loro

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `pymunk.Body(body_type=pymunk.Body.KINEMATIC)` | Crea un body **cinematico**: non è soggetto a gravità né a forze, ma può essere mosso dal codice (posizione, rotazione, velocità). |
| `shape.elasticity` | Quanto rimbalza la shape (0 = niente, 1 = perfetto) |
| `shape.collision_type = intero` | Assegna un "tipo" alla shape per identificarla nelle collisioni |
| `shape.filter = pymunk.ShapeFilter(categories=..., mask=...)` | **Maschera di collisione**: `categories` è il "tipo" della shape, `mask` specifica con quali categorie interagisce. La collisione fisica avviene solo se i bit di `categories` di un oggetto coincidono con i bit di `mask` dell'altro. |

### Come combinarli

Aggiungiamo la parte fisica alla funzione `create_basket()`:

1. Crea il body cinematico: `pymunk.Body(body_type=pymunk.Body.KINEMATIC)`
2. Imposta la posizione: `basket_body.position = BASKET_CENTER`
3. Crea la shape circolare: `pymunk.Circle(basket_body, BASKET_RADIUS)`
4. Imposta l'elasticità: `basket_shape.elasticity = 0.4`
5. Assegna il tipo di collisione: `basket_shape.collision_type = COLLISION_TYPE_BASKET`
6. Imposta la maschera di collisione: `basket_shape.filter = pymunk.ShapeFilter(categories=COLLISION_TYPE_BASKET, mask=COLLISION_TYPE_BALL)` — il canestro interagisce fisicamente solo con la palla
7. Aggiungi body e shape allo spazio: `space.add(basket_body, basket_shape)`
8. Aggiungi `"body"` e `"shape"` al dizionario restituito

**Nota:** La palla interagisce fisicamente con il canestro (rimbalza) finché la sua maschera include `COLLISION_TYPE_BASKET`. Quando vorremo far passare la palla attraverso il canestro (palla "caught"), cambieremo la maschera della palla nel callback, escludendo il canestro.

### Esercizio

Modifica la funzione `create_basket()` aggiungendo body KINEMATIC, shape con elasticità e maschere di collisione.

Esegui il programma. Ancora nessuna differenza visiva: il canestro esiste nello spazio fisico ma non lo stiamo disegnando. Prossimo blocco!

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
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

    # BODY                                                                    # 🆕
    # Definiamo il Body del canestro (oggetto fisico)                         # 🆕
    # KINEMATIC: non soggetto alla gravità, interagisce con gli altri body    # 🆕
    basket_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)                # 🆕
    basket_body.position = BASKET_CENTER                                      # 🆕
                                                                              # 🆕
    # SHAPE                                                                   # 🆕
    # Definiamo la forma fisica                                               # 🆕
    basket_shape = pymunk.Circle(basket_body, BASKET_RADIUS)                  # 🆕
    basket_shape.elasticity = 0.4                                             # 🆕
    basket_shape.collision_type = COLLISION_TYPE_BASKET                        # 🆕
    # mask: oggetti con cui interagire fisicamente                             # 🆕
    basket_shape.filter = pymunk.ShapeFilter(categories=COLLISION_TYPE_BASKET, # 🆕
                                             mask=COLLISION_TYPE_BALL)         # 🆕
                                                                              # 🆕
    # Aggiungo il canestro allo spazio fisico                                 # 🆕
    space.add(basket_body, basket_shape)                                      # 🆕

    return {"body": basket_body, "shape": basket_shape, "surface": basket_surface}  # 🆕
```

</details>

---

## Blocco 8 - Disegnare il canestro con rotazione

### Obiettivo

Disegnare il canestro sullo schermo. Poiché il canestro ruoterà, dobbiamo ruotare la surface grafica in base all'angolo fisico del body.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `math.degrees(radianti)` | Converte un angolo da radianti a gradi (Pygame usa i gradi per le rotazioni grafiche) |
| `pygame.transform.rotate(surface, angolo_gradi)` | Restituisce una **nuova** surface ruotata dell'angolo specificato. L'originale non viene modificata. |
| `surface.get_rect(center=posizione)` | Calcola il rettangolo centrato sulla posizione (già visto nel Blocco 5) |
| `screen.blit(surface, rect)` | Disegna la surface sullo schermo (già visto nel Blocco 5) |
| `body.angle` | L'angolo corrente del body in **radianti**, aggiornato da Pymunk |

### Come combinarli

Creiamo una funzione `draw_basket(screen, basket)`:

1. Recupera body e surface dal dizionario `basket`
2. Converti l'angolo del body in gradi: `angle_deg = math.degrees(basket_body.angle)`
3. Ruota la surface: `surface_rotated = pygame.transform.rotate(basket_surface, angle_deg)`
4. Calcola il rettangolo centrato sulla posizione del body: `rect_new = surface_rotated.get_rect(center=basket_body.position)`
5. Disegna sullo schermo: `screen.blit(surface_rotated, rect_new)`
6. Nel game loop, chiama `draw_basket(screen, basket)` prima di `draw_ball(screen, ball)`

### Esercizio

Crea la funzione `draw_basket()` e chiamala nel game loop.

Esegui il programma. Ora vedi il canestro con i 4 colori e la palla che cade! La palla rimbalza sul bordo del canestro perché la shape del canestro interagisce fisicamente con la palla. Vedremo nel Blocco 10 come far passare la palla attraverso il canestro quando il colore è corretto.

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
def draw_basket(screen, basket):                                                          # 🆕
    """Ruota la superficie pre-disegnata in base all'angolo del body e la disegna."""      # 🆕
    basket_body = basket["body"]                                                          # 🆕
    basket_surface = basket["surface"]                                                    # 🆕
    # Ridisegno il canestro, considerando la rotazione corrente di basket_body             # 🆕
    angle_deg = math.degrees(basket_body.angle) # da radianti a gradi                     # 🆕
    surface_rotated = pygame.transform.rotate(basket_surface, angle_deg)                  # 🆕
    # Calcolo il nuovo riquadro da disegnare                                              # 🆕
    rect_new = surface_rotated.get_rect(center=basket_body.position)                      # 🆕
    # Scrivo la surface ridisegnata nel nuovo riquadro                                    # 🆕
    screen.blit(surface_rotated, rect_new)                                                # 🆕
```

E nel game loop:

```python
    # --- Disegno gli oggetti ---
    draw_basket(screen, basket)                                   # 🆕
    draw_ball(screen, ball)
```

</details>

---

## Blocco 9 - Ruotare il canestro con le frecce

### Obiettivo

Permettere al giocatore di ruotare il canestro di 90° premendo le frecce SX e DX. La rotazione deve essere **smooth** (fluida), non istantanea.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `pygame.KEYDOWN` | Evento che scatta quando si **preme** un tasto (v. Lezione 01, dove usavamo `get_pressed()` per la pressione continua; qui ci basta il singolo evento) |
| `event.key` | Il tasto premuto nell'evento `KEYDOWN` |
| `pygame.K_LEFT` / `pygame.K_RIGHT` | Costanti per le frecce (v. Lezione 01) |
| `body.angular_velocity` | Velocità angolare del body in radianti/secondo. Pymunk ruota il body automaticamente. |
| `body.angle` | Angolo corrente del body in radianti |

### Come combinarli

Usiamo una tecnica di **rotazione smooth**: quando il giocatore preme un tasto, impostiamo una velocità angolare e un angolo di arrivo. Ad ogni frame, controlliamo se abbiamo raggiunto l'angolo target e in quel caso fermiamo la rotazione.

1. Prima del game loop, crea le variabili di stato:
   - `basket_body = basket["body"]` — riferimento al body del canestro
   - `basket_top_color_index = 0` — indice del colore attualmente in alto (inizia da `COLORS[0]`)
   - `target_rotation_angle = 0.0` — angolo target a cui il canestro deve arrivare
2. Nel ciclo degli eventi, intercetta `pygame.KEYDOWN`:
   - **Freccia SX**: rotazione antioraria
     - `target_rotation_angle += math.pi / 2` (aggiungi 90°)
     - `basket_body.angular_velocity = BASKET_ROTATION_STEP * FPS` (velocità positiva)
     - `basket_top_color_index = (basket_top_color_index - 1) % 4` (colore precedente nella lista)
   - **Freccia DX**: rotazione oraria
     - `target_rotation_angle -= math.pi / 2` (togli 90°)
     - `basket_body.angular_velocity = -BASKET_ROTATION_STEP * FPS` (velocità negativa)
     - `basket_top_color_index = (basket_top_color_index + 1) % 4` (colore successivo nella lista)
3. Nel game loop, dopo `space.step()`, aggiungi il controllo di arrivo:
   - Calcola `diff = target_rotation_angle - basket_body.angle`
   - Se `abs(diff) <= BASKET_ROTATION_STEP`: il canestro è arrivato! Imposta `basket_body.angle = target_rotation_angle` e `basket_body.angular_velocity = 0`

### Esercizio

Aggiungi la gestione dei tasti e la rotazione smooth al game loop.

Esegui il programma. Premi le frecce SX e DX: il canestro ruota in modo fluido di 90° alla volta! La palla rimbalza sul bordo del canestro.

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

Prima del game loop:

```python
# Crea il canestro
basket = create_basket()
# Crea la prima palla
ball = create_ball()

# ============================================================
# GAME LOOP
# ============================================================
basket_body = basket["body"]                          # 🆕
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:                                      # 🆕
            if event.key == pygame.K_LEFT:                                    # 🆕
                target_rotation_angle += math.pi / 2                          # 🆕
                basket_body.angular_velocity = BASKET_ROTATION_STEP * FPS     # 🆕
                basket_top_color_index = (basket_top_color_index - 1) % 4     # 🆕
            elif event.key == pygame.K_RIGHT:                                 # 🆕
                target_rotation_angle -= math.pi / 2                          # 🆕
                basket_body.angular_velocity = -BASKET_ROTATION_STEP * FPS    # 🆕
                basket_top_color_index = (basket_top_color_index + 1) % 4     # 🆕

    screen.fill(DARK_BG)

    # Aggiorno la fisica
    space.step(1 / FPS)

    # --- Rotazione smooth via pymunk ---
    if basket_body.angular_velocity != 0:                                     # 🆕
        diff = target_rotation_angle - basket_body.angle                      # 🆕
        if abs(diff) <= BASKET_ROTATION_STEP:                                 # 🆕
            basket_body.angle = target_rotation_angle                         # 🆕
            basket_body.angular_velocity = 0                                  # 🆕

    # --- Disegno gli oggetti ---
    draw_basket(screen, basket)
    draw_ball(screen, ball)

    pygame.display.flip()
    clock.tick(FPS)
```

**Nota:** `basket_top_color_index` e `target_rotation_angle` non sono ancora definiti qui perché li introdurremo nel prossimo blocco insieme al collision handler. Per ora, aggiungili temporaneamente prima del game loop:

```python
basket_top_color_index = 0
target_rotation_angle = 0.0
```

</details>

---

## Blocco 10 - Gestire le collisioni

### Obiettivo

Quando la palla tocca il canestro, vogliamo sapere se il colore corrisponde. Se sì, la palla "entra" nel canestro: modifichiamo la sua maschera di collisione in modo che non interagisca più fisicamente con il canestro e poi la rallentiamo. Se no, la palla "rimbalza via" con una spinta laterale.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `space.on_collision(type_a, type_b, begin=callback)` | Registra una funzione **callback** che viene chiamata quando due shape con i `collision_type` specificati si toccano |
| `def callback(arbiter, space, data)` | La firma della funzione callback. `arbiter` contiene info sulla collisione. |
| `shape.filter = pymunk.ShapeFilter(categories=..., mask=...)` | Cambia dinamicamente la maschera di collisione di una shape. Modificando `mask` possiamo far sì che la palla non interagisca più fisicamente con il canestro (la attraversa). |
| `body.velocity = (vx, vy)` | Imposta direttamente la velocità di un body |
| `body.apply_impulse_at_local_point((ix, iy))` | Applica un impulso (forza istantanea) al body nel suo sistema di riferimento locale |
| `random.choice([-1, 1])` | Sceglie casualmente una direzione (sinistra o destra) |

### Come combinarli

1. Crea due variabili globali: `caught = False` e `missed = False`
2. Sposta `basket_top_color_index = 0` e `target_rotation_angle = 0.0` qui — ora servono anche al callback
3. Crea la funzione callback `on_ball_enter_basket(arbiter, space, data)`:
   - Recupera il colore in alto al canestro: `basket_top_color = COLORS[basket_top_color_index]`
   - Usa `global caught, missed` per accedere alle variabili globali
   - Se `caught` o `missed` sono già `True`, la collisione è già stata gestita: ritorna `True` (ignora)
   - Se il colore della palla corrisponde al colore del canestro:
     - `caught = True`
     - Modifica la maschera della palla escludendo il canestro: `ball["shape"].filter = pymunk.ShapeFilter(categories=COLLISION_TYPE_BALL, mask=COLLISION_TYPE_BALL)` — così la palla non interagisce più fisicamente con il canestro e lo attraversa
     - Rallenta la palla: `ball["body"].velocity = (0, 80)`
   - Altrimenti:
     - `missed = True`
     - Fai rimbalzare la palla lateralmente con un impulso: scegli una direzione casuale e applica `ball["body"].apply_impulse_at_local_point((direction * 100, 0))`
   - Ritorna `False`
4. Registra il callback: `space.on_collision(COLLISION_TYPE_BALL, COLLISION_TYPE_BASKET, begin=on_ball_enter_basket)`
5. Posiziona tutto **prima** della creazione del canestro e della palla

### Esercizio

Aggiungi le variabili globali, la funzione callback e la registrazione del collision handler.

Esegui il programma. Ora quando la palla tocca il canestro: se il colore corrisponde, la maschera di collisione cambia e la palla attraversa il canestro e scende; se non corrisponde, la palla riceve un impulso laterale e rimbalza via! Però la palla non torna... lo risolviamo nel prossimo blocco.

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

Posiziona questa sezione **prima** della creazione di canestro e palla:

```python
# ============================================================
# COLLISION HANDLER
# ============================================================
caught = False # La palla entra nel canestro                      # 🆕
missed = False # La palla non entra nel canestro                  # 🆕
basket_top_color_index = 0  # indice del colore in alto al canestro  # 🆕
target_rotation_angle = 0.0 # angolo attuale del canestro         # 🆕


def on_ball_enter_basket(arbiter, space, data):                   # 🆕
    """Callback: la pallina ha toccato il canestro."""             # 🆕
                                                                  # 🆕
    # Colore del canestro                                         # 🆕
    basket_top_color = COLORS[basket_top_color_index]             # 🆕
                                                                  # 🆕
    global caught, missed                                         # 🆕
    if caught or missed:                                          # 🆕
        return True                                               # 🆕
                                                                  # 🆕
    if ball["color"] == basket_top_color:                          # 🆕
        caught = True                                             # 🆕
        # Modificando la maschera di collisione, la pallina non   # 🆕
        # interagisce più con il canestro, attraversandolo        # 🆕
        ball["shape"].filter = pymunk.ShapeFilter(                # 🆕
            categories=COLLISION_TYPE_BALL,                       # 🆕
            mask=COLLISION_TYPE_BALL)                             # 🆕
        ball["body"].velocity = (0, 80)   # rallenta la pallina   # 🆕
    else:                                                         # 🆕
        missed = True                                             # 🆕
        # Applico una forza su x per far rimbalzare la pallina lateralmente  # 🆕
        direction = random.choice([-1, 1])                        # 🆕
        ball["body"].apply_impulse_at_local_point((direction * 100, 0))  # 🆕
                                                                  # 🆕
    return False                                                  # 🆕

space.on_collision(COLLISION_TYPE_BALL, COLLISION_TYPE_BASKET,     # 🆕
                   begin=on_ball_enter_basket)                     # 🆕


# Crea il canestro
basket = create_basket()
# Crea la prima palla
ball = create_ball()
```

**Nota:** Rimuovi le definizioni temporanee di `basket_top_color_index` e `target_rotation_angle` che avevi aggiunto nel Blocco 9 — ora sono qui.

</details>

---

## Blocco 11 - Logica di gioco: caught, missed, reset

### Obiettivo

Completare il gioco: quando la palla entra nel canestro o rimbalza fuori schermo, creare automaticamente una nuova palla.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `space.remove(shape, body)` | Rimuove un oggetto dallo spazio fisico |
| `body.position.x`, `body.position.y` | Coordinate correnti del body |

### Come combinarli

1. Crea una funzione `reset_ball(ball)`:
   - Usa `global caught, missed` per accedere alle variabili globali
   - Resetta: `caught = False`, `missed = False`
   - Rimuove la palla corrente dallo spazio fisico con `space.remove(ball["shape"], ball["body"])`
   - Crea e restituisce una nuova palla con `create_ball()`
2. Nel game loop, dopo la rotazione smooth, aggiungi la logica di gioco:
   - Se `caught` è `True`: la palla sta entrando nel canestro. Quando la sua posizione y supera `BASKET_CENTER[1]` (il centro del canestro), fai il reset: `ball = reset_ball(ball)`
   - Se `missed` è `True`: la palla è rimbalzata via. Quando esce dallo schermo (y > HEIGHT + 50, o x < -50, o x > WIDTH + 50), fai il reset
   - Altrimenti (nessuna collisione): se la palla cade oltre HEIGHT + 50 senza toccare il canestro, fai il reset

### Esercizio

Crea la funzione `reset_ball()` e aggiungi la logica di gioco nel game loop.

Esegui il programma. Il gioco è completo! Le palle cadono con colori casuali, puoi ruotare il canestro con le frecce e, colore giusto o sbagliato, una nuova palla appare ogni volta.

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

La funzione `reset_ball()` va aggiunta tra le funzioni di creazione/disegno:

```python
def reset_ball(ball):                                             # 🆕
    """Rimuove la pallina corrente e ne crea una nuova."""        # 🆕
    global caught, missed                                         # 🆕
    caught = False                                                # 🆕
    missed = False                                                # 🆕
                                                                  # 🆕
    # Rimuove la palla dallo spazio fisico.                       # 🆕
    space.remove(ball["shape"], ball["body"])                      # 🆕
    # Ritorna la nuova palla                                      # 🆕
    return create_ball()                                          # 🆕
```

E nel game loop, dopo la rotazione smooth:

```python
    # --- Logica di gioco ---
    if caught:                                                    # 🆕
        # La pallina continua a cadere; quando supera il centro del canestro, reset  # 🆕
        by = ball["body"].position.y                              # 🆕
        if by >= BASKET_CENTER[1]:                                # 🆕
            ball = reset_ball(ball)                                # 🆕
    elif missed:                                                  # 🆕
        # Aspetta che la pallina esca dallo schermo, poi crea una nuova  # 🆕
        bx, by = ball["body"].position                            # 🆕
        if by > HEIGHT + 50 or bx < -50 or bx > WIDTH + 50:      # 🆕
            ball = reset_ball(ball)                                # 🆕
    else:                                                         # 🆕
        # Pallina uscita dallo schermo senza toccare il canestro  # 🆕
        bx, by = ball["body"].position                            # 🆕
        if by > HEIGHT + 50:                                      # 🆕
            ball = reset_ball(ball)                                # 🆕
```

</details>

---

## Codice completo finale

Ecco il programma completo che abbiamo costruito passo dopo passo:

<details>
<summary>Apri per vedere il codice completo</summary>

```python
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
```

</details>

---

## Esercizi extra

Prova a modificare il programma per aggiungere queste funzionalità:

### 1. Punteggio a schermo
Aggiungi un contatore di palle catturate e mostralo in alto a sinistra.

<details>
<summary>Suggerimento</summary>

Usa `pygame.font.SysFont("Arial", 30)` per creare un font e `font.render(f"Score: {score}", True, (255,255,255))` per trasformarlo in una surface da disegnare con `blit`.

</details>

<details>
<summary>Soluzione</summary>

Aggiungi prima del game loop:

```python
font = pygame.font.SysFont("Arial", 30)
score = 0
```

In `reset_ball()`, prima di resettare `caught`:

```python
global score
if caught:
    score += 1
```

Nel game loop, dopo aver disegnato palla e canestro:

```python
score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
screen.blit(score_surface, (10, 10))
```

</details>

### 2. Velocità crescente
Fai in modo che la gravità aumenti leggermente dopo ogni palla catturata, rendendo il gioco progressivamente più difficile.

<details>
<summary>Suggerimento</summary>

Modifica `space.gravity` in `reset_ball()` quando `caught` è `True`.

</details>

<details>
<summary>Soluzione</summary>

In `reset_ball()`:

```python
if caught:
    gx, gy = space.gravity
    space.gravity = (gx, gy + 20)  # la gravità aumenta ogni volta
```

</details>

### 3. Palle di dimensione variabile
Fai in modo che ogni palla abbia un raggio casuale tra 10 e 25. Ricorda di aggiornare sia la surface che la shape!

<details>
<summary>Suggerimento</summary>

Usa `random.randint(10, 25)` per generare il raggio e usalo al posto di `BALL_RADIUS` nella funzione `create_ball()`.

</details>

<details>
<summary>Soluzione</summary>

Modifica `create_ball()`:

```python
def create_ball():
    radius = random.randint(10, 25)  # raggio variabile
    size = radius * 2
    center = (size//2, size//2)
    ball_surface = pygame.Surface((size,size), pygame.SRCALPHA)
    color = random.choice(COLORS)
    pygame.draw.circle(ball_surface, color, center, radius)

    mass = 1
    moment = pymunk.moment_for_circle(mass, 0, radius)
    ball_body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
    ball_body.position = (BASKET_CENTER[0], BALL_START_Y)

    ball_shape = pymunk.Circle(ball_body, radius)
    ball_shape.elasticity = 0.7
    ball_shape.friction = 0.5
    ball_shape.collision_type = COLLISION_TYPE_BALL
    ball_shape.filter = pymunk.ShapeFilter(categories=COLLISION_TYPE_BALL,
                                           mask=COLLISION_TYPE_BALL | COLLISION_TYPE_BASKET)

    space.add(ball_body, ball_shape)

    return {"body": ball_body, "shape": ball_shape, "surface": ball_surface, "color": color}
```

</details>

### 4. Effetto sonoro
Aggiungi un suono diverso quando la palla entra nel canestro e quando rimbalza via.

<details>
<summary>Suggerimento</summary>

Usa `pygame.mixer.Sound("file.wav")` per caricare un file audio `.wav` e `sound.play()` per riprodurlo. Puoi scaricare file .wav gratuiti da siti come [freesound.org](https://freesound.org/).

</details>

<details>
<summary>Soluzione</summary>

Dopo `pygame.init()`:

```python
pygame.mixer.init()
catch_sound = pygame.mixer.Sound("catch.wav")
miss_sound = pygame.mixer.Sound("miss.wav")
```

Nel callback `on_ball_enter_basket()`:

```python
if ball["color"] == basket_top_color:
    caught = True
    catch_sound.play()    # 🆕
    ball["shape"].filter = pymunk.ShapeFilter(categories=COLLISION_TYPE_BALL,
                                              mask=COLLISION_TYPE_BALL)
    ball["body"].velocity = (0, 80)
else:
    missed = True
    miss_sound.play()     # 🆕
    direction = random.choice([-1, 1])
    ball["body"].apply_impulse_at_local_point((direction * 100, 0))
```

</details>

### 5. Gestione delle vite e Game Over
Il giocatore ha 3 vite. Ogni volta che la palla non entra nel canestro (colore sbagliato o palla uscita senza toccare il canestro), perde una vita. Quando le vite finiscono, appare la scritta "Game Over" al centro dello schermo e il gioco si blocca. Premendo la barra spaziatrice il gioco ricomincia da zero.

<details>
<summary>Suggerimento</summary>

- Crea una variabile `lives = 3` e una variabile `game_over = False`
- In `reset_ball()`, se la palla non è stata catturata (`caught` è `False`), decrementa `lives`
- Quando `lives <= 0`, imposta `game_over = True`
- Nel game loop, se `game_over` è `True`, disegna solo la scritta "Game Over" e intercetta `pygame.K_SPACE` per resettare tutto
- Mostra le vite rimanenti a schermo con `font.render()`

</details>

<details>
<summary>Soluzione</summary>

Aggiungi prima del game loop:

```python
font = pygame.font.SysFont("Arial", 30)
font_big = pygame.font.SysFont("Arial", 60)
lives = 3
game_over = False
```

Modifica `reset_ball()` per gestire le vite:

```python
def reset_ball(ball):
    """Rimuove la pallina corrente e ne crea una nuova."""
    global caught, missed, lives, game_over

    # Se presenta anche la parte del punteggio,
    # score va aumentato se not game_over ...

    if not caught:
        lives -= 1
        if lives <= 0:
            game_over = True

    caught = False
    missed = False

    # Rimuove la palla dallo spazio fisico.
    space.remove(ball["shape"], ball["body"])
    # Ritorna la nuova palla
    return create_ball()
```

Crea una funzione per resettare tutto il gioco:

```python
def reset_game():
    global lives, game_over, caught, missed, basket_top_color_index, target_rotation_angle, ball, score
    lives = 3
    score = 0
    game_over = False
    caught = False
    missed = False
    basket_top_color_index = 0
    target_rotation_angle = 0.0
    basket_body.angle = 0.0
    basket_body.angular_velocity = 0
    space.remove(ball["shape"], ball["body"])
    ball = create_ball()
```

Nel game loop, intercetta la barra spaziatrice negli eventi:

```python
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_SPACE:         # 🆕
                reset_game()                                      # 🆕
            elif not game_over:                                   # 🆕
                if event.key == pygame.K_LEFT:
                    # ... rotazione come prima
                elif event.key == pygame.K_RIGHT:
                    # ... rotazione come prima
```

Nel game loop, dopo la sezione di disegno, gestisci il Game Over:

```python
    if game_over:
        # Scritta Game Over centrata
        go_surface = font_big.render("Game Over", True, (255, 50, 50))
        go_rect = go_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(go_surface, go_rect)
        # Istruzione per ricominciare
        restart_surface = font.render("Premi SPAZIO per ricominciare", True, (200, 200, 200))
        restart_rect = restart_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(restart_surface, restart_rect)
    else:
        # Mostra le vite rimanenti
        lives_surface = font.render(f"Vite: {'♥ ' * lives}", True, (255, 100, 100))
        screen.blit(lives_surface, ( WIDTH//2 + WIDTH//4 , 10))
```

**Nota:** Quando `game_over` è `True`, la logica di gioco (rotazione, collisioni, reset) viene saltata perché i tasti sono bloccati dal controllo `elif not game_over`. La simulazione fisica continua a girare ma non ha effetti visibili perché la palla è ferma fuori schermo dopo il reset.

</details>