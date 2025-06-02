import signal

def timeout(signum, frame):
    print("\nTrop tard !!")
    exit(0)

signal.signal(signal.SIGALRM, timeout)
signal.alarm(5) #envoie le signal SIGALARM au bout de 5s si non desactivé

print("Entrez un entier en moins de 5 secondes")

while True:
    try:
        saisie = input("Svp un entier : ")
        entier = int(saisie)
        signal.alarm(0) #desactive l'alarme
        print("Ok merci !!")
        break
    except ValueError:
        continue