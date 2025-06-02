from multiprocessing import Process, Queue
import random
import time

def calculateur(queue_demandes, queue_resultats):
    # Fonction exécutée par chaque processus calculateur
    print(f"Calculateur démarré PID={str(Process().pid)}")
    while True:
        # On attend une expression dans la file des demandes
        expr = queue_demandes.get()

        # Message d'arrêt reçu => on quitte la boucle et termine le processus
        if expr == "STOP":
            print("Calculateur reçu STOP, arrêt.")
            break
        
        try:
            # On évalue l'expression arithmétique reçue
            res = eval(expr)
        except Exception as e:
            # En cas d'erreur (ex: expression mal formée), on capture l'exception
            res = f"Erreur dans expression : {e}"

        # Affichage pour trace dans la console
        print(f"Calculateur calcule {expr} = {res}")

        # On place le résultat dans la file des résultats
        queue_resultats.put((expr, res))

        # Petite pause pour simuler le temps de calcul
        time.sleep(1)

def demandeur(queue_demandes, expressions):
    # Fonction exécutée par le processus demandeur
    for expr in expressions:
        # Affiche et envoie chaque expression à calculer dans la file des demandes
        print(f"Demandeur envoie : {expr}")
        queue_demandes.put(expr)

def generer_expressions(n):
    # Génère une liste d'expressions arithmétiques aléatoires
    expressions = []
    for _ in range(n):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(['+', '-', '*', '/'])
        expressions.append(f"{a}{op}{b}")
    # Ajoute volontairement une expression incorrecte pour test
    expressions.append("2 + 3 - ")
    return expressions

def main():
    # Création des files d'attente partagées entre processus
    queue_demandes = Queue()
    queue_resultats = Queue()

    n_calculateurs = 3  # Nombre de calculateurs

    # Création et lancement des processus calculateurs
    calculateurs = [Process(target=calculateur, args=(queue_demandes, queue_resultats)) for _ in range(n_calculateurs)]
    for p in calculateurs:
        p.start()

    # Génération des expressions à calculer
    expressions = generer_expressions(10)

    # Lancement du processus demandeur qui envoie les expressions
    p_demandeur = Process(target=demandeur, args=(queue_demandes, expressions))
    p_demandeur.start()
    p_demandeur.join()  # On attend que le demandeur ait fini d'envoyer toutes les expressions

    # Envoi d'un message STOP pour chaque calculateur pour leur indiquer d'arrêter
    for _ in calculateurs:
        queue_demandes.put("STOP")

    # On attend que tous les calculateurs se terminent proprement
    for p in calculateurs:
        p.join()

    print("\n=== Résultats reçus ===")
    # Récupération et affichage de tous les résultats disponibles
    while not queue_resultats.empty():
        expr, res = queue_resultats.get()
        print(f"{expr} = {res}")

if __name__ == "__main__":
    main()
