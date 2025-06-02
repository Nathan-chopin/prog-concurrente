from multiprocessing import Process, Lock, Value
import time

def demander_attente_active(k, nbr_disponible_billes, lock):
    while True:
        lock.acquire()
        if nbr_disponible_billes.value >= k:
            nbr_disponible_billes.value -= k
            lock.release()
            break  # On a pris les billes, on sort de la boucle
        lock.release()
        time.sleep(0.5)  # Pause pour ne pas saturer l'ordi, attente active

def rendre_attente_active(k, nbr_disponible_billes, lock):
    with lock:
        nbr_disponible_billes.value += k
        # Pas de notification ici, car pas d'attente passive

def travailleur(id, k, m, nbr_disponible_billes, lock):
    for i in range(m):
        print(f"Travailleur {id} demande {k} billes (cycle {i+1}/{m})")
        demander_attente_active(k, nbr_disponible_billes, lock)
        print(f"Travailleur {id} a obtenu {k} billes")
        time.sleep(k)  # Simule l'utilisation des billes
        rendre_attente_active(k, nbr_disponible_billes, lock)
        print(f"Travailleur {id} a rendu {k} billes")

def controleur(nbr_disponible_billes, nb_max_billes, lock):
    while True:
        with lock:
            dispo = nbr_disponible_billes.value
            assert 0 <= dispo <= nb_max_billes, f"Nombre de billes hors limite: {dispo}"
            print(f"[Controleur] Billes disponibles : {dispo}/{nb_max_billes}")
        time.sleep(1)

def main():
    nb_max_billes = 9
    k_demande = [4, 3, 5, 2]  # demande par chaque travailleur
    m = 3  # nombre de cycles pour chaque travailleur

    lock = Lock()
    nbr_disponible_billes = Value('i', nb_max_billes)  # variable partagée

    travailleurs = []
    for i, k in enumerate(k_demande):
        p = Process(target=travailleur, args=(i, k, m, nbr_disponible_billes, lock))
        travailleurs.append(p)
        p.start()

    controleur_proc = Process(target=controleur, args=(nbr_disponible_billes, nb_max_billes, lock), daemon=True)
    controleur_proc.start()

    for p in travailleurs:
        p.join()

    print("Tous les travailleurs ont terminé.")

if __name__ == "__main__":
    main()