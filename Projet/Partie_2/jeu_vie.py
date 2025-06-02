# Nathan CHOPIN
# main du jeu de la vie
# 2/06/25
# TODO : tout

from random import randint

vivant = '◼️'
mort ='◻️'
N = 15
T = [[ '◻️' ] * N]*N

def affichage():
    '''permet d'afficher le plateau'''
    ligne = ''
    for i in T:
        for k in i:
            ligne += k + ' '
        print(ligne)
        ligne = ''

def init_aleatoire():
    return