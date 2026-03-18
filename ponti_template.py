# https://training.olinfo.it/task/ponti

import sys
from collections import deque

# Per la sottoposizione di questo problema in piattaforma: ATTIVARE QUESTE DUE RIGHE!
sys.stdin = open('input.txt')
sys.stdout = open('output.txt', 'w')

#sys.stdin = open('ponti_input01.txt')
#sys.stdout = open('output.txt', 'w')

#Funzione per contare le componenti connesse
def conta_componenti(adj):
    componenti = 0
    #implementare il conteggio delle componenti connesse
    return componenti

# Lettura input
N, M = map(int, input().split())

#Lista di adiacenza, implementata come dizionario
adj = {}
for nodo in range(N):
    # Inizializzare la lista di adiacenza con una lista vuota per ogni nodo
    pass

for _ in range(M):
    i, j = map(int, input().split())
    # Creare gli archi nella lista di adiacenza

# Calcolo e output
K = conta_componenti(adj)
# Se le componenti connesse sono K, le strade minime per connettere tutte le città sono K-1
print(K - 1)
