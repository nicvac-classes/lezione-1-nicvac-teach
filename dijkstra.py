# https://training.olinfo.it/task/dijkstra
# Versione con patch nodi 1 based.

import sys
import heapq #Coda con priorità  

# Per la sottoposizione di questo problema in piattaforma: ATTIVARE QUESTE DUE RIGHE!
sys.stdin = open('input.txt')
sys.stdout = open('output.txt', 'w')

#sys.stdin = open('dijkstra_input01.txt')
#sys.stdout = open('output.txt', 'w')

# Lettura input
N, M = map(int, input().split())
nodo_start, nodo_stop = map(int, input().split())
#Patch per problema 1-based
nodo_start -= 1
nodo_stop  -= 1

adj = {}
for nodo in range(N):
    adj[nodo] = []

for _ in range(M):
    i, j, p = map(int, input().split())
    #Patch per problema 1-based
    #adj[i].append((p,j))
    adj[i-1].append((p,j-1))

# IMPLEMENTARE QUI
risposta = 0

#Calcola le distanze minime per ogni nodo a partire da nodo_start
def dijkstra(adj, N, nodo_start):
    
    # Coda con priorità
    # Inizializzo la coda con il nodo di partenza a costo 0
    pq = [(0, nodo_start)]

    #Inizializzo i visitati
    visitati = [ False ] * N
    percorso = []

    #Distanze. Inizializzo a infinito per ogni nodo e a 0 per nodo_start
    dist = [ float('inf') ] * N
    dist[nodo_start] = 0

    #Finchè la coda è piena
    while len(pq) > 0:
        #Estraggo il nodo a distanza minima.
        # La prima volta corrisponde con nodo_start
        (p, i) = heapq.heappop(pq)

        if visitati[i]:
            continue

        visitati[i] = True
        percorso.append( (p,i) )

        # Per ogni nodo adiacente ad i
        for (dist_j, j) in adj[i]:
            dist_curr = dist[i] # Distanza percorsa fino al nodo i, quello corrente
            dist_new = dist_curr + dist_j
            if dist_new < dist[j]:
                dist[j] = dist_new
                heapq.heappush( pq, (dist[j], j) )

    return dist, percorso

#Calcolo il percorso minimo e distanze da nodo_start
distanze, percorso = dijkstra(adj, N, nodo_start)

risposta = distanze[nodo_stop]

print(risposta)

#print(percorso)
