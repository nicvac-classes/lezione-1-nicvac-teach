#!/usr/bin/env python3
# NOTA: si raccomanda di usare questo template anche se non lo si capisce completamente.

import sys

# decommenta le due righe seguenti se vuoi leggere/scrivere da file
#sys.stdin = open('input.txt')
#sys.stdin = open('spegnitutto_input0.txt')
sys.stdin = open('spegnitutto_input_1.txt')
sys.stdout = open('output.txt', 'w')

T = int(input().strip())
for test in range(1, T+1):
    input()
    N = int(input().strip())

    A = list(map(int, input().strip().split()))

    ris = 0


    # INSERISCI IL TUO CODICE QUI

    # Conta le azioni necessarie
    azioni = 0
    i = 0
    
    while i < N:
        if A[i] == 1:  # Trovata lampadina accesa
            # Conta quante lampadine accese consecutive
            lunghezza = 0
            while i < N and A[i] == 1:
                lunghezza += 1
                i += 1
            # Per spegnere K lampadine consecutive servono ceil(K/2) azioni
            azioni += (lunghezza + 1) // 2
        else:
            i += 1

    ris = azioni
    ###

    print("Case #%d: " % test, end='')
    print(ris)

sys.stdout.close()
