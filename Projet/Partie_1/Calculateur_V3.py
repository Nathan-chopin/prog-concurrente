from multiprocessing import Process, Queue
import random
import time

# Fonctions définies au niveau global pour pouvoir être envoyées via multiprocessing (picklables)
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

# Processus calculateur : récupère les demandes, exécute la fonction avec les arguments et place le résultat
def calculateur(queue_demandes, queue_resultats):
    while True:
        data = queue_demandes.get()  # Récupère une demande (id_demandeur, fonction, arguments)
        if data == "STOP":           # Condition d'arrêt
            break
        id_demandeur, func, args = data
        try:
            res = func(*args)         # Exécution de la fonction avec déballage des arguments
        except Exception as e:
            res = f"Erreur : {e}"    # En cas d'erreur, on stocke le message d'erreur
        # On place dans la queue des résultats : id_demandeur, nom de la fonction, arguments, résultat
        queue_resultats.put((id_demandeur, func.__name__, args, res))
        time.sleep(1)                 # Petite pause pour simuler un calcul un peu long

# Processus demandeur : envoie ses demandes et récupère ses résultats correspondants
def demandeur(id_demandeur, queue_demandes, queue_resultats, fonctions_args):
    for func, args in fonctions_args:
        print(f"Demandeur {id_demandeur} envoie : {func.__name__} avec args {args}")
        # On envoie la demande au calculateur avec l'id du demandeur, la fonction et ses arguments
        queue_demandes.put((id_demandeur, func, args))

    résultats_attendus = len(fonctions_args)  # Nombre total de résultats que ce demandeur attend
    résultats_trouvés = 0                     # Compteur de résultats reçus
    tampons = []                              # Tampon pour stocker temporairement les résultats non destinés à ce demandeur

    # Tant que tous les résultats ne sont pas reçus
    while résultats_trouvés < résultats_attendus:
        res = queue_resultats.get()           # Récupère un résultat depuis la queue globale
        id_res, nom_func_res, args_res, val_res = res

        if id_res == id_demandeur:            # Si le résultat correspond à ce demandeur
            print(f"Demandeur {id_demandeur} a reçu : {nom_func_res}({args_res}) = {val_res}")
            résultats_trouvés += 1
        else:
            # Sinon, ce résultat est pour un autre demandeur, on le stocke temporairement
            tampons.append(res)

        # On remet dans la queue tous les résultats qui ne sont pas destinés à ce demandeur
        if len(tampons) > 0:
            for r in tampons:
                queue_resultats.put(r)
            tampons.clear()

# Fonction qui génère une liste de tuples (fonction, arguments) aléatoires à exécuter
def generer_fonctions_args(n):
    fonctions_args = []
    ops = [add, sub, mul, div]           # Liste des fonctions disponibles
    for _ in range(n):
        a = random.randint(1, 10)        # Génère un entier aléatoire entre 1 et 10
        b = random.randint(1, 10)
        f = random.choice(ops)            # Choisit une fonction aléatoirement parmi ops
        fonctions_args.append((f, (a, b)))  # Ajoute le couple (fonction, tuple d'arguments)
    return fonctions_args

def main():
    m = 2  # nombre de demandeurs
    n = 3  # nombre de calculateurs

    queue_demandes = Queue()    # Queue partagée pour envoyer les demandes de calcul
    queue_resultats = Queue()   # Queue partagée pour récupérer les résultats

    # Création et démarrage des processus calculateurs
    calculateurs = [Process(target=calculateur, args=(queue_demandes, queue_resultats)) for _ in range(n)]
    for p in calculateurs:
        p.start()

    # Création et démarrage des processus demandeurs
    demandeurs = []
    for i in range(m):
        fonctions_args = generer_fonctions_args(5)  # Chaque demandeur génère 5 demandes
        p = Process(target=demandeur, args=(i, queue_demandes, queue_resultats, fonctions_args))
        demandeurs.append(p)
        p.start()

    # On attend que tous les demandeurs aient terminé leur travail
    for p in demandeurs:
        p.join()

    # Envoi du signal d'arrêt "STOP" aux calculateurs
    for _ in calculateurs:
        queue_demandes.put("STOP")

    # On attend que tous les calculateurs s'arrêtent proprement
    for p in calculateurs:
        p.join()

if __name__ == "__main__":
    main()