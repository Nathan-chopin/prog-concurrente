from multiprocessing import Process, Queue
import random
import time

def calculateur(queue_demandes, queue_resultats):
    # Fonction exécutée par chaque processus calculateur
    while True:
        # Récupère une demande dans la queue des demandes
        data = queue_demandes.get()
        # Si la demande est "STOP", on termine la boucle et le processus
        if data == "STOP":
            break
        # On récupère l'id du demandeur et l'expression à calculer
        id_demandeur, expr = data
        try:
            # On évalue l'expression arithmétique
            res = eval(expr)
        except Exception as e:
            # En cas d'erreur dans l'expression, on stocke un message d'erreur
            res = f"Erreur : {e}"
        # On met le résultat dans la queue des résultats, avec l'id du demandeur
        queue_resultats.put((id_demandeur, expr, res))
        # Petite pause pour simuler un temps de calcul
        time.sleep(1)

def demandeur(id_demandeur, queue_demandes, queue_resultats, expressions):
    # Fonction exécutée par chaque demandeur
    # Envoie toutes ses expressions dans la queue des demandes
    for expr in expressions:
        print(f"Demandeur {id_demandeur} envoie : {expr}")
        queue_demandes.put((id_demandeur, expr))

    # Nombre de résultats attendus (autant que d'expressions envoyées)
    résultats_attendus = len(expressions)
    résultats_trouvés = 0
    tampons = []  # Liste temporaire pour stocker les résultats non destinés à ce demandeur

    # Tant que tous les résultats attendus n'ont pas été reçus
    while résultats_trouvés < résultats_attendus:
        # On récupère un résultat de la queue des résultats
        res = queue_resultats.get()
        id_res, expr_res, val_res = res

        if id_res == id_demandeur:
            # Si le résultat est destiné à ce demandeur, on l'affiche
            print(f"Demandeur {id_demandeur} a reçu : {expr_res} = {val_res}")
            résultats_trouvés += 1
        else:
            # Sinon on stocke temporairement le résultat pour un autre demandeur
            tampons.append(res)

        # On remet dans la queue les résultats non destinés à ce demandeur
        if len(tampons) > 0:
            for r in tampons:
                queue_resultats.put(r)
            tampons.clear()

def generer_expressions(n):
    # Génère n expressions arithmétiques aléatoires
    expressions = []
    for _ in range(n):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(['+', '-', '*', '/'])
        expressions.append(f"{a}{op}{b}")
    return expressions

def main():
    m = 2  # nombre de demandeurs
    n = 3  # nombre de calculateurs

    queue_demandes = Queue()   # queue commune pour toutes les demandes
    queue_resultats = Queue()  # queue commune pour tous les résultats

    # Création et démarrage des processus calculateurs
    calculateurs = [Process(target=calculateur, args=(queue_demandes, queue_resultats)) for _ in range(n)]
    for p in calculateurs:
        p.start()

    demandeurs = []
    # Création et démarrage des processus demandeurs
    for i in range(m):
        exprs = generer_expressions(5)  # chaque demandeur génère 5 expressions
        p = Process(target=demandeur, args=(i, queue_demandes, queue_resultats, exprs))
        demandeurs.append(p)
        p.start()

    # Attente de la fin de tous les demandeurs
    for p in demandeurs:
        p.join()

    # Envoi du signal d'arrêt aux calculateurs
    for _ in calculateurs:
        queue_demandes.put("STOP")

    # Attente de la fin de tous les calculateurs
    for p in calculateurs:
        p.join()

if __name__ == "__main__":
    main()