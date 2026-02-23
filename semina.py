# https://training.olinfo.it/task/abc_semina

import sys

# Per la sottoposizione di questo problema in piattaforma: DISATTIVARE QUESTE DUE RIGHE!
#sys.stdin = open('semina_input01.txt')
#sys.stdout = open('output.txt', 'w')

# Vincolo: −100 < Xi,Yi,Xf,Yf < 100.
# Quindi le coordinate vanno da -99 a 99, quindi sono 199 coordinate possibili ==> Le riporto in [0,198]
# Il campo è formato massimo da 199x199 celle
offset = 99
size = 199

campo = [
      [ 0 for _ in range(size) ]
      for _ in range(size)
    ]

#Coordinate del campo con il valore più alto
max_i = 0
max_j = 0

N = int(input().strip())
for k in range(N):
    L = list(map(int, input().strip().split()))

    # Per ogni semina, vale che Xi<Xf e Yf<Yi.
    xi = L[0] + offset
    yi = L[1] + offset
    xf = L[2] + offset
    yf = L[3] + offset

    # v. figura spiegazione output ==> xf e yi sono esclusi (area racchiusa, estremi non compresi)
    for i in range( xi, xf ):
        for j in range( yf, yi ): # Yf<Yi.
            campo[i][j] += 1
            # Calcolo il massimo, man mano che semino
            if campo[i][j] > campo[max_i][max_j]:
                max_i = i
                max_j = j


print(campo[max_i][max_j])


sys.exit(0)
