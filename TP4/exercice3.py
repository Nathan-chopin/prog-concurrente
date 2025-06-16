from multiprocessing import Process, Queue, Semaphore, Lock, Value
import random
import time

def producteur(q, sem, n_messages, name):
    for _ in range(n_messages):
        msg = random.randint(1, 100)
        q.put(msg)
        sem.release()  # Signal qu'un message est disponible
        print(f"{name} produit : {msg}")
        time.sleep(0.1)
    print(f"{name} a terminé la production.")

def consommateur(q, sem, rendez_vous_sem1, rendez_vous_sem2, lock, count, n_messages, name):
    for _ in range(n_messages):
        sem.acquire()  # Attente d'un message disponible
        msg = q.get()
        print(f"{name} consomme : {msg}")
        with lock:
            count.value += 1
            if count.value == 2:
                count.value = 0
                print(f"{name} et son collègue ont consommé, rendez-vous validé.")
                rendez_vous_sem1.release()
                rendez_vous_sem2.release()
        if name == "C1":
            rendez_vous_sem1.acquire()  # Attente que l'autre consommateur ait consommé aussi
        else:
            rendez_vous_sem2.acquire()
        time.sleep(0.1)
    print(f"{name} a terminé la consommation.")

if __name__ == "__main__":
    n = 5  # Nombre de messages à produire/consommer chacun

    q1 = Queue()
    q2 = Queue()

    sem_q1 = Semaphore(0)
    sem_q2 = Semaphore(0)

    rendez_vous_sem1 = Semaphore(0)
    rendez_vous_sem2 = Semaphore(0)

    lock = Lock()
    count = Value('i', 0)

    p1 = Process(target=producteur, args=(q1, sem_q1, n, "P1"))
    p2 = Process(target=producteur, args=(q2, sem_q2, n, "P2"))
    c1 = Process(target=consommateur, args=(q1, sem_q1, rendez_vous_sem1, rendez_vous_sem2, lock, count, n, "C1"))
    c2 = Process(target=consommateur, args=(q2, sem_q2, rendez_vous_sem1, rendez_vous_sem2, lock, count, n, "C2"))

    p1.start()
    p2.start()
    c1.start()
    c2.start()

    p1.join()
    p2.join()
    c1.join()
    c2.join()

    print("Fin du programme : tous les messages ont été traités.")
