# Nathan CHOPIN et Maël PIERRON
# 16/06/25
# TODO : Done
from multiprocessing import Process, Queue
import random
import time

def calculateur(queue_demandes, queue_resultats):
    print(f"Calculateur démarré PID={str(Process().pid)}")
    while True:
        expr = queue_demandes.get()

        if expr == "STOP":
            print("Calculateur reçu STOP, arrêt.")
            break
        
        try:
            res = eval(expr)
        except Exception as e:
            res = f"Erreur dans expression : {e}"

        print(f"Calculateur calcule {expr} = {res}")
        queue_resultats.put((expr, res))
        time.sleep(1)

def demandeur(queue_demandes, expressions):
    for expr in expressions:
        print(f"Demandeur envoie : {expr}")
        queue_demandes.put(expr)

def generer_expressions(n):
    expressions = []
    for _ in range(n):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(['+', '-', '*', '/'])
        expressions.append(f"{a}{op}{b}")
    expressions.append("2 + 3 - ")
    return expressions

def main():
    queue_demandes = Queue()
    queue_resultats = Queue()

    n_calculateurs = 3

    calculateurs = [Process(target=calculateur, args=(queue_demandes, queue_resultats)) for _ in range(n_calculateurs)]
    for p in calculateurs:
        p.start()

    expressions = generer_expressions(10)

    p_demandeur = Process(target=demandeur, args=(queue_demandes, expressions))
    p_demandeur.start()
    p_demandeur.join()

    for _ in calculateurs:
        queue_demandes.put("STOP")

    for p in calculateurs:
        p.join()

    print("\n=== Résultats reçus ===")
    while not queue_resultats.empty():
        expr, res = queue_resultats.get()
        print(f"{expr} = {res}")

if __name__ == "__main__":
    main()