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

    # Corrispondenze fra parentesi
    par_aperta = {
        '}': '{',
        ')': '(',
        ']': '[',
        '>': '<',
    }

    pila = []
    for parentesi in E:
        if parentesi in ['{','[','(','<']: #Se parentesi aperta
            pila.append(  parentesi )
        
        else: #Se parentesi chiusa
            #Se pila vuota e chiudo la parentesi, malformata    
            if len(pila) == 0:
                return False

            ultima_aperta = pila[-1] # top della pila
            if ultima_aperta == par_aperta[parentesi]: # la chiusa semplifica l'aperta corrispondente
                pila.pop()
            else:
                return False # una chiusa non corrispondente all'aperta
    
    #Se la pila è vuota ==> parentesi bilanciate
    return (len(pila) == 0)


N = int(input().strip())
E = input().strip()

if controlla(N, E) == False:
    print("malformata")
else:
    print("corretta")

sys.exit(0)
