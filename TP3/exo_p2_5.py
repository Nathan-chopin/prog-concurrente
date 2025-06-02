import os
import signal
import time
import sys

def intercepter_SIGINT(sig, frame):
    print("Fils : signal SIGINT intercepté.")

pid_fils = os.fork()

if pid_fils == 0:
    # Processus fils
    signal.signal(signal.SIGINT, intercepter_SIGINT)
    while True:
        print("Fils : je travaille...")
        time.sleep(1)
else:
    # Processus père
    for i in range(5):
        print(f"Père : tour {i + 1}")
        time.sleep(1)
    print("Père : fin de la boucle.")

"""
Il 'est pas possible pour le fils de continuer à intercepter les SIGINT après la mort du père car il devient alors
orphelin et s'execute en arrière-plan. Il n'est alors plus impacté par les SIGINT. 
"""