# Nathan CHOPIN et Maël PIERRON
# 16/06/25
# TODO : Done
from multiprocessing import Process, Lock, Value
import time

def demander_attente_active(k, nbr_disponible_billes, lock):
    while True:
        lock.acquire()
        if nbr_disponible_billes.value >= k:
            nbr_disponible_billes.value -= k
            lock.release()
            break
        lock.release()
        time.sleep(0.5)

def rendre_attente_active(k, nbr_disponible_billes, lock):
    with lock:
        nbr_disponible_billes.value += k

def travailleur(id, k, m, nbr_disponible_billes, lock):
    for i in range(m):
        print(f"Travailleur {id} demande {k} billes (cycle {i+1}/{m})")
        demander_attente_active(k, nbr_disponible_billes, lock)
        print(f"Travailleur {id} a obtenu {k} billes")
        time.sleep(k)
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
    k_demande = [4, 3, 5, 2]
    m = 3

    lock = Lock()
    nbr_disponible_billes = Value('i', nb_max_billes)

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