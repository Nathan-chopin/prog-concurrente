from multiprocessing import Process, Lock, Condition, Value
import time
  
def demander(k, nbr_disponible_billes, lock, condition):
    with lock:
        # Tant que le nombre de billes dispo est insuffisant
        while nbr_disponible_billes.value < k:
            # On attend sur la condition (libère le verrou et se bloque)
            condition.wait()
        # Quand réveillé, on réévalue la condition, puis on "prend" les billes
        nbr_disponible_billes.value -= k

def rendre(k, nbr_disponible_billes, lock, condition):
    with lock:
        nbr_disponible_billes.value += k
        # On notifie tous les processus en attente (ils peuvent vérifier s'ils peuvent continuer)
        condition.notify_all()

def travailleur(id, k, m, nbr_disponible_billes, lock, condition):
    for i in range(m):
        print(f"Travailleur {id} demande {k} billes (cycle {i+1}/{m})")
        demander(k, nbr_disponible_billes, lock, condition)
        print(f"Travailleur {id} a obtenu {k} billes")
        time.sleep(k)  # Simule l'utilisation des billes
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
    k_demande = [4, 3, 5, 2]  # demande par chaque travailleur
    m = 3  # nombre de cycles pour chaque travailleur

    lock = Lock()
    condition = Condition(lock)
    nbr_disponible_billes = Value('i', nb_max_billes)  # variable partagée, initialisée à nb_max_billes

    # Création des travailleurs
    travailleurs = []
    for i, k in enumerate(k_demande):
        p = Process(target=travailleur, args=(i, k, m, nbr_disponible_billes, lock, condition))
        travailleurs.append(p)
        p.start()

    # Création du contrôleur
    controleur_proc = Process(target=controleur, args=(nbr_disponible_billes, nb_max_billes, lock), daemon=True)
    controleur_proc.start()

    # Attente de la fin des travailleurs
    for p in travailleurs:
        p.join()

    # Terminaison du contrôleur (processus daemon s'arrête automatiquement quand main termine)
    print("Tous les travailleurs ont terminé.")

if __name__ == "__main__":
    main()