#!/usr/bin/env python3
# NOTE: it is recommended to use this even if you don't understand the following code.

import sys

# se preferisci leggere e scrivere da file
# ti basta decommentare le seguenti due righe:

sys.stdin = open('keyboardshift_input2.txt')
sys.stdout = open('output.txt', 'w')


# input data
N = int(input().strip())
S = input().strip()


# insert your code here
tastiFila1 = "qwertyuiop"
tastiFila2 = "asdfghjkl"
tastiFila3 = "zxcvbnm"

tastiera = {}
i = 0
for i in range(0, len(tastiFila1)-1 ):
    digitato = tastiFila1[i]
    corretto = tastiFila1[i+1]
    tastiera[ digitato ] = corretto


for i in range(0, len(tastiFila2)-1 ):
    digitato = tastiFila2[i]
    corretto = tastiFila2[i+1]
    tastiera[ digitato ] = corretto

for i in range(0, len(tastiFila3)-1 ):
    digitato = tastiFila3[i]
    corretto = tastiFila3[i+1]
    tastiera[ digitato ] = corretto

corretto = ''
for i in range(0, len(S)):
    carattere = S[i]
    corretto += tastiera[ carattere ]

S = corretto

print(S)  # print the result
