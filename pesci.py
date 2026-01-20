#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys

# se preferisci leggere e scrivere da file
# ti basta decommentare le seguenti due righe:

sys.stdin = open('input.txt')
# sys.stdin = open('pesci_input01.txt')
sys.stdout = open('output.txt', 'w')

def solve():
    input()
    N, K = map(int, input().split())
    
    # aggiungi codice...
    risposta = N
    while N >= K:
        N = N // K
        risposta = risposta + N

    return risposta


T = int(input())

for t in range(1, T+1):
    print("Case #" + str(t) + ":", solve())
