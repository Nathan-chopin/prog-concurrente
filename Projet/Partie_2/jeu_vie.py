# Nathan CHOPIN et le grand et beau Maël PIERRON
# main du jeu de la vie
# 2/06/25
# TODO : faire le jeu de la vie

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
    for i in range(len(T)):
        for k in range(len(T)):
            if randint(0,50) == 1:
                T[i][k] = vivant

init_aleatoire()
affichage()