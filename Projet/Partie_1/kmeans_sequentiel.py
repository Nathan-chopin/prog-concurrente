# Nathan CHOPIN et Maël PIERRON
# 16/06/25
# TODO : Done
import random   # Pour générer des nombres aléatoires
import math     # Pour utiliser la racine carrée et autres fonctions mathématiques
import matplotlib.pyplot as plt  # Pour tracer des graphiques

def dist(a, b):
    # Calcule la distance Euclidienne entre deux points a et b en 2D
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def moyenne(points):
    # Calcule le centre (moyenne) d'une liste de points
    n = len(points)
    if n == 0:
        return (0, 0)  # Si pas de points, retourne (0,0) pour éviter les erreurs
    x_moy = sum(p[0] for p in points) / n  # Moyenne des coordonnées x
    y_moy = sum(p[1] for p in points) / n  # Moyenne des coordonnées y
    return (x_moy, y_moy)

def k_means(Lst, k=4, epsilon=0.01, max_iter=100):
    # Fonction principale pour faire du k-means sur la liste de points Lst
    centres = random.sample(Lst, k)  # On choisit k points au hasard comme centres initiaux
    fini = False  # Flag pour savoir quand on a convergé
    iteration = 0  # Compteur d'itérations
    while not fini and iteration < max_iter:
        clusters = [[] for _ in range(k)]  # On crée k listes vides pour stocker les clusters
        for p in Lst:
            distances = [dist(p, c) for c in centres]  # Calcul des distances du point p à chaque centre
            idx_min = distances.index(min(distances))  # On trouve l'indice du centre le plus proche
            clusters[idx_min].append(p)  # On ajoute le point p au cluster correspondant
        nouveaux_centres = [moyenne(cluster) for cluster in clusters]  # Calcul des nouveaux centres des clusters
        fini = True  # On suppose qu'on a fini
        for i in range(k):
            if dist(nouveaux_centres[i], centres[i]) > epsilon:
                # Si un centre a bougé de plus que epsilon, on n'a pas encore fini
                fini = False
        centres = nouveaux_centres  # On met à jour les centres
        iteration += 1  # On passe à l'itération suivante
    return centres, clusters  # On retourne les centres finaux et la liste des clusters

def calc_sse_ssd(centres, clusters):
    # Calcule deux métriques : SSE (erreur quadratique) et SSD (distance simple)
    sse = 0
    ssd = 0
    for i, cluster in enumerate(clusters):
        for p in cluster:
            d = dist(p, centres[i])  # Distance du point p à son centre de cluster
            sse += d**2  # On ajoute le carré de la distance à SSE
            ssd += d     # On ajoute la distance simple à SSD
    return sse, ssd  # On retourne les deux valeurs

def plot_clusters(centres, clusters):
    # Affiche un scatter plot des clusters et de leurs centres
    couleurs = ['r', 'g', 'b', 'm', 'c', 'y', 'k']  # Couleurs différentes pour chaque cluster
    for i, cluster in enumerate(clusters):
        x = [p[0] for p in cluster]  # Coordonnées x des points dans le cluster i
        y = [p[1] for p in cluster]  # Coordonnées y des points dans le cluster i
        couleur = couleurs[i % len(couleurs)]  # Choix de la couleur (en boucle si plus de 7 clusters)
        plt.scatter(x, y, c=couleur, label=f'Cluster {i+1}')  # On affiche les points du cluster
        plt.scatter(centres[i][0], centres[i][1], c='k', marker='X', s=100)  # Centre du cluster en croix noire
    plt.title('K-means clustering (k=4)')  # Titre du graphique
    plt.xlabel('X')  # Label axe x
    plt.ylabel('Y')  # Label axe y
    plt.legend()     # Légende pour distinguer les clusters
    plt.grid(True)   # Affiche une grille pour mieux voir les points
    plt.show()       # Affiche la fenêtre graphique

def generer_points(n=100, x_max=100, y_max=100):
    # Génère n points aléatoires dans un rectangle [0,x_max] x [0,y_max]
    return [(random.uniform(0, x_max), random.uniform(0, y_max)) for _ in range(n)]

if __name__ == "__main__":
    Lst = generer_points(100)  # Génère 100 points aléatoires
    k = 4  # Nombre de clusters voulu
    centres, clusters = k_means(Lst, k)  # Lance l’algorithme k-means
    sse, ssd = calc_sse_ssd(centres, clusters)  # Calcule les métriques d’erreur
    print("Centres finaux :", centres)  # Affiche les centres calculés
    for i, cluster in enumerate(clusters):
        print(f"Cluster {i+1} ({len(cluster)} points)")  # Affiche la taille de chaque cluster
    print(f"SSE (Sum of Squared Errors) = {sse:.4f}")  # Affiche la somme des erreurs au carré
    print(f"SSD (Sum of Squared Distances) = {ssd:.4f}")  # Affiche la somme des distances
    plot_clusters(centres, clusters)  # Affiche le résultat avec matplotlib
