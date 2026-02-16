#!/usr/bin/env python3
# NOTE: it is recommended to use this even if you don't understand the following code.

import math
import sys

# uncomment the two following lines if you want to read/write from files
#sys.stdin = open('countturns_input0.txt')
#sys.stdout = open('output.txt', 'w')

T = int(input().strip())
for test in range(1, T+1):
    N, K = map(int, input().strip().split())

    S = ""

    #Minimo comune multiplo fra max K pietre e i due giocatori
    L = math.lcm(2,K)

    # d[n][t] = True se Alice vince con n pietre rimaste e t turni giocati (mod L)
    d = [ [False for j in range(L+1)] for i in range(N+1) ]


    # Caso base: 0 pietre, allora Alice vince se turni divisibili per K
    for t in range(L):
        d[0][t] = (t % K == 0)

    # Riempio la matrice d delle pietre rimaste e turni
    for n in range(1, N + 1):
        for t in range(L):
            t_succ = (t + 1) % L
            max_presa = min(K, n)

            if t % 2 == 0:
                # Turno di Alice: basta UNA mossa vincente
                d[n][t] = any(d[n - i][t_succ] for i in range(1, max_presa + 1))
            else:
                # Turno di Bob: TUTTE le mosse devono essere vincenti per Alice
                d[n][t] = all(d[n - i][t_succ] for i in range(1, max_presa + 1))    


    S = "Alice" if d[N][0] else "Bob"

    print(S)

sys.stdout.close()
