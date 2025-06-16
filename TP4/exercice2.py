from multiprocessing import Process, Semaphore
from time import sleep

def tache1(sem):
    print("T1 démarre")
    sleep(2)
    print("T1 terminée")
    sem.release()  # signal que T1 est finie

def tache2(sem):
    print("T2 attend T1")
    sem.acquire()  # attend le signal de T1
    print("T2 démarre")
    sleep(2)
    print("T2 terminée")


sem = Semaphore(0)

p1 = Process(target=tache1, args=(sem,))
p2 = Process(target=tache2, args=(sem,))

p1.start()
p2.start()
p1.join()
p2.join()
