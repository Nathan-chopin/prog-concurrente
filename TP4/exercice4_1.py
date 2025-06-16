from multiprocessing import Process, Semaphore

def rdv1():
    print("P1 exécute rdv1 (après rendez-vous)")

def rdv2():
    print("P2 exécute rdv2 (après rendez-vous)")

def P1(sem_p1, sem_p2):
    print("P1 prêt, signale sa présence au rendez-vous")
    sem_p1.release()       # P1 dit : "Je suis prêt pour le rendez-vous"
    print("P1 attend que P2 soit prêt (attente du rendez-vous)")
    sem_p2.acquire()       # P1 attend que P2 signale sa présence
    print("P1 : Rendez-vous établi, on peut continuer")
    rdv1()                 # Exécution après rendez-vous

def P2(sem_p1, sem_p2):
    print("P2 prêt, signale sa présence au rendez-vous")
    sem_p2.release()       # P2 dit : "Je suis prêt pour le rendez-vous"
    print("P2 attend que P1 soit prêt (attente du rendez-vous)")
    sem_p1.acquire()       # P2 attend que P1 signale sa présence
    print("P2 : Rendez-vous établi, on peut continuer")
    rdv2()                 # Exécution après rendez-vous

if __name__ == "__main__":
    sem_p1 = Semaphore(0)
    sem_p2 = Semaphore(0)

    p1 = Process(target=P1, args=(sem_p1, sem_p2))
    p2 = Process(target=P2, args=(sem_p1, sem_p2))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Les deux processus ont fait leur rendez-vous et ont terminé.")
