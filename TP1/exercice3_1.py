import os,sys
N = 10
v=1
while os.fork()==0 and v<=N :
    v += 1
print(v)
sys.exit(0)
"""
Ce programme crée des processus enfants via `fork()` qui incrémentent et affichent une variable partagée.
Sans synchronisation, cela produit un affichage désordonné (valeurs mélangées et dupliquées), illustrant parfaitement les risques d'accès concurrent non contrôlé.
Le parent affiche 1 puis reste actif, tandis que les enfants affichent 2 à 11 avant de terminer.
"""