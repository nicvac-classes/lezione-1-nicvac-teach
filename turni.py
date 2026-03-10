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

# Ordino le persone in base al loro primo giorno disponibile
# Gli elementi di persone sono dei pair (inizio, fine). Mi interessa che siano ordinate su inizio, 
# quindi l'ordinamento su pair python mi va bene
persone.sort()

giorno = 0    # prossimo giorno da coprire
i = 0         # indice nella lista ordinata di persone

while giorno < K:
    
    miglior_fine = -1

    # Raccolgo tutte persone che hanno inizio turno <= giorno coperto
    persone_da_scegliere = []
    while i < N:
        persona = persone[i]
        if persona[0] <= giorno:
            # Fra le persone con inizio turno compatibile, 
            persone_da_scegliere.append( persona )
            i += 1
        else:
            # interrompo la ricerca se non ci sono altre persone che 
            # coprono il giorno richiesto
            break 

    # fra tutte le persone con giorno inizio compatibile,
    # seleziono quella con la fine turno più lontano possibile
    for pers in persone_da_scegliere:
        miglior_fine = max( miglior_fine, pers[1] )

    risposta += 1 # Ho trovato un'altra persona (la migliore disponibile)

    # Ho coperto fino a miglior_fine, nel prossimo loop cerco chi può coprire il prossimo giorno.
    giorno = miglior_fine + 1


print(risposta)