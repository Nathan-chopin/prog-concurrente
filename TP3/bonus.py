import os
import signal
import time
import sys

def gestion_signal(signum, frame):
    if signum == signal.SIGUSR1:
        print("Petit Fils 1 : signal du meurtre du fils 1.")
    elif signum == signal.SIGUSR2:
        print("Petit Fils 2 : signal du meurtre du fils 2.")
    elif signum == signal.SIGUSR3:
        print("Petit Fils 3 : signal du meurtre du fils 3.")
    elif signum == signal.SIGUSR4:
        print("Petit Fils 4 : signal du meurtre du fils 4.")
    else:
        print("Fin.")
        sys.exit(0)

pid_pere = os.fork()



if pid_pere == 0:
    pid_fils1 = os.fork()
    if pid_fils1:
        petit_fils1 = os.fork()   

        # Processus petit_fils
        signal.signal(signal.SIGUSR1, gestion_signal)
        signal.signal(signal.SIGUSR2, gestion_signal)
        print(f"Petit Fils 1 : mon PID est {os.getpid()}")
        # boucle infinie en attente de signaux
        while True:
            signal.pause()  # attend un signal  

    else: 
        petit_fils2 = os.fork() 

        # Processus petit_fils
        signal.signal(signal.SIGUSR2, gestion_signal)
        print(f"Petit Fils 2 : mon PID est {os.getpid()}")
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

    pid_fils2 = os.fork()
    if pid_fils2:
        petit_fils3 = os.fork()  

        # Processus petit_fils
        signal.signal(signal.SIGUSR3, gestion_signal)
        print(f"Petit Fils 3 : mon PID est {os.getpid()}")
        # boucle infinie en attente de signaux
        while True:
            signal.pause()  # attend un signal  
   
    else: 
        petit_fils4 = os.fork() 

        # Processus petit_fils
        signal.signal(signal.SIGUSR4, gestion_signal)
        print(f"Petit Fils 4 : mon PID est {os.getpid()}")
        # boucle infinie en attente de signaux
        while True:
            signal.pause()  # attend un signal  

    

