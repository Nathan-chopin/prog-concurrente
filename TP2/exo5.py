import os
import sys
import time

if len(sys.argv) != 2:
    print("Usage : python programme.py N")
    sys.exit(1)

n = int(sys.argv[1])

for i in range(n):
    pid = os.fork()
    if pid == 0:
        # Processus fils : affiche son pid et celui de son père
        print(f"Fils {i} : pid = {os.getpid()}, père = {os.getppid()}")
        time.sleep(2 * i)  # Attend un temps proportionnel à i
        print(f"Fils {i} : fin attente ({2 * i} s)")
        sys.exit(i)  # Quitte avec un code de retour égal à i

for _ in range(n):
    pid_fils, etat = os.wait()  # Attend un processus fils terminé
    print(f"Fin du processus {pid_fils}, code retour = {os.WEXITSTATUS(etat)}")
