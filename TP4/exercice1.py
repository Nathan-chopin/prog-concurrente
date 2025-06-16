from multiprocessing import Process, Value, Lock

def somme_impairs(liste, somme):
    for i in range(1, len(liste), 2):
        with lock:
            somme.value += liste[i]

def somme_pairs(liste, somme):
    for i in range(0, len(liste), 2):
        with lock:
            somme.value += liste[i]

L = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
somme = Value('i', 0) #création d'une variable partagée

p1 = Process(target=somme_impairs, args=(L, somme))
p2 = Process(target=somme_pairs, args=(L, somme))

lock = Lock()

p1.start()
p2.start()
p1.join()
p2.join()

print("Somme totale :", somme.value)
