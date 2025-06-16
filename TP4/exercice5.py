from multiprocessing import Process, Semaphore, Lock, Value
import sys
import time

def emetteur(num, sem_rdv, verrou, compteur, taille_groupe):
    print(f"Le processus {num} émetteur produit un message et se met en attente")
    time.sleep(0.1)  # Simuler la production du message
    with verrou:
        compteur.value += 1  # Indiquer qu'un participant est arrivé au rendez-vous
        if compteur.value == taille_groupe:
            # Si tous les participants du groupe sont arrivés,
            # on libère la barrière pour laisser tout le monde continuer
            for _ in range(taille_groupe):
                sem_rdv.release()
    sem_rdv.acquire()  # Attente du rendez-vous avec les autres processus
    print(f"Le processus {num} émetteur débloqué, message consommé")

def recepteur(num, sem_rdv, verrou, compteur, taille_groupe):
    print(f"Le processus {num} récepteur se met en attente")
    time.sleep(0.1)  # Simuler l'attente avant d'arriver au rendez-vous
    with verrou:
        compteur.value += 1  # Indiquer qu'un participant est arrivé au rendez-vous
        if compteur.value == taille_groupe:
            # Quand tout le groupe est là, libérer la barrière pour tous
            for _ in range(taille_groupe):
                sem_rdv.release()
    sem_rdv.acquire()  # Attente que le rendez-vous soit complet
    print(f"Le processus {num} récepteur débloqué, message consommé")

def main(args):
    if len(args) < 2:
        print("Usage : python script.py R E E R R R")
        return

    taille_groupe = 3  # 1 émetteur + 2 récepteurs par groupe rendez-vous

    sem_rdv = Semaphore(0)  # Sémaphore pour synchroniser les processus d'un groupe
    verrou = Lock()         # Verrou pour protéger l'accès au compteur
    compteur = Value('i', 0)  # Compteur partagé du nombre de participants arrivés

    processus = []
    compteur_groupe = 0  # Compteur du nombre de processus dans le groupe courant

    for i, role in enumerate(args, 1):
        # Dès qu'un nouveau groupe commence, on réinitialise compteur et sémaphore
        if compteur_groupe == 0:
            compteur.value = 0
            sem_rdv = Semaphore(0)

        if role == 'E':
            p = Process(target=emetteur, args=(i, sem_rdv, verrou, compteur, taille_groupe))
        elif role == 'R':
            p = Process(target=recepteur, args=(i, sem_rdv, verrou, compteur, taille_groupe))
        else:
            print(f"Rôle inconnu {role} pour le processus {i}")
            continue

        p.start()
        processus.append(p)

        compteur_groupe += 1
        # Dès que le groupe est complet, on passe au groupe suivant
        if compteur_groupe == taille_groupe:
            compteur_groupe = 0

    # On attend que tous les processus se terminent proprement
    for p in processus:
        p.join()

if __name__ == "__main__":
    main(sys.argv[1:])