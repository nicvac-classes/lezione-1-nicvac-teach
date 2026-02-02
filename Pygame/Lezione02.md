# Lezione 02 - Introduzione a Pymunk

## Cos'è Pymunk?

**Pymunk** è una libreria Python per la simulazione fisica 2D. È costruita sopra Chipmunk, un motore fisico usato in molti videogiochi.

## Perché integrarlo con Pygame?

Pygame sa disegnare e gestire input, ma non sa nulla di fisica: se vuoi che una pallina cada, rimbalzi o collida con altri oggetti, devi calcolare tutto a mano (gravità, velocità, angoli di rimbalzo...).

Pymunk risolve questo problema: tu descrivi gli oggetti (forma, massa, elasticità) e lui calcola come si muovono. Pygame si occupa solo di disegnarli.

**In sintesi:**
- **Pygame** → disegno e input
- **Pymunk** → fisica e movimento

---

## Blocco 1 - Lo scheletro dell'applicazione

### Obiettivo

Ricreare lo scheletro base di un'applicazione Pygame, come abbiamo imparato nella Lezione 01. Questa struttura sarà il punto di partenza su cui innesteremo la fisica.

### Ingredienti (già visti nella Lezione 01)

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
| `clock.tick(60)` | Limita a 60 FPS |
| `pygame.quit()` | Chiude Pygame |
| `sys.exit()` | Termina il programma |

### Esercizio

Ricrea lo scheletro di un'applicazione Pygame con:
- Finestra 800x600
- Titolo "Test Pymunk - Fisica"
- Sfondo color antracite (30, 30, 50)
- Game loop con gestione chiusura e frame rate a 60 FPS

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test Pymunk - Fisica")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 50))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```

</details>

---

## Blocco 2 - Lo spazio fisico e la gravità

### Obiettivo

Creare lo **spazio fisico** di Pymunk: il "mondo" in cui vivranno tutti gli oggetti della simulazione. Imposteremo anche la gravità.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `import pymunk` | Importa la libreria per la fisica 2D |
| `pymunk.Space()` | Crea uno spazio fisico vuoto. È il contenitore di tutti gli oggetti. |
| `space.gravity = (x, y)` | Imposta la gravità. In Pygame l'asse Y cresce verso il basso, quindi un valore positivo di Y fa cadere gli oggetti. |

### Come combinarli

1. Aggiungi `import pymunk` tra gli import
2. Dopo aver creato il clock, crea lo spazio fisico con `pymunk.Space()`
3. Imposta la gravità a `(0, 900)` — nessuna forza orizzontale, 900 pixel/secondo² verso il basso

### Esercizio

Partendo dal codice del Blocco 1, aggiungi lo spazio fisico con la gravità.

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
import pygame
import pymunk                                        # 🆕
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test Pymunk - Fisica")
clock = pygame.time.Clock()

# Spazio fisico
space = pymunk.Space()                               # 🆕
space.gravity = (0, 900)                             # 🆕

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 50))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```

</details>

---

## Blocco 3 - Il renderer per disegnare gli oggetti Pymunk

### Obiettivo

Collegare Pymunk a Pygame in modo che tutti gli oggetti fisici vengano disegnati automaticamente sullo schermo.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `import pymunk.pygame_util` | Importa le utility per disegnare oggetti Pymunk con Pygame |
| `pymunk.pygame_util.DrawOptions(screen)` | Crea un renderer che sa disegnare tutti gli oggetti dello spazio sulla superficie `screen` |
| `space.debug_draw(draw_options)` | Disegna tutti gli oggetti dello spazio usando il renderer |

### Come combinarli

1. Aggiungi `import pymunk.pygame_util` tra gli import
2. Dopo aver creato lo spazio fisico, crea il renderer con `pymunk.pygame_util.DrawOptions(screen)` e salvalo in una variabile `draw_options`
3. Nel game loop, dopo `screen.fill()`, chiama `space.debug_draw(draw_options)` per disegnare tutti gli oggetti

### Esercizio

Partendo dal codice del Blocco 2, aggiungi il renderer.

Esegui il programma. Cosa vedi? Ancora niente di nuovo, perché lo spazio fisico è vuoto! Ma ora siamo pronti: ogni oggetto che aggiungeremo apparirà automaticamente sullo schermo.

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
import pygame
import pymunk
import pymunk.pygame_util                            # 🆕
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test Pymunk - Fisica")
clock = pygame.time.Clock()

# Spazio fisico
space = pymunk.Space()
space.gravity = (0, 900)

# Renderer
draw_options = pymunk.pygame_util.DrawOptions(screen) # 🆕

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 50))
    space.debug_draw(draw_options)                    # 🆕
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```

</details>

---

## Blocco 4 - Il pavimento statico

### Obiettivo

Creare un **pavimento** su cui le palline potranno rimbalzare. Il pavimento è un oggetto **statico**: non si muove, non cade, ma interagisce con gli altri oggetti.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `space.static_body` | Un corpo statico predefinito, già presente nello spazio. Non si muove mai. |
| `pymunk.Segment(body, punto_a, punto_b, spessore)` | Crea un segmento (linea) tra due punti, con uno spessore. |
| `shape.elasticity` | Quanto l'oggetto è "elastico" (0 = nessun rimbalzo, 1 = rimbalzo perfetto). |
| `shape.friction` | Quanto attrito ha la superficie (0 = ghiaccio, 1 = molto attrito). |
| `space.add(shape)` | Aggiunge un oggetto allo spazio fisico. |

### Come combinarli

1. Crea il pavimento con `pymunk.Segment()`:
   - Primo parametro: il corpo a cui appartiene (`space.static_body`)
   - Secondo e terzo parametro: i due estremi del segmento `(0, 580)` e `(800, 580)`
   - Quarto parametro: lo spessore `5`
2. `pymunk.Segment()` restituisce una **shape** (forma). Salva il risultato in una variabile `floor`
3. Imposta le proprietà fisiche della shape:
   - `floor.elasticity = 0.8` (rimbalzo all'80%)
   - `floor.friction = 0.5` (attrito medio)
4. Aggiungi la shape allo spazio con `space.add(floor)`

### Esercizio

Partendo dal codice del Blocco 3, aggiungi il pavimento statico.

Esegui il programma. Ora dovresti vedere una linea grigia in basso: è il pavimento! Il renderer lo disegna automaticamente.

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
import pygame
import pymunk
import pymunk.pygame_util
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test Pymunk - Fisica")
clock = pygame.time.Clock()

# Spazio fisico
space = pymunk.Space()
space.gravity = (0, 900)

# Pavimento
floor = pymunk.Segment(space.static_body, (0, 580), (800, 580), 5)  # 🆕
floor.elasticity = 0.8                                              # 🆕
floor.friction = 0.5                                                # 🆕
space.add(floor)                                                    # 🆕

# Renderer
draw_options = pymunk.pygame_util.DrawOptions(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 50))
    space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```

</details>

---

## Blocco 5 - Creare il body (corpo rigido) di una pallina

### Obiettivo

Creare il **body** di una pallina. In Pymunk, ogni oggetto dinamico è composto da due parti:
- **Body**: il "corpo" invisibile che ha massa, posizione e velocità
- **Shape**: la "forma" visibile che definisce i contorni e le proprietà di collisione

In questo blocco ci occupiamo del body. Nel prossimo aggiungeremo la shape.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `pymunk.Body(massa, momento)` | Crea un corpo rigido con una certa massa e momento d'inerzia |
| `pymunk.moment_for_circle(massa, raggio_interno, raggio_esterno)` | Calcola il momento d'inerzia per un cerchio. Per un cerchio pieno, il raggio interno è 0. |
| `body.position = (x, y)` | Imposta la posizione iniziale del corpo |

### Come combinarli

1. Definisci la massa della pallina (es. `mass = 1`)
2. Definisci il raggio (es. `radius = 20`)
3. Calcola il momento d'inerzia con `pymunk.moment_for_circle(mass, 0, radius)`
4. Crea il body con `pymunk.Body(mass, momento)` e salvalo in una variabile `body`
5. Imposta la posizione iniziale, ad esempio `body.position = (400, 100)` (centro-alto della finestra)

### Esercizio

Partendo dal codice del Blocco 4, crea il body di una pallina con massa 1, raggio 20, posizionata a (400, 100).

Esegui il programma. Ancora nessuna novità visibile: il body esiste ma non ha ancora una forma da disegnare!

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
import pygame
import pymunk
import pymunk.pygame_util
import sys

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

# Pallina - body
mass = 1                                              # 🆕
radius = 20                                           # 🆕
moment = pymunk.moment_for_circle(mass, 0, radius)    # 🆕
body = pymunk.Body(mass, moment)                      # 🆕
body.position = (400, 100)                            # 🆕

# Renderer
draw_options = pymunk.pygame_util.DrawOptions(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 50))
    space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```

</details>

---

## Blocco 6 - Creare la shape e associarla al body

### Obiettivo

Creare la **shape** (forma) della pallina e collegarla al body. Solo quando body e shape sono collegati e aggiunti allo spazio, l'oggetto diventa visibile e interagisce con il mondo fisico.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `pymunk.Circle(body, raggio)` | Crea una forma circolare collegata a un body |
| `shape.elasticity` | Quanto la pallina rimbalza (0 = niente, 1 = rimbalzo perfetto) |
| `shape.friction` | Quanto attrito ha la superficie della pallina |
| `space.add(body, shape)` | Aggiunge body e shape allo spazio. Si possono aggiungere insieme! |

### Come combinarli

1. Crea la shape con `pymunk.Circle(body, radius)` e salvala in una variabile `shape`
2. Imposta le proprietà fisiche:
   - `shape.elasticity = 0.9` (rimbalzo al 90%)
   - `shape.friction = 0.5` (attrito medio)
3. Aggiungi body e shape allo spazio con `space.add(body, shape)`

### Esercizio

Partendo dal codice del Blocco 5, crea la shape circolare, imposta elasticità e attrito, e aggiungi tutto allo spazio.

Esegui il programma. Finalmente! Dovresti vedere un cerchio colorato in alto... ma non si muove! Perché? Lo scopriamo nel prossimo blocco.

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
import pygame
import pymunk
import pymunk.pygame_util
import sys

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

# Pallina - body
mass = 1
radius = 20
moment = pymunk.moment_for_circle(mass, 0, radius)
body = pymunk.Body(mass, moment)
body.position = (400, 100)

# Pallina - shape
shape = pymunk.Circle(body, radius)                   # 🆕
shape.elasticity = 0.9                                # 🆕
shape.friction = 0.5                                  # 🆕
space.add(body, shape)                                # 🆕

# Renderer
draw_options = pymunk.pygame_util.DrawOptions(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 50))
    space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```

</details>

---

## Blocco 7 - Far avanzare la simulazione (step)

### Obiettivo

Far "avanzare il tempo" nella simulazione fisica. Senza questo passaggio, Pymunk non calcola nulla: gli oggetti restano fermi perché il mondo fisico è congelato!

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `space.step(dt)` | Fa avanzare la simulazione di `dt` secondi. Calcola gravità, collisioni, rimbalzi, ecc. |

### Come combinarli

1. Nel game loop, chiama `space.step(1/60)` per far avanzare la simulazione di 1/60 di secondo (coerente con i 60 FPS)
2. Posizionalo **prima** di disegnare, così disegniamo la situazione aggiornata

### Esercizio

Partendo dal codice del Blocco 6, aggiungi `space.step(1/60)` nel game loop.

Esegui il programma. La pallina cade e rimbalza sul pavimento! La fisica è in azione.

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
import pygame
import pymunk
import pymunk.pygame_util
import sys

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

# Pallina - body
mass = 1
radius = 20
moment = pymunk.moment_for_circle(mass, 0, radius)
body = pymunk.Body(mass, moment)
body.position = (400, 100)

# Pallina - shape
shape = pymunk.Circle(body, radius)
shape.elasticity = 0.9
shape.friction = 0.5
space.add(body, shape)

# Renderer
draw_options = pymunk.pygame_util.DrawOptions(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 50))
    space.debug_draw(draw_options)
    space.step(1/60)                                  # 🆕
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```

</details>

---

## Blocco 8 - Creare palline al click del mouse

### Obiettivo

Rendere il programma interattivo: ogni volta che clicchiamo con il mouse, creiamo una nuova pallina nella posizione del click.

### Ingredienti

| Elemento | Descrizione |
|----------|-------------|
| `pygame.MOUSEBUTTONDOWN` | Evento che scatta quando si preme un tasto del mouse |
| `event.pos` | La posizione (x, y) del mouse al momento dell'evento |
| Funzione `create_ball(pos)` | Una funzione che crea una pallina in una posizione data |

### Come combinarli

1. Crea una funzione `create_ball(pos)` che:
   - Crea un body con massa 1 e raggio 20
   - Imposta `body.position = pos`
   - Crea una shape circolare con elasticità 0.9 e attrito 0.5
   - Aggiunge body e shape allo spazio
   - Restituisce la shape (utile per tenerla in una lista)
2. Crea una lista vuota `balls = []` per tenere traccia delle palline
3. Nel ciclo degli eventi, intercetta `pygame.MOUSEBUTTONDOWN`
4. Quando scatta, chiama `create_ball(event.pos)` e aggiungi il risultato alla lista
5. Rimuovi la pallina singola creata nei blocchi precedenti (ora le creiamo al click)

### Esercizio

Partendo dal codice del Blocco 7, crea la funzione `create_ball()` e gestisci il click del mouse per creare nuove palline.

Esegui il programma. Clicca in punti diversi della finestra: le palline cadono, rimbalzano e interagiscono tra loro!

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
import pygame
import pymunk
import pymunk.pygame_util
import sys

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

# Funzione per creare una pallina                     # 🆕
def create_ball(pos):                                 # 🆕
    mass = 1                                          # 🆕
    radius = 20                                       # 🆕
    body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))  # 🆕
    body.position = pos                               # 🆕
    shape = pymunk.Circle(body, radius)               # 🆕
    shape.elasticity = 0.9                            # 🆕
    shape.friction = 0.5                              # 🆕
    space.add(body, shape)                            # 🆕
    return shape                                      # 🆕

balls = []                                            # 🆕

# Renderer
draw_options = pymunk.pygame_util.DrawOptions(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:      # 🆕
            balls.append(create_ball(event.pos))      # 🆕

    screen.fill((30, 30, 50))
    space.debug_draw(draw_options)
    space.step(1/60)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```

</details>

---

## Codice completo finale

Ecco il programma completo che abbiamo costruito passo dopo passo:

```python
import pygame
import pymunk
import pymunk.pygame_util
import sys

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

# Funzione per creare una pallina
def create_ball(pos):
    mass = 1
    radius = 20
    body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.9
    shape.friction = 0.5
    space.add(body, shape)
    return shape

balls = []

# Renderer
draw_options = pymunk.pygame_util.DrawOptions(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            balls.append(create_ball(event.pos))

    screen.fill((30, 30, 50))
    space.debug_draw(draw_options)
    space.step(1/60)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```

---

## Esercizi extra

Prova a modificare il programma per aggiungere queste funzionalità:

### 1. Pavimento inclinato
Aggiungi un secondo segmento inclinato che faccia rotolare le palline. Ad esempio, da `(0, 400)` a `(300, 500)`.

<details>
<summary>Suggerimento</summary>

Usa `pymunk.Segment()` come per il pavimento, ma con coordinate diverse per creare una rampa.

</details>

<details>
<summary>Soluzione</summary>

```python
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
```

</details>

### 2. Pareti laterali
Aggiungi due pareti verticali ai lati della finestra per impedire alle palline di uscire.

<details>
<summary>Suggerimento</summary>

Crea due segmenti verticali: uno da `(0, 0)` a `(0, 600)` e uno da `(800, 0)` a `(800, 600)`.

</details>

<details>
<summary>Soluzione</summary>

```python
# Pavimento
floor = pymunk.Segment(space.static_body, (0, 580), (800, 580), 5)
floor.elasticity = 0.8
floor.friction = 0.5
space.add(floor)

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
```

</details>

### 3. Palline di dimensioni casuali
Fai in modo che ogni pallina abbia un raggio casuale tra 10 e 40 pixel.

<details>
<summary>Suggerimento</summary>

Usa `import random` e `random.randint(10, 40)` per generare il raggio.

</details>

<details>
<summary>Soluzione</summary>

```python
import pygame
import pymunk
import pymunk.pygame_util
import random                                         # 🆕
import sys

# ... resto del codice ...

def create_ball(pos):
    mass = 1
    radius = random.randint(10, 40)                   # 🆕
    body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.9
    shape.friction = 0.5
    space.add(body, shape)
    return shape
```

</details>

### 4. Cambia la gravità con i tasti
Usa i tasti freccia per cambiare la direzione della gravità: SU inverte la gravità, GIÙ la ripristina, SINISTRA e DESTRA la inclinano.

<details>
<summary>Suggerimento</summary>

Intercetta `pygame.KEYDOWN` e modifica `space.gravity` in base al tasto premuto. Ricorda che puoi usare `pygame.key.get_pressed()` come nella Lezione 01.

</details>

<details>
<summary>Soluzione</summary>

```python
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            balls.append(create_ball(event.pos))
        if event.type == pygame.KEYDOWN:              # 🆕
            if event.key == pygame.K_UP:              # 🆕
                space.gravity = (0, -900)             # 🆕
            if event.key == pygame.K_DOWN:            # 🆕
                space.gravity = (0, 900)              # 🆕
            if event.key == pygame.K_LEFT:            # 🆕
                space.gravity = (-900, 0)             # 🆕
            if event.key == pygame.K_RIGHT:           # 🆕
                space.gravity = (900, 0)              # 🆕
```

</details>

### 5. Cancella tutte le palline
Premi SPAZIO per rimuovere tutte le palline dallo schermo.

<details>
<summary>Suggerimento</summary>

Per ogni shape nella lista `balls`, devi rimuovere sia la shape che il suo body con `space.remove(shape.body, shape)`. Poi svuota la lista con `balls.clear()`.

</details>

<details>
<summary>Soluzione</summary>

```python
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            balls.append(create_ball(event.pos))
        if event.type == pygame.KEYDOWN:              # 🆕
            if event.key == pygame.K_SPACE:           # 🆕
                for shape in balls:                   # 🆕
                    space.remove(shape.body, shape)   # 🆕
                balls.clear()                         # 🆕
```

</details>