import signal
import time

signal.signal(signal.SIGINT, signal.SIG_IGN)

while True:
    print("Travail en cours...")
    time.sleep(1)
    
# kill -9 numéro_PID