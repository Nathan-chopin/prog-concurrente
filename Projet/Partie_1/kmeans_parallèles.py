# Nathan CHOPIN et Maël PIERRON
# 16/06/25
# TODO : Done
import numpy as np  # On importe numpy pour gérer les tableaux et calculs numériques
import matplotlib.pyplot as plt  # Pour afficher les résultats graphiquement
from multiprocessing import Pool, set_start_method  # Pour faire du parallélisme avec plusieurs processus
from typing import Tuple, List  # Pour annoter les types des fonctions

def euclidean_distance(a, b):
    return np.linalg.norm(a - b)  # Calcul de la distance euclidienne entre deux points a et b

def centroid_init(X: np.ndarray, k: int) -> np.ndarray:
    centres = [X[np.random.choice(len(X))]]  # Choisit un centre initial au hasard parmi les points
    while len(centres) < k:  # Tant qu’on a pas k centres...
        # Pour chaque point x, calcule la distance la plus petite à un centre déjà choisi
        distances = np.array([min(np.array([euclidean_distance(x, c) for c in centres])) for x in X])
        next_centroid = X[np.argmax(distances)]  # Choisit le point qui est le plus éloigné de tous les centres actuels
        centres.append(next_centroid)  # Ajoute ce point comme nouveau centre
    return np.array(centres)  # Renvoie la liste des centres sous forme de tableau numpy

def assigner_points_aux_clusters(args: Tuple[np.ndarray, np.ndarray]) -> List[int]:
    X_part, centres = args  # X_part est une partie des points, centres est la liste des centres
    clusters = []  # On va stocker pour chaque point le numéro du cluster auquel il appartient
    for point in X_part:
        distances = np.array([euclidean_distance(point, c) for c in centres])  # Calcul des distances aux centres
        clusters.append(np.argmin(distances))  # Ajoute l’indice du centre le plus proche à la liste
    return clusters  # Renvoie cette liste d’assignations de cluster pour la partie

def main(X: np.ndarray, k: int, max_iter=100, epsilon=1e-4):
    set_start_method("fork")  # Sur Mac obligatoire pour multiprocessing, sinon sans effet

    centres = centroid_init(X, k)  # Initialise les centres de clusters
    for _ in range(max_iter):  # Jusqu’à max_iter itérations
        split_X = np.array_split(X, k)  # Coupe le tableau de points en k morceaux pour le parallélisme

        with Pool(processes=k) as pool:  # Crée un pool de k processus
            clusters_list = pool.map(assigner_points_aux_clusters, [(part, centres) for part in split_X])
            # Chaque processus assigne ses points à un cluster, on récupère la liste complète

        clusters = [c for sublist in clusters_list for c in sublist]  # On aplatit la liste des listes en une seule liste

        new_centres = []  # Pour stocker les nouveaux centres recalculés
        for i in range(k):  # Pour chaque cluster i
            points_in_cluster = X[np.array(clusters) == i]  # Récupère les points assignés au cluster i
            if len(points_in_cluster) > 0:
                new_centres.append(points_in_cluster.mean(axis=0))  # Calcul du centre (moyenne des points)
            else:
                new_centres.append(centres[i])  # Si aucun point dans le cluster, garde l’ancien centre
        new_centres = np.array(new_centres)  # Transforme en tableau numpy

        if np.allclose(new_centres, centres, atol=epsilon):  # Si les centres ne bougent plus beaucoup
            break  # On arrête les itérations
        centres = new_centres  # Sinon on met à jour les centres pour la prochaine itération

    return centres, clusters  # On renvoie les centres finaux et les assignations

def afficher_resultats(X: np.ndarray, centres: np.ndarray, clusters: List[int], k: int):
    couleurs = plt.cm.get_cmap("tab10", k)  # Choix d’une palette de couleurs pour les clusters
    plt.figure(figsize=(8, 6))  # Taille de la fenêtre d’affichage
    for i in range(k):  # Pour chaque cluster i
        pts = X[np.array(clusters) == i]  # Récupère les points du cluster i
        plt.scatter(pts[:, 0], pts[:, 1], s=30, color=couleurs(i), label=f"Cluster {i+1}")  # Affiche les points en couleur
        plt.scatter(centres[i, 0], centres[i, 1], s=200, c='black', marker='X')  # Affiche le centre en gros X noir
    plt.title(f"K-means parallèle avec k={k}")  # Titre du graphique
    plt.legend()  # Affiche la légende
    plt.grid(True)  # Affiche la grille
    plt.show()  # Affiche tout ça à l’écran

if __name__ == "__main__":
    np.random.seed(42)  # Fixe la graine aléatoire pour reproduire les résultats
    X = np.random.rand(200, 2) * 100  # Génère 200 points aléatoires dans un carré 100x100
    k = 4  # Nombre de clusters voulu
    centres, clusters = main(X, k)  # Lance le k-means parallèle
    afficher_resultats(X, centres, clusters, k)  # Affiche le résultat
