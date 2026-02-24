import random

N = 5
M = 10

matrice = []

for _ in range(N):
    riga = []
    for _ in range(M):
        riga.append(0)
    
    matrice.append(riga)

matriceB = [  [ 0 for _ in range(M) ] for _ in range(N) ]

print( "a" * 10)
print( [3] * 10)
print()
matriceB = [ ([0] * M) for _ in range(N) ]
matriceC = [([0] * M)] * N # No! Sarebbe la stessa riga (ref) per N volte 

def print_matrice(matrice):
    for riga in matrice:
        print(riga)

for i in range( len(matriceB) ):
    for j in range( len(matriceB[i]) ):
        matriceB[i][j] = random.randint(1, 9)

print_matrice(matriceB)

# Calcolo del massimo + coordinate
max_i = 0
max_j = 0
for i in range( len(matriceB) ):
    for j in range( len(matriceB[i]) ):
        if matriceB[i][j] > matriceB[max_i][max_j]:
            max_i, max_j = i, j

print(f"\nValore massimo {matriceB[max_i][max_j]} trovato in {max_i}, {max_j}")
