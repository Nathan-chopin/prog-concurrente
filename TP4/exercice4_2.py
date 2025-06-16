from multiprocessing import Process, Semaphore, Lock, Value
import time

def rdv(name):
    print(f"{name} exécute sa fonction après rendez-vous")

def processus(name, sem_arrive, sem_depart, lock, count, total):
    print(f"{name} est prêt pour le rendez-vous")
    sem_arrive.release()  # Signale qu'il est arrivé au rendez-vous

    with lock:
        count.value += 1
        if count.value == total:
            print(f"{name} constate que tous sont prêts, libération des participants")
            for _ in range(total):
                sem_depart.release()  # Libère tous les processus

    print(f"{name} attend que tous soient prêts")
    sem_depart.acquire()  # Attend que tout le monde soit prêt
    print(f"{name} : Rendez-vous établi, on peut continuer")
    rdv(name)

if __name__ == "__main__":
    total_processus = 3
    sem_arrive = Semaphore(0)
    sem_depart = Semaphore(0)
    lock = Lock()
    count = Value('i', 0)

    p1 = Process(target=processus, args=("P1", sem_arrive, sem_depart, lock, count, total_processus))
    p2 = Process(target=processus, args=("P2", sem_arrive, sem_depart, lock, count, total_processus))
    p3 = Process(target=processus, args=("P3", sem_arrive, sem_depart, lock, count, total_processus))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    print("Tous les processus ont fait leur rendez-vous.")
