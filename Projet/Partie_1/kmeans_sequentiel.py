import random
import math
import matplotlib.pyplot as plt

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def moyenne(points):
    n = len(points)
    if n == 0:
        return (0, 0)
    x_moy = sum(p[0] for p in points) / n
    y_moy = sum(p[1] for p in points) / n
    return (x_moy, y_moy)

def k_means(Lst, k=4, epsilon=0.01, max_iter=100):
    centres = random.sample(Lst, k)
    fini = False
    iteration = 0
    while not fini and iteration < max_iter:
        clusters = [[] for _ in range(k)]
        for p in Lst:
            distances = [dist(p, c) for c in centres]
            idx_min = distances.index(min(distances))
            clusters[idx_min].append(p)
        nouveaux_centres = [moyenne(cluster) for cluster in clusters]
        fini = True
        for i in range(k):
            if dist(nouveaux_centres[i], centres[i]) > epsilon:
                fini = False
        centres = nouveaux_centres
        iteration += 1
    return centres, clusters

def calc_sse_ssd(centres, clusters):
    sse = 0
    ssd = 0
    for i, cluster in enumerate(clusters):
        for p in cluster:
            d = dist(p, centres[i])
            sse += d**2
            ssd += d
    return sse, ssd

def plot_clusters(centres, clusters):
    couleurs = ['r', 'g', 'b', 'm', 'c', 'y', 'k']
    for i, cluster in enumerate(clusters):
        x = [p[0] for p in cluster]
        y = [p[1] for p in cluster]
        couleur = couleurs[i % len(couleurs)]
        plt.scatter(x, y, c=couleur, label=f'Cluster {i+1}')
        plt.scatter(centres[i][0], centres[i][1], c='k', marker='X', s=100)
    plt.title('K-means clustering (k=4)')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.show()

def generer_points(n=100, x_max=100, y_max=100):
    return [(random.uniform(0, x_max), random.uniform(0, y_max)) for _ in range(n)]

if __name__ == "__main__":
    Lst = generer_points(100)
    k = 4
    centres, clusters = k_means(Lst, k)
    sse, ssd = calc_sse_ssd(centres, clusters)
    print("Centres finaux :", centres)
    for i, cluster in enumerate(clusters):
        print(f"Cluster {i+1} ({len(cluster)} points)")
    print(f"SSE (Sum of Squared Errors) = {sse:.4f}")
    print(f"SSD (Sum of Squared Distances) = {ssd:.4f}")
    plot_clusters(centres, clusters)