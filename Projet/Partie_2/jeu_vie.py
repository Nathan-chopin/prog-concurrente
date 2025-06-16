# Nathan CHOPIN et le grand et beau Maël PIERRON
# main du jeu de la vie
# 2/06/25
# TODO : faire le jeu de la vie

import multiprocessing as mp
from random import randint
import keyboard as kb

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
    '''permet d'afficher le plateau'''
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
    bord_x0  = x == 0
    bord_x14 = x == len(T)
    bord_y0  = y == 0
    bord_y14 = y == len(T)

    nb_mort =  3 * bord_x0  + (3 * bord_y0 - int(bord_y0 and bord_x0 )) + (3 * bord_y14 - int(bord_y14 and bord_x0 ))
    nb_mort += 3 * bord_x14 + (3 * bord_y0 - int(bord_y0 and bord_x14)) + (3 * bord_y14 - int(bord_y14 and bord_x14))
    
    for i in [int(not bord_y0),-1 * int(not bord_y14)]:
        if i != 0:
            if not bord_x0:
                nb_mort += int(T[x-1][y+i] == mort)
            if not bord_x14:
                nb_mort += int(T[x+1][y+i] == mort)
            nb_mort += int(T[x][y+i] == mort)
    
    nb_vivant = 8 - nb_mort
    if etat == mort and nb_vivant == 3:
        with lock:
            T[x][y] = vivant
        

def action_clavier(event):
    if event.name == 'b':
        print('caca')

if __name__ == '__main__' :
    lock = mp.Lock()
    init_aleatoire()
    affichage()
    
    mes_process = []                          # Liste des processus chevaux
    for x in range(N):
        for y in range(N):
            p = mp.Process(target=vie_mort, args=(lock,x,y,T[x][y]))  # Crée le processus cheval
            p.start()                             # Lance le processus
            mes_process.append(p)

    kb.on_press(action_clavier)
    
    for p in mes_process:
        p.join()
    kb.unhook_all()
