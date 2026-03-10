# La Tecnica Greedy (Ingordo)

## Cos'è un algoritmo greedy?

Un algoritmo **greedy** (dall'inglese *greedy* = ingordo, avido) è una strategia algoritmica che, ad ogni passo, compie la **scelta localmente migliore**, senza mai tornare indietro sulle decisioni prese.

L'idea è semplice: se ad ogni passo faccio la scelta che *sembra* la più conveniente in quel momento, alla fine otterrò la soluzione ottima globale.

> **Attenzione:** questo non funziona sempre! Un greedy è corretto solo se il problema ha una struttura particolare (la cosiddetta *proprietà greedy*). Vedremo come riconoscerla.

---

## Un primo esempio: il problema del resto

### Il problema

Devi dare un resto di **36 centesimi** usando il minor numero possibile di monete.
Le monete disponibili sono: **20, 10, 5, 2, 1** centesimi.

### Ragionamento greedy

Ad ogni passo, scelgo la **moneta più grande** che non supera il resto ancora da dare:

| Passo | Resto rimasto | Moneta scelta |
|:-----:|:-------------:|:-------------:|
| 1     | 36            | 20            |
| 2     | 16            | 10            |
| 3     | 6             | 5             |
| 4     | 1             | 1             |

**Risultato:** 4 monete (20 + 10 + 5 + 1).

È la soluzione ottima? Sì! Con il sistema monetario dell'euro questa strategia funziona sempre.

### Quando NON funziona

Immagina un sistema monetario con monete da **25, 20, 1** centesimi. Devi dare un resto di **40 centesimi**.

- **Greedy:** 25 + 1 + 1 + ... + 1 = 25 + 15×1 → **16 monete**
- **Soluzione ottima:** 20 + 20 → **2 monete**

Il greedy ha fallito! Questo perché la struttura del problema (quel particolare insieme di monete) non garantisce la proprietà greedy.

> **Lezione:** prima di usare un greedy, bisogna convincersi (o dimostrare) che la scelta locale porta effettivamente alla soluzione globale ottima.

---

## Schema generale di un algoritmo greedy

```
1. Ordina i candidati secondo un criterio di "bontà"
2. Per ogni candidato (dal migliore al peggiore):
     se il candidato è compatibile con la soluzione corrente:
         aggiungilo alla soluzione
3. Restituisci la soluzione
```

I tre ingredienti fondamentali sono:

1. **Criterio di ordinamento** — come decido chi è "il migliore"?
2. **Criterio di compatibilità** — quando posso aggiungere un candidato?
3. **Correttezza** — perché questa strategia dà la soluzione ottima?

---

## Il problema: Turni di guardia (OII – Selezioni Territoriali 2012)

### Testo del problema

Zio Paperone parte per un viaggio di **K** giorni (dal giorno `0` al giorno `K-1`).
Ha bisogno che il suo deposito sia **sempre sorvegliato**.

**N** persone hanno dato la loro disponibilità: ognuna è disponibile per un intervallo di giorni `[A, B]` (dal giorno `A` al giorno `B` compresi).

Paperone vuole coinvolgere il **minor numero di persone** possibile, coprendo tutti i K giorni senza lasciare buchi.

### Esempio

K = 8 (giorni da 0 a 7), disponibilità:

| Persona   | Intervallo |
|:---------:|:----------:|
| Paperino  | [3, 5]     |
| Paperoga  | [0, 2]     |
| Battista  | [1, 3]     |
| Gastone   | [5, 6]     |
| Archimede | [4, 7]     |

**Soluzione:** Paperoga [0,2] + Paperino [3,5] + Archimede [4,7] → **3 persone**.

---

### Che tipo di problema è?

Questo è un classico problema di **Interval Covering**: data una "linea" da coprire (i giorni da 0 a K-1) e un insieme di intervalli, trovare il **minor numero di intervalli** che coprono l'intera linea.

È uno dei problemi più classici risolvibili con la tecnica greedy.

---

### Strategia greedy

Ragioniamo passo per passo.

Siamo al giorno `0` e dobbiamo coprire fino al giorno `K-1`.

**Idea chiave:** ad ogni passo, tra tutte le persone che possono coprire il giorno corrente, scelgo quella che **arriva più lontano** (cioè con il giorno `B` massimo). In questo modo, con una sola scelta, copro il maggior numero possibile di giorni futuri.

#### Algoritmo

```
1. Ordina le persone per inizio turno crescente

2. giorno = 0      // primo giorno da coprire
   risposta = 0

3. Finché giorno <= K-1:
     a. Tra tutte le persone con inizio turno <= giorno,
        trova quella con fine turno massima (miglior_fine).
     b. Seleziona quella persona
     c. risposta += 1
     d. giorno = miglior_fine + 1  // il prossimo giorno da coprire

4. Restituisci risposta
```

---

### Esempio passo-passo

K = 8, intervalli ordinati per inizio crescente:

| Persona   | Inizio | Fine |
|:---------:|:------:|:----:|
| Paperoga  | 0      | 2    |
| Battista  | 1      | 3    |
| Paperino  | 3      | 5    |
| Archimede | 4      | 7    |
| Gastone   | 5      | 6    |

**Passo 1:** `giorno = 0`
- Chi ha inizio turno ≤ 0? → Paperoga [0,2]
- Scelgo Paperoga (fine=2 è il massimo tra i candidati)
- `giorno = 3`, `risposta = 1`

**Passo 2:** `giorno = 3`
- Chi ha inizio turno ≤ 3? → Battista [1,3], Paperino [3,5]
- Scelgo Paperino (fine=5 > fine=3 di Battista)
- `giorno = 6`, `risposta = 2`

**Passo 3:** `giorno = 6`
- Chi ha inizio turno ≤ 6? → Archimede [4,7], Gastone [5,6]
- Scelgo Archimede (fine=7 > fine=6 di Gastone)
- `giorno = 8`, `risposta = 3`

**Fine:** `giorno = 8 > K-1 = 7` → tutto coperto!

**Risultato: 3 persone.**

---

### Perché funziona?

L'intuizione è questa: se devo coprire il giorno `d`, e ho diverse persone disponibili, scegliere quella che arriva più lontano **non può mai essere peggio** di qualsiasi altra scelta. Qualunque altra persona coprirebbe un sottoinsieme dei giorni coperti dalla scelta greedy (o meno), quindi non mi può mai servire a "risparmiare" una persona in futuro.

Più formalmente, si può dimostrare per **scambio (exchange argument)**: se esiste una soluzione ottima che non usa la scelta greedy, posso sostituire la persona scelta in quella soluzione con la persona greedy, e la soluzione resta valida (perché la persona greedy copre almeno gli stessi giorni, e potenzialmente di più). Quindi la soluzione greedy non usa mai più persone di quella ottima.

---

### Implementazione in Python

```python
# https://training.olinfo.it/task/turni

K = int(input())
N = int(input())

persone = []
for _ in range(N):
    a, b = map(int, input().split())
    persone.append((a, b))

risposta = 0

# Ordino le persone in base al loro primo giorno disponibile
# Gli elementi di persone sono dei pair (inizio, fine). Mi interessa che siano ordinate su inizio, 
# quindi l'ordinamento su pair python mi va bene
persone.sort()

giorno = 0    # prossimo giorno da coprire
i = 0         # indice nella lista ordinata di persone

while giorno < K:
    
    miglior_fine = -1

    # Cerco la persona che ha inizio turno <= giorno coperto
    while i < N:
        persona = persone[i]
        if persona[0] <= giorno:
            # Fra le persone con inizio turno compatibile, 
            # seleziono quella con la fine turno più lontano possibile
            miglior_fine = max( miglior_fine, persona[1] )
        else:
            # interrompo la ricerca se non ci sono altre persone che 
            # coprono il giorno richiesto
            break 
        i += 1

    risposta += 1 # Ho trovato un'altra persona (la migliore disponibile)

    # Ho coperto fino a miglior_fine, nel prossimo loop cerco chi può coprire il prossimo giorno.
    giorno = miglior_fine + 1

print(risposta)
```

### Complessità

- **Ordinamento:** O(N log N)
- **Scansione:** O(N) — ogni persona viene esaminata al più una volta
- **Totale:** O(N log N)

---

### Verifica con il secondo esempio del problema

K = 10, intervalli:

| Inizio | Fine |
|:------:|:----:|
| 2      | 5    |
| 0      | 2    |
| 1      | 3    |
| 5      | 6    |
| 4      | 7    |
| 7      | 9    |

Ordinati per inizio crescente: [0,2], [1,3], [2,5], [4,7], [5,6], [7,9]

- `giorno=0` → candidati con inizio ≤ 0: [0,2] → miglior_fine = 2 → `giorno=3`, risposta=1
- `giorno=3` → candidati con inizio ≤ 3: [1,3] (fine=3), [2,5] (fine=5) → miglior_fine = 5 → `giorno=6`, risposta=2
- `giorno=6` → candidati con inizio ≤ 6: [4,7] (fine=7), [5,6] (fine=6) → miglior_fine = 7 → `giorno=8`, risposta=3
- `giorno=8` → candidati con inizio ≤ 8: [7,9] (fine=9) → miglior_fine = 9 → `giorno=10`, risposta=4

**Risultato: 4 persone** ✓

---

## Quando usare il greedy?

La tecnica greedy è applicabile quando il problema ha due proprietà:

1. **Scelta greedy (Greedy Choice Property):** esiste sempre una soluzione ottima che include la scelta localmente migliore. In altre parole, non è mai necessario "sacrificare" il presente per il futuro.

2. **Sottostruttura ottima (Optimal Substructure):** dopo aver fatto la scelta greedy, il sottoproblema rimanente ha la stessa struttura del problema originale.

### Problemi classici risolvibili con greedy

| Problema | Criterio greedy |
|:---------|:----------------|
| Interval Covering (questo!) | Scegli l'intervallo che arriva più lontano |
| Activity Selection | Scegli l'attività che finisce prima |
| Fractional Knapsack | Scegli l'oggetto con miglior rapporto valore/peso |
| Huffman Coding | Unisci i due nodi con frequenza minima |
| Kruskal / Prim (MST) | Scegli l'arco di peso minimo |

### Problemi NON risolvibili con greedy

| Problema | Perché il greedy fallisce |
|:---------|:--------------------------|
| 0/1 Knapsack | La scelta locale (miglior rapporto) può escludere combinazioni migliori |
| Problema del resto (con monete arbitrarie) | Come visto nell'esempio iniziale |
| Cammino minimo con pesi negativi | Il cammino localmente corto può essere globalmente lungo |

---

## Esercizi proposti

1. **Activity Selection:** hai N attività, ognuna con un orario di inizio e fine. Puoi fare al massimo un'attività alla volta. Quante attività puoi fare al massimo? *(Hint: ordina per tempo di fine crescente)*

2. **Variante Turni di guardia:** modifica il codice per stampare anche **quali persone** vengono selezionate, non solo il numero.

3. **Sfida:** cosa succede se le disponibilità non coprono tutti i giorni? Modifica l'algoritmo per restituire `-1` in quel caso e verificare la correttezza con un esempio.
