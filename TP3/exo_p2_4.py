import os
import signal
import time

pid_fils = os.fork()

if pid_fils == 0:
    # Processus fils
    while True:
        print("Fils : je travaille...")
        time.sleep(1)
else:
    # Processus père
    for i in range(5):
        print(f"Père : tour {i + 1}")
        time.sleep(1)
        if i == 2:  # au 3e tour (i = 2)
            print("Père : je tue le fils.")
            os.kill(pid_fils, signal.SIGKILL)

    print("Père : fin de la boucle.")