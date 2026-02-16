# https://training.olinfo.it/task/ois_parentesi

import sys

# Per la sottoposizione di questo problema in piattaforma: ATTIVARE QUESTE DUE RIGHE!
sys.stdin = open('input.txt')
sys.stdout = open('output.txt', 'w')

#sys.stdin = open('parentesi_input04.txt')
#sys.stdout = open('output.txt', 'w')

def controlla(N, E):
    # SCRIVERE QUI LA SOLUZIONE
    # N: dimensione dell'espressione E
    # E: espressione da controllare
    # Tornare True se E ben formata

    return True


N = int(input().strip())
E = input().strip()

if controlla(N, E) == False:
    print("malformata")
else:
    print("corretta")

sys.exit(0)
