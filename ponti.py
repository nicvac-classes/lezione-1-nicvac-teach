# https://training.olinfo.it/task/ponti

import sys
from collections import deque

# Per la sottoposizione di questo problema in piattaforma: ATTIVARE QUESTE DUE RIGHE!
sys.stdin = open('input.txt')
sys.stdout = open('output.txt', 'w')

#sys.stdin = open('ponti_input01.txt')
#sys.stdout = open('output.txt', 'w')

def conta_componenti(adj):
    visitati = []
    componenti = 0

    for nodo in adj:
        if nodo not in visitati:
            componenti += 1
            coda = deque([nodo])
            visitati.append(nodo)
            while coda:
                corrente = coda.popleft()
                for vicino in adj[corrente]:
                    if vicino not in visitati:
                        visitati.append(vicino)
                        coda.append(vicino)

    return componenti

# Lettura input
N, M = map(int, input().split())

adj = {}
for nodo in range(N):
    adj[nodo] = []

for _ in range(M):
    i, j = map(int, input().split())
    adj[i].append(j)
    adj[j].append(i)

# Calcolo e output
K = conta_componenti(adj)
print(K - 1)
