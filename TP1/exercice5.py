import os

def afficher(debut, fin):
    for i in range(debut, fin + 1):
        print(f"PID {os.getpid()}: {i}")
if os.fork() == 0:
    afficher(1, 100)
    os._exit(0)

os.wait() #ajout pour que les nombres s'affichent bien dans l'ordre croissant

if os.fork() == 0:
    afficher(101, 200)
    os._exit(0)
    
