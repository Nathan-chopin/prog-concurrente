import signal
import time

fin = False

def arreter(sig, frame):
    global fin
    print("\nSignal SIGINT reçu. Fin demandée.")
    fin = True

signal.signal(signal.SIGINT, arreter)

while not fin:
    print("Travail en cours...")
    time.sleep(1)

print("Programme terminé proprement.")