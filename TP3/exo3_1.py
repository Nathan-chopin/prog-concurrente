import os
import sys
import random

def ecrire_str(fd, s):
    # écrit la chaîne s encodée en bytes, avec un \n à la fin
    os.write(fd, (s + '\n').encode()) #transforme le str en byte

def lire_ligne(fd):
    # lit un "ligne" terminée par \n depuis fd, renvoie une chaîne sans \n
    ligne = b''
    while True:
        c = os.read(fd, 1)
        if not c:
            # fin de fichier
            if ligne:
                return ligne.decode() #pareil qu'avant mais en pas pareil
            else:
                return None
        if c == b'\n':
            break
        ligne += c
    return ligne.decode()

N = 20

rPairs, wPairs = os.pipe()
rImpairs, wImpairs = os.pipe()
rSommePairs, wSommePairs = os.pipe()
rSommeImpairs, wSommeImpairs = os.pipe()

pid_paire = os.fork()
if pid_paire == 0:
    os.close(wPairs)
    os.close(rSommePairs)
    somme = 0
    while True:
        ligne = lire_ligne(rPairs)
        if ligne is None:
            break
        n = int(ligne)
        if n == -1:
            break
        somme += n
    os.close(rPairs)
    ecrire_str(wSommePairs, str(somme))
    os.close(wSommePairs)
    sys.exit(0)

pid_impair = os.fork()
if pid_impair == 0:
    os.close(wImpairs)
    os.close(rSommeImpairs)
    somme = 0
    while True:
        ligne = lire_ligne(rImpairs)
        if ligne is None:
            break
        n = int(ligne)
        if n == -1:
            break
        somme += n
    os.close(rImpairs)
    ecrire_str(wSommeImpairs, str(somme))
    os.close(wSommeImpairs)
    sys.exit(0)

os.close(rPairs)
os.close(rImpairs)
os.close(wSommePairs)
os.close(wSommeImpairs)

for _ in range(N):
    x = random.randint(0, 100)
    if x % 2 == 0:
        ecrire_str(wPairs, str(x))
    else:
        ecrire_str(wImpairs, str(x))

ecrire_str(wPairs, '-1')
ecrire_str(wImpairs, '-1')

os.close(wPairs)
os.close(wImpairs)

somme_pairs = int(lire_ligne(rSommePairs))
somme_impairs = int(lire_ligne(rSommeImpairs))

os.close(rSommePairs)
os.close(rSommeImpairs)

print(f"Somme des nombres pairs = {somme_pairs}")
print(f"Somme des nombres impairs = {somme_impairs}")
print(f"Somme totale = {somme_pairs + somme_impairs}")

os.waitpid(pid_paire, 0)
os.waitpid(pid_impair, 0)
