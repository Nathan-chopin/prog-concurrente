# Nathan CHOPIN et Maël PIERRON
# main du jeu de la vie
# 16/06/25

import multiprocessing as mp
from random import randint
import time

vivant = '◼️'
mort = '◻️'
N = 15

def creation_tableau_bis(N):
    manager = mp.Manager()
    T = manager.list()
    for i in range(N):
        T.append(manager.list())
        for _ in range(N):
            T[i].append(mort)
    return T

def affichage(T):
    print("\033[H\033[J", end='')
    ligne = ''
    for i in T:
        for k in i:
            ligne += k + ' '
        print(ligne)
        ligne = ''
    print('\n')

def init_aleatoire(T):
    for i in range(len(T)):
        for k in range(len(T)):
            if randint(0,8) == 1:
                T[i][k] = vivant

def vie_mort(lock, x, y, T_source, T_dest):
    voisins = [(-1, -1), (-1, 0), (-1, 1),
               (0, -1),          (0, 1),
               (1, -1), (1, 0),  (1, 1)]
    nb_vivant = 0
    for dx, dy in voisins:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(T_source) and 0 <= ny < len(T_source):
            if T_source[nx][ny] == vivant:
                nb_vivant += 1

    etat = T_source[x][y]
    with lock:
        if etat == vivant:
            if nb_vivant < 2 or nb_vivant > 3:
                T_dest[x][y] = mort
            else:
                T_dest[x][y] = vivant
        else:
            if nb_vivant == 3:
                T_dest[x][y] = vivant
            else:
                T_dest[x][y] = mort

def crea_proc(T_source):
    T_dest = creation_tableau_bis(N)
    mes_process = []
    lock = mp.Lock()
    for x in range(N):
        for y in range(N):
            p = mp.Process(target=vie_mort, args=(lock, x, y, T_source, T_dest))
            p.start()
            mes_process.append(p)
    for p in mes_process:
        p.join()
    return T_dest

if __name__ == '__main__':
    T = creation_tableau_bis(N)
    init_aleatoire(T)
    affichage(T)

    while True:
        time.sleep(0.5)
        T = crea_proc(T)
        affichage(T)
