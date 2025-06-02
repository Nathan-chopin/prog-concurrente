"""
ATTENTION !!! Utiliser 3 consoles différentes :
-Dans la premièr, python3 filtrePair.py
-Dans la deuxième, python3 filtreImpair.py
-Dans la troisième, python3 generateurNombres.py
☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺
"""

import os
import random

for fifo in ["nombresPairs", "nombresImpairs", "sommePairs", "sommeImpairs"]:
    try:
        os.mkfifo(fifo)
    except FileExistsError:
        pass

N = 20

fpairs = open("nombresPairs", "w")
fimpairs = open("nombresImpairs", "w")

for _ in range(N):
    x = random.randint(0, 100)
    if x % 2 == 0:
        fpairs.write(str(x) + "\n")
    else:
        fimpairs.write(str(x) + "\n")

fpairs.write("-1\n")
fimpairs.write("-1\n")

fpairs.close()
fimpairs.close()

fsommePairs = open("sommePairs", "r")
fsommeImpairs = open("sommeImpairs", "r")

somme_pairs = int(fsommePairs.readline())
somme_impairs = int(fsommeImpairs.readline())

fsommePairs.close()
fsommeImpairs.close()

print("Somme des nombres pairs =", somme_pairs)
print("Somme des nombres impairs =", somme_impairs)
print("Somme totale =", somme_pairs + somme_impairs)