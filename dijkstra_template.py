# https://training.olinfo.it/task/dijkstra
# Versione con nodi zero based.
# Il problema è con nodi 1 based, fissare i nodi prima dell'upload della soluzione

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

risposta = 0

#Calcola le distanze minime per ogni nodo a partire da nodo_start
def dijkstra(adj, N, nodo_start):    
    #Distanze. Inizializzo a infinito per ogni nodo e a 0 per nodo_start
    dist = [ float('inf') ] * N
    percorso = []

    # IMPLEMENTARE QUI LA SOLUZIONE

    return dist, percorso

#Calcolo il percorso minimo e distanze da nodo_start
distanze, percorso = dijkstra(adj, N, nodo_start)

risposta = distanze[nodo_stop]

print(risposta)

#print(percorso)
