# https://training.olinfo.it/task/dijkstra
# Versione con nodi zero based.

import sys
import heapq #Coda con priorità  

# Per la sottoposizione di questo problema in piattaforma: ATTIVARE QUESTE DUE RIGHE!
#sys.stdin = open('input.txt')
#sys.stdout = open('output.txt', 'w')

sys.stdin = open('dijkstra_input01.txt')
sys.stdout = open('output.txt', 'w')

# Lettura input
N, M = map(int, input().split())
nodo_start, nodo_stop = map(int, input().split())

adj = {}
for nodo in range(N):
    adj[nodo] = []

for _ in range(M):
    i, j, p = map(int, input().split())
    adj[i].append((p,j))

# IMPLEMENTARE QUI
risposta = 0

#Calcola le distanze minime per ogni nodo a partire da nodo_start
def dijkstra(adj, N, nodo_start):
    
    # Coda con priorità: (costo, nodo)
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
        # Estrae la coppia (costo, nodo) col costo minimo
        # La prima volta corrisponde con nodo_start
        (p, i) = heapq.heappop(pq)

        if visitati[i]: # già elaborato? salta
            continue

        visitati[i] = True
        percorso.append( (p,i) )

        # Per ogni nodo adiacente ad i 
        for (dist_j, j) in adj[i]:
            dist_curr = dist[i] # Distanza percorsa fino al nodo i, quello corrente
            dist_new = dist_curr + dist_j
            if dist_new < dist[j]: # trovata distanza migliore?
                dist[j] = dist_new # aggiorna (rilassamento)
                heapq.heappush( pq, (dist[j], j) )

    return dist, percorso

#Calcolo il percorso minimo e distanze da nodo_start
distanze, percorso = dijkstra(adj, N, nodo_start)

risposta = distanze[nodo_stop]

print(risposta)

#print(percorso)
