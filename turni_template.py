# https://training.olinfo.it/task/turni

import sys

# Per la sottoposizione di questo problema in piattaforma: ATTIVARE QUESTE DUE RIGHE!
sys.stdin = open('input.txt')
sys.stdout = open('output.txt', 'w')

#sys.stdin = open('turni_input01.txt')
#sys.stdout = open('output.txt', 'w')

K = int(input())
N = int(input())

persone = []
for _ in range(N):
    a, b = map(int, input().split())
    persone.append((a, b))

risposta = 0

# SCRIVI QUI LA SOLUZIONE


print(risposta)