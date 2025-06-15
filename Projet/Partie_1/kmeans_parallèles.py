import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool, set_start_method
from typing import Tuple, List

def euclidean_distance(a, b):
    return np.linalg.norm(a - b)

def centroid_init(X: np.ndarray, k: int) -> np.ndarray:
    centres = [X[np.random.choice(len(X))]]
    while len(centres) < k:
        distances = np.array([min(np.array([euclidean_distance(x, c) for c in centres])) for x in X])
        next_centroid = X[np.argmax(distances)]
        centres.append(next_centroid)
    return np.array(centres)

def assigner_points_aux_clusters(args: Tuple[np.ndarray, np.ndarray]) -> List[int]:
    X_part, centres = args
    clusters = []
    for point in X_part:
        distances = np.array([euclidean_distance(point, c) for c in centres])
        clusters.append(np.argmin(distances))
    return clusters

def main(X: np.ndarray, k: int, max_iter=100, epsilon=1e-4):
    set_start_method("fork")

    centres = centroid_init(X, k)
    for _ in range(max_iter):
        split_X = np.array_split(X, k)

        with Pool(processes=k) as pool:
            clusters_list = pool.map(assigner_points_aux_clusters, [(part, centres) for part in split_X])

        clusters = [c for sublist in clusters_list for c in sublist]

        new_centres = []
        for i in range(k):
            points_in_cluster = X[np.array(clusters) == i]
            if len(points_in_cluster) > 0:
                new_centres.append(points_in_cluster.mean(axis=0))
            else:
                new_centres.append(centres[i])
        new_centres = np.array(new_centres)

        if np.allclose(new_centres, centres, atol=epsilon):
            break
        centres = new_centres

    return centres, clusters

def afficher_resultats(X: np.ndarray, centres: np.ndarray, clusters: List[int], k: int):
    couleurs = plt.cm.get_cmap("tab10", k)
    plt.figure(figsize=(8, 6))
    for i in range(k):
        pts = X[np.array(clusters) == i]
        plt.scatter(pts[:, 0], pts[:, 1], s=30, color=couleurs(i), label=f"Cluster {i+1}")
        plt.scatter(centres[i, 0], centres[i, 1], s=200, c='black', marker='X')
    plt.title(f"K-means parallèle avec k={k}")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    np.random.seed(42)
    X = np.random.rand(200, 2) * 100
    k = 4
    centres, clusters = main(X, k)
    afficher_resultats(X, centres, clusters, k)