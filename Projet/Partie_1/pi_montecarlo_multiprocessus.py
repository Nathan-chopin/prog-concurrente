# Nathan CHOPIN et Maël PIERRON
# 16/06/25
# TODO : Done
import random
import time
from multiprocessing import Process, Queue

def frequence_de_hits_pour_n_essais(nb_iteration, queue):
    count = 0
    for _ in range(nb_iteration):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1:
            count += 1
    queue.put(count)

if __name__ == "__main__":
    nb_total_iteration = 10_000_000
    nb_processus = 4
    iterations_par_processus = nb_total_iteration // nb_processus

    queue = Queue()
    processes = []

    debut = time.time()

    for _ in range(nb_processus):
        p = Process(target=frequence_de_hits_pour_n_essais, args=(iterations_par_processus, queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    nb_hits_total = sum(queue.get() for _ in processes)
    fin = time.time()

    pi_estime = 4 * nb_hits_total / (iterations_par_processus * nb_processus)
    print("Valeur estimée Pi (Multi-Processus) :", pi_estime)
    print("Durée d'exécution (Multi-Processus) :", fin - debut, "secondes")