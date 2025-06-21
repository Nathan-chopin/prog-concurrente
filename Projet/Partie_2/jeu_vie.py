# Nathan CHOPIN et Maël PIERRON
# main du jeu de la vie
# 16/06/25
# TODO : faire le jeu de la vie

import multiprocessing as mp
from random import randint
import time

vivant = '◼️'
mort ='◻️'
N = 15

def creation_tableau(N):
    T = []
    for i in range(N):
        T.append([])
        for _ in range(N):
            T[i].append(mort)
    return T

T = creation_tableau(N)

def affichage():
    '''permet d'afficher le plateau '''
    ligne = ''
    for i in T:
        for k in i:
            ligne += k + ' '
        print(ligne)
        ligne = ''

def init_aleatoire():
    for i in range(len(T)):
        for k in range(len(T)):
            if randint(0,8) == 1:
                T[i][k] = vivant

def vie_mort(lock,x,y,etat):
    '''détermine la vie ou la mort d'une cellule'''
    bord_x0  = x == 0
    bord_x14 = x == len(T) - 1
    bord_y0  = y == 0
    bord_y14 = y == len(T) - 1

    # compte le nombre de cellules mortes aux bords x et y
    nb_mort =  3 * int(bord_x0)  + (3 * int(bord_y0) - int(bord_y0 and bord_x0 )) + (3 * int(bord_y14) - int(bord_y14 and bord_x0 ))
    nb_mort += 3 * int(bord_x14) + (3 * int(bord_y0) - int(bord_y0 and bord_x14)) + (3 * int(bord_y14) - int(bord_y14 and bord_x14))

    def est_mort(etat):
        '''la cellule est morte ?'''
        if etat == mort:
            return 1
        else:
            return 0

    # compte le nombre de cellules mortes quand on n'est pas aux bords
    for i in [int( not bord_y14 ),-1 * int( not bord_y0 )]:
        if i != 0:
            if not bord_x0:
                nb_mort += est_mort(T[x-1][y+i])
            if not bord_x14:
                nb_mort += est_mort(T[x+1][y+i])
            nb_mort += est_mort(T[x][y+i])
    
    nb_vivant = 8 - nb_mort
    if etat == mort and nb_vivant == 3:
        with lock:
            T[x][y] = vivant
    
    if etat == vivant and (nb_vivant < 2 or nb_vivant > 3):
        with lock:
            T[x][y] = mort

def crea_proc():
    mes_process = []                          # Liste des processus chevaux
    for x in range(N):
        for y in range(N):
            p = mp.Process(target=vie_mort, args=(lock,x,y,T[x][y]))  # Crée le processus
            p.start()                             # Lance le processus
            mes_process.append(p)
    for p in mes_process:
        p.join()

if __name__ == '__main__' :
    lock = mp.Lock()
    init_aleatoire()
    affichage()
    
    while True:
        time.sleep(3)
        crea_proc()
        affichage()