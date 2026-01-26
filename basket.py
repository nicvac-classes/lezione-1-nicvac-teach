#!/usr/bin/env python3
# NOTA: si raccomanda di usare questo template anche se non lo si capisce completamente.

import sys

# decommenta le due righe seguenti se vuoi leggere/scrivere da file
# sys.stdin = open('input.txt')
# sys.stdin = open('basket_input01.txt')
sys.stdin = open('basket_input_3.txt')
sys.stdout = open('output.txt', 'w')

T = int(input().strip())
for test in range(1, T+1):
    input()
    N = int(input().strip())

    A = list(map(int, input().strip().split()))

    B = list(map(int, input().strip().split()))

    x = 0

    # INSERISCI IL TUO CODICE QUI
    A.sort()
    B.sort()

    comuni = 0
    i = 0
    j = 0
    while ( i<N and j<N):
        if A[i] == B[j]:
            comuni += 1
            i += 1
            j += 1
        elif A[i] < B[j]:
            i += 1
        else:
            j += 1
    x = comuni
    ###


    print("Case #%d: " % test, end='')
    print(x)

sys.stdout.close()
