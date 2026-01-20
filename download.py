#!/usr/bin/env python3
# NOTA: si raccomanda di usare questo template anche se non lo si capisce completamente.

import sys

# decommenta le due righe seguenti se vuoi leggere/scrivere da file
#sys.stdin = open('download_input01.txt')
sys.stdin = open('input.txt')
sys.stdout = open('output.txt', 'w')

T = int(input().strip())
for test in range(1, T+1):
    input()
    N, F, C = map(int, input().strip().split())

    nf = 0
    nc = 0

    # INSERISCI IL TUO CODICE QUI
    nf = N // F
    left = N - (nf*F)
    nc = left // C

    print("Case #%d: " % test, end='')
    print(nf, nc)

sys.stdout.close()
