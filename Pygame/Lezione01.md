| Attenzione |
| --- |
| Per leggere correttamente questo documento, click destro su questo file e selezionare Open Preview. |

# Introduzione a Pygame: Muovere un cerchio con la tastiera

Impariamo le basi di Pygame costruendo passo dopo passo un programma che mostra un cerchio e permette di muoverlo con le frecce direzionali.

## Il risultato finale

Al termine della lezione avremo un programma che:
- Apre una finestra grafica 640x480
- Disegna un cerchio rosso al centro
- Permette di muovere il cerchio con le frecce direzionali
- Si chiude correttamente quando premiamo la X della finestra

```
┌─────────────────────────────────┐
│ Test Pygame                 [X] │
├─────────────────────────────────┤
│                                 │
│                                 │
│              ●                  │
│           (cerchio              │
│            mobile)              │
│                                 │
│                                 │
└─────────────────────────────────┘
        ↑ ↓ ← → per muoversi
```

---

## Blocco 1 - Creare la finestra grafica

### Obiettivo

Creare una finestra grafica di dimensioni 640x480 pixel con titolo "Test Pygame".

### Ingredienti

| Funzione | Descrizione |
|----------|-------------|
| `import pygame` | Importa la libreria pygame |
| `pygame.init()` | Inizializza tutti i moduli di pygame. Va chiamata sempre all'inizio. |
| `pygame.display.set_mode((larghezza, altezza))` | Crea una finestra delle dimensioni specificate. Restituisce una *surface* su cui disegneremo. |
| `pygame.display.set_caption("titolo")` | Imposta il titolo della finestra. |

### Come combinarli

1. Importare pygame
2. Inizializzare pygame con `init()`
3. Creare la finestra con `set_mode()` e salvare la surface restituita in una variabile `screen`
4. Impostare il titolo con `set_caption()`

### Esercizio

Scrivi un programma che crea una finestra 640x480 con titolo "Test Pygame".

**Attenzione:** Se esegui il programma, vedrai la finestra aprirsi e chiudersi immediatamente. È normale! Il programma termina subito dopo aver creato la finestra. Nel prossimo blocco risolveremo questo problema.

---

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Test Pygame")
```

</details>

---

## Blocco 2 - Il game loop e la gestione degli eventi

### Obiettivo

Mantenere la finestra aperta finché l'utente non preme la X per chiuderla.

### Ingredienti

| Funzione | Descrizione |
|----------|-------------|
| `while running:` | Ciclo principale del gioco (game loop). Ripete le istruzioni finché `running` è `True`. |
| `pygame.event.get()` | Restituisce la lista di tutti gli eventi accaduti (click, tastiera, chiusura finestra, ecc.). Va chiamata ad ogni ciclo. |
| `event.type` | Il tipo di evento. Ogni evento ha un tipo che lo identifica. |
| `pygame.QUIT` | Costante che rappresenta l'evento "chiusura finestra" (click sulla X). |

### Come combinarli

1. Creare una variabile `running = True` che controlla il ciclo
2. Creare un ciclo `while running:`
3. Dentro il ciclo, scorrere tutti gli eventi con `for event in pygame.event.get():`
4. Se l'evento è di tipo `pygame.QUIT`, impostare `running = False` per uscire dal ciclo

### Esercizio

Partendo dal codice del Blocco 1, aggiungi un game loop che mantiene la finestra aperta. La finestra deve chiudersi solo quando l'utente preme la X.

Esegui il programma: la finestra dovrebbe rimanere aperta finché non la chiudi.

---

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Test Pygame")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
```

</details>

---

## Blocco 3 - Disegnare sullo schermo

### Obiettivo

Disegnare un cerchio rosso al centro della finestra su uno sfondo scuro.

### Ingredienti

| Funzione | Descrizione |
|----------|-------------|
| `screen.fill((R, G, B))` | Riempie l'intera finestra con un colore. I valori R, G, B vanno da 0 a 255. |
| `pygame.draw.circle(surface, colore, (x, y), raggio)` | Disegna un cerchio sulla surface indicata, con il centro in (x, y) e il raggio specificato. |
| `pygame.display.flip()` | Aggiorna lo schermo mostrando tutto ciò che è stato disegnato. Senza questa chiamata non vedremo nulla. |

### Come combinarli

1. Dentro il game loop, riempire lo sfondo con `screen.fill()` usando un colore scuro, ad esempio `(30, 30, 50)`
2. Disegnare il cerchio con `pygame.draw.circle()` al centro della finestra (320, 240) con un colore rosso `(255, 100, 100)` e raggio 30
3. Chiamare `pygame.display.flip()` per mostrare il risultato

**Nota:** L'ordine è importante! Prima si riempie lo sfondo, poi si disegna sopra, infine si aggiorna lo schermo.

### Esercizio

Partendo dal codice del Blocco 2, aggiungi le istruzioni per disegnare un cerchio rosso al centro della finestra su sfondo scuro.

Esegui il programma: dovresti vedere una finestra con sfondo scuro e un cerchio rosso al centro.

---

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Test Pygame")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((30, 30, 50))
    pygame.draw.circle(screen, (255, 100, 100), (320, 240), 30)
    pygame.display.flip()
```

</details>

---

## Blocco 4 - Leggere la tastiera e muovere il cerchio

### Obiettivo

Fare in modo che il cerchio si muova quando premiamo le frecce direzionali.

### Ingredienti

| Funzione | Descrizione |
|----------|-------------|
| `pygame.key.get_pressed()` | Restituisce lo stato di tutti i tasti. È un dizionario che indica quali tasti sono premuti in questo momento. |
| `keys[pygame.K_LEFT]` | Vale `True` se la freccia sinistra è premuta. |
| `keys[pygame.K_RIGHT]` | Vale `True` se la freccia destra è premuta. |
| `keys[pygame.K_UP]` | Vale `True` se la freccia su è premuta. |
| `keys[pygame.K_DOWN]` | Vale `True` se la freccia giù è premuta. |

### Come combinarli

1. Prima del game loop, creare due variabili `x` e `y` per la posizione del cerchio (inizialmente al centro: 320, 240)
2. Creare una variabile `speed` per la velocità di movimento (ad esempio 5)
3. Dentro il game loop, leggere lo stato dei tasti con `keys = pygame.key.get_pressed()`
4. Modificare `x` e `y` in base ai tasti premuti:
   - Freccia sinistra: `x -= speed`
   - Freccia destra: `x += speed`
   - Freccia su: `y -= speed`
   - Freccia giù: `y += speed`
5. Usare le variabili `x` e `y` nel disegno del cerchio al posto dei valori fissi

### Esercizio

Partendo dal codice del Blocco 3, aggiungi le variabili per la posizione e la velocità, leggi la tastiera e fai muovere il cerchio con le frecce direzionali.

Esegui il programma: dovresti poter muovere il cerchio con le frecce direzionali.

**Attenzione:** Il cerchio si muove, ma la velocità dipende da quanto è veloce il computer! Su un PC potente il cerchio potrebbe volare via, su uno lento potrebbe essere più gestibile. Nel prossimo blocco risolveremo questo problema.

---

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Test Pygame")

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
```

</details>

---

## Blocco 5 - Controllo della velocità (frame rate)

### Obiettivo

Limitare la velocità del gioco a 60 fotogrammi al secondo, così il movimento sarà uniforme su qualsiasi computer.

### Ingredienti

| Funzione | Descrizione |
|----------|-------------|
| `pygame.time.Clock()` | Crea un orologio per controllare il tempo. Va chiamata una sola volta, prima del game loop. |
| `clock.tick(fps)` | Limita il ciclo a un massimo di `fps` fotogrammi al secondo. Va chiamata ad ogni ciclo, tipicamente alla fine. |

### Come combinarli

1. Prima del game loop, creare un orologio con `clock = pygame.time.Clock()`
2. Alla fine del game loop, chiamare `clock.tick(60)` per limitare a 60 FPS

**Nota:** 60 FPS significa che il game loop viene eseguito al massimo 60 volte al secondo. Se il computer è più veloce, `tick()` aggiunge una piccola pausa per mantenere la velocità costante.

### Esercizio

Partendo dal codice del Blocco 4, aggiungi il controllo del frame rate a 60 FPS.

Esegui il programma: ora il cerchio dovrebbe muoversi in modo fluido e costante, indipendentemente dalla potenza del computer.

---

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
import pygame

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
```

</details>

---

## Blocco 6 - Chiusura pulita

### Obiettivo

Terminare correttamente il programma, rilasciando le risorse utilizzate da Pygame.

### Ingredienti

| Funzione | Descrizione |
|----------|-------------|
| `import sys` | Importa il modulo sys, necessario per terminare il programma. |
| `pygame.quit()` | Chiude tutti i moduli di Pygame e rilascia le risorse. Va chiamata quando il gioco termina. |
| `sys.exit()` | Termina il programma Python. Assicura che il processo si chiuda correttamente. |

### Come combinarli

1. All'inizio del programma, aggiungere `import sys`
2. Dopo il game loop (quando `running` diventa `False`), chiamare `pygame.quit()`
3. Subito dopo, chiamare `sys.exit()`

**Nota:** Senza queste istruzioni il programma potrebbe non chiudersi correttamente, lasciando processi attivi in background.

### Esercizio

Partendo dal codice del Blocco 5, aggiungi l'import di sys e le istruzioni di chiusura dopo il game loop.

Esegui il programma: il comportamento visibile sarà lo stesso, ma ora il programma si chiude in modo pulito.

---

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
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
```

</details>

---

## Codice completo

Ecco il programma finale con tutto il codice assemblato:

```python
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
```

---

## Esercizi extra

### Esercizio A - Limita il movimento

Impedisci al cerchio di uscire dai bordi della finestra. Il cerchio ha raggio 30, quindi il centro non deve andare oltre 30 pixel dal bordo.

**Suggerimento:** Dopo aver modificato `x` e `y`, controlla che i valori rimangano nell'intervallo consentito. Usa `max()` e `min()` oppure degli `if`.

---

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    x -= speed
if keys[pygame.K_RIGHT]:
    x += speed
if keys[pygame.K_UP]:
    y -= speed
if keys[pygame.K_DOWN]:
    y += speed

# Limita il movimento ai bordi della finestra
raggio = 30
if x < raggio:
    x = raggio
if x > 640 - raggio:
    x = 640 - raggio
if y < raggio:
    y = raggio
if y > 480 - raggio:
    y = 480 - raggio
```

</details>

---

### Esercizio B - Cambia colore

Premi la barra spaziatrice per cambiare il colore del cerchio. Ad ogni pressione il colore deve cambiare tra rosso, verde e blu.

**Suggerimento:** Crea una lista di colori e una variabile per l'indice corrente. Usa l'evento `pygame.KEYDOWN` con `event.key == pygame.K_SPACE` per rilevare la pressione del tasto.

---

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
# Prima del game loop
colori = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
indice_colore = 0

# Nel game loop, dentro il ciclo degli eventi
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            indice_colore = (indice_colore + 1) % len(colori)

# Nel disegno del cerchio
pygame.draw.circle(screen, colori[indice_colore], (x, y), 30)
```

</details>

---

### Esercizio C - Velocità variabile

Usa i tasti `+` e `-` per aumentare o diminuire la velocità del cerchio. La velocità minima deve essere 1, la massima 15.

**Suggerimento:** Usa gli eventi `pygame.KEYDOWN` con `event.key == pygame.K_PLUS` (oppure `pygame.K_KP_PLUS` per il tastierino numerico) e `pygame.K_MINUS`.

---

<details>
<summary>Solo dopo aver svolto l'esercizio, apri qui per vedere la soluzione</summary>

```python
# Nel game loop, dentro il ciclo degli eventi
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
            speed = speed + 1
            if speed > 15:
                speed = 15
        if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
            speed = speed - 1
            if speed < 1:
                speed = 1
```

</details>

---