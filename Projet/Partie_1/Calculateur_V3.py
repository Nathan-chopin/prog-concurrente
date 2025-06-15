from multiprocessing import Process, Queue
import random
import time

def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def mul(x, y):
    return x * y

def div(x, y):
    if y == 0:
        return "division par zéro"
    return x / y

def calculateur(queue_demandes, queue_resultats):
    while True:
        data = queue_demandes.get()
        if data == "STOP":
            break
        id_demandeur, func, args = data
        try:
            res = func(*args)
        except Exception as e:
            res = f"Erreur : {e}"
        queue_resultats.put((id_demandeur, func.__name__, args, res))
        time.sleep(1)

def demandeur(id_demandeur, queue_demandes, queue_resultats, fonctions_args):
    for func, args in fonctions_args:
        print(f"Demandeur {id_demandeur} envoie : {func.__name__} avec args {args}")
        queue_demandes.put((id_demandeur, func, args))

    résultats_attendus = len(fonctions_args)
    résultats_trouvés = 0
    tampons = []

    while résultats_trouvés < résultats_attendus:
        res = queue_resultats.get()
        id_res, nom_func_res, args_res, val_res = res

        if id_res == id_demandeur:
            print(f"Demandeur {id_demandeur} a reçu : {nom_func_res}({args_res}) = {val_res}")
            résultats_trouvés += 1
        else:
            tampons.append(res)

        if len(tampons) > 0:
            for r in tampons:
                queue_resultats.put(r)
            tampons.clear()

def generer_fonctions_args(n):
    fonctions_args = []
    ops = [add, sub, mul, div]
    for _ in range(n):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        f = random.choice(ops)
        fonctions_args.append((f, (a, b)))
    return fonctions_args

def main():
    m = 2
    n = 3

    queue_demandes = Queue()
    queue_resultats = Queue()

    calculateurs = [Process(target=calculateur, args=(queue_demandes, queue_resultats)) for _ in range(n)]
    for p in calculateurs:
        p.start()

    demandeurs = []
    for i in range(m):
        fonctions_args = generer_fonctions_args(5)
        p = Process(target=demandeur, args=(i, queue_demandes, queue_resultats, fonctions_args))
        demandeurs.append(p)
        p.start()

    for p in demandeurs:
        p.join()

    for _ in calculateurs:
        queue_demandes.put("STOP")

    for p in calculateurs:
        p.join()

if __name__ == "__main__":
    main()