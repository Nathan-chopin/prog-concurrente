# Nathan CHOPIN et Maël PIERRON
# 16/06/25
# TODO : Done
from multiprocessing import Process, Lock, Condition, Value
import time

def demander(k, nbr_disponible_billes, lock, condition):
    with lock:
        while nbr_disponible_billes.value < k:
            condition.wait()
        nbr_disponible_billes.value -= k

def rendre(k, nbr_disponible_billes, lock, condition):
    with lock:
        nbr_disponible_billes.value += k
        condition.notify_all()

def travailleur(id, k, m, nbr_disponible_billes, lock, condition):
    for i in range(m):
        print(f"Travailleur {id} demande {k} billes (cycle {i+1}/{m})")
        demander(k, nbr_disponible_billes, lock, condition)
        print(f"Travailleur {id} a obtenu {k} billes")
        time.sleep(k)
        rendre(k, nbr_disponible_billes, lock, condition)
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
    condition = Condition(lock)
    nbr_disponible_billes = Value('i', nb_max_billes)

    travailleurs = []
    for i, k in enumerate(k_demande):
        p = Process(target=travailleur, args=(i, k, m, nbr_disponible_billes, lock, condition))
        travailleurs.append(p)
        p.start()

    controleur_proc = Process(target=controleur, args=(nbr_disponible_billes, nb_max_billes, lock), daemon=True)
    controleur_proc.start()

    for p in travailleurs:
        p.join()

    print("Tous les travailleurs ont terminé.")

if __name__ == "__main__":
    main()