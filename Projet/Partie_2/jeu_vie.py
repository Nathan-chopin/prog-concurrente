# Nathan CHOPIN et le grand et beau Maël PIERRON
# main du jeu de la vie
# 2/06/25
# TODO : faire le jeu de la vie

import multiprocessing as mp
from random import randint

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
            if randint(0,10) == 1:
                T[i][k] = vivant

def vie_mort():
    return

if __name__ == '__main__' :
    
    init_aleatoire()
    affichage()
    
    mes_process = []                          # Liste des processus chevaux
    for i in range(N**2):
        p = mp.Process(target=vie_mort, args=())  # Crée le processus cheval
        p.start()                             # Lance le processus
        mes_process.append(p)

    
    for p in mes_process:
        p.join()

