import signal
import sys
import time

def arreter(sig, frame):
    print("\nSignal SIGINT reçu. Fin du programme.")
    sys.exit(0)

signal.signal(signal.SIGINT, arreter)

while True:
    print("Travail en cours...")
    time.sleep(1)