import os,sys
for i in range(4) :
    pid = os.fork()
    if pid != 0 :
        print("Ok !")
    print("Bonjour !")
sys.exit(0)
"""
Le programme affiche 32 "Ok !" 
(un par appel réussi à fork()) et 64 "Bonjour !" 
(chaque processus parent et enfant imprime une fois "Bonjour !" à chaque itération).
"""