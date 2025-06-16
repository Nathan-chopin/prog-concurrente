# Nathan CHOPIN et Maël PIERRON
# 16/06/25
# TODO : Done
from multiprocessing import Process, Queue
import random
import time

def calculateur(queue_demandes, queue_resultats):
    while True:
        data = queue_demandes.get()
        if data == "STOP":
            break
        id_demandeur, expr = data
        try:
            res = eval(expr)
        except Exception as e:
            res = f"Erreur : {e}"
        queue_resultats.put((id_demandeur, expr, res))
        time.sleep(1)

def demandeur(id_demandeur, queue_demandes, queue_resultats, expressions):
    for expr in expressions:
        print(f"Demandeur {id_demandeur} envoie : {expr}")
        queue_demandes.put((id_demandeur, expr))

    résultats_attendus = len(expressions)
    résultats_trouvés = 0
    tampons = []

    while résultats_trouvés < résultats_attendus:
        res = queue_resultats.get()
        id_res, expr_res, val_res = res

        if id_res == id_demandeur:
            print(f"Demandeur {id_demandeur} a reçu : {expr_res} = {val_res}")
            résultats_trouvés += 1
        else:
            tampons.append(res)

        if len(tampons) > 0:
            for r in tampons:
                queue_resultats.put(r)
            tampons.clear()

def generer_expressions(n):
    expressions = []
    for _ in range(n):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(['+', '-', '*', '/'])
        expressions.append(f"{a}{op}{b}")
    return expressions

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
        exprs = generer_expressions(5)
        p = Process(target=demandeur, args=(i, queue_demandes, queue_resultats, exprs))
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