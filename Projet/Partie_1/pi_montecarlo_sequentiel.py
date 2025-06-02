import random
import time

def frequence_de_hits_pour_n_essais(nb_iteration):
    count = 0
    for _ in range(nb_iteration):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1:
            count += 1
    return count

if __name__ == "__main__":
    nb_total_iteration = 10_000_000
    debut = time.time()
    nb_hits = frequence_de_hits_pour_n_essais(nb_total_iteration)
    fin = time.time()
    pi_estime = 4 * nb_hits / nb_total_iteration
    print("Valeur estimée Pi (Mono-Processus) :", pi_estime)
    print("Durée d'exécution (Mono-Processus) :", fin - debut, "secondes")