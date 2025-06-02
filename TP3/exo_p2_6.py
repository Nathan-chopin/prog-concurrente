import os
import signal
import time
import sys

def gestion_signal(signum, frame):
    if signum == signal.SIGUSR1:
        print("Fils : signal SIGUSR1 reçu, j'affiche ce message.")
    elif signum == signal.SIGUSR2:
        print("Fils : signal SIGUSR2 reçu, fin du traitement.")
        sys.exit(0)

pid_fils = os.fork()

if pid_fils == 0:
    # Processus fils
    signal.signal(signal.SIGUSR1, gestion_signal)
    signal.signal(signal.SIGUSR2, gestion_signal)
    print(f"Fils : mon PID est {os.getpid()}")
    # boucle infinie en attente de signaux
    while True:
        signal.pause()  # attend un signal

else:
    # Processus père
    for i in range(1, 6):
        print(f"Père : itération {i}")
        time.sleep(1)
        if i == 3 or i == 5:
            print(f"Père : j'envoie SIGUSR1 au fils (PID {pid_fils})")
            os.kill(pid_fils, signal.SIGUSR1)
    print(f"Père : j'envoie SIGUSR2 au fils (PID {pid_fils}) pour terminer")
    os.kill(pid_fils, signal.SIGUSR2)
    print("Père : fin de la boucle.")
