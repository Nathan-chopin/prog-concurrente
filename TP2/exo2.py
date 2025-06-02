import os

for i in range(3):
    retour = os.fork()
    print(f"(i : {i}) je suis le processus : {os.getpid()}, mon pere est : {os.getppid()}, retour : {retour}")
#arbre des processus : cf tablette Tathan