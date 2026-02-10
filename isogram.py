#!/usr/bin/env python3
# https://training.olinfo.it/task/ois_isogram
# NOTE: it is recommended to use this even if you don't understand the following code.

import sys

sys.stdin = open('isogram_input1.txt')
sys.stdout = open('output.txt', 'w')

# contatore delle parole isogram
risposta = 0

# input data
N = int(input().strip())

for i in range(N):
    S = input().strip()

    # insert your code here

    #Si considerano solo i caratteri alfabetici (ignorando numeri, spazi, punteggiatura).
    s_alfa = ""
    for i in range(0, len(S)):
        if S[i].isalpha():
            s_alfa += S[i]

    #Non si fa distinzione tra maiuscole e minuscole (case-insensitive).
    s_alfa = s_alfa.lower()

    #Nessuna lettera compare più di 2 volte.
    #Conto le occorrenze di ogni lettera usando un dizionario.
    isogram = True
    contatori = {}
    for c in s_alfa:
        if c not in contatori:
            contatori[c] = 1
        else:
            contatori[c] += 1
        
        if contatori[c] > 2:
            isogram = False
            break # Interrompo subito il controllo

    #Controllo
    if isogram:
        risposta += 1 
    

print(risposta)  # print the result
