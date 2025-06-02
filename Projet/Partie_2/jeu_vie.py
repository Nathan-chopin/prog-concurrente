# Nathan CHOPIN et le grand et beau Maël PIERRON
# main du jeu de la vie
# 2/06/25
# TODO : faire le jeu de la vie

import random as rd
import multiprocessing as mp                # Import du module multiprocessing pour la création de processus
import time                                 # Pour les temporisations


vivant = '◼️'
mort ='◻️'
N = 15
nb_vivant = 0

T = []
for _ in range(15):
    T.append([])
for i in range(15):
    for _ in range(15):
        T[i].append(mort)

def affichage():
    '''permet d'afficher le plateau'''
    ligne = ''
    for i in T:
        for k in i:
            ligne += k + ' '
        print(ligne)
        ligne = ''

def init_aleatoire():
    global nb_vivant
    for i in range(len(T)):
        for k in range(len(T)):
            if rd.randint(1,8) == 2:
                T[i][k] = vivant
                nb_vivant += 1

init_aleatoire()
affichage()

# Extrait de l’énoncé d’origine :
# • L’univers du Jeu de la Vie est une grille orthogonale bidimensionnelle infinie de cellules carrées, chacune étant dans l’un des deux états possibles : vivante ou morte.
# • Chaque cellule interagit avec ses huit voisines, qui sont adjacentes horizontalement, verticalement ou diagonalement. À chaque étape du temps, les transitions suivantes se produisent :
# ◦ Toute cellule vivante ayant moins de deux voisines vivantes meurt, comme par sous-population.
# ◦ Toute cellule vivante ayant deux ou trois voisines vivantes survit à la génération suivante.
# ◦ Toute cellule vivante ayant plus de trois voisines vivantes meurt, comme par surpopulation.
# ◦ Toute cellule morte ayant exactement trois voisines vivantes devient une cellule vivante, comme par reproduction.
# ◦ Le schéma initial constitue la graine du système. • La première génération est créée en appliquant simultanément les règles ci-dessus à chaque cellule de la graine : 
#       les naissances et les morts se produisent simultanément, et le moment précis où cela se produit est parfois appelé un tic (autrement dit, chaque génération est une pure fonction de la précédente).

# • Les règles continuent d'être appliquées de manière répétée pour créer d'autres générations.



def vie_ou_mort(N):
    n = 0
    voisin_vivant = 0
    voisin_mort = 0
    for i in range(len(T)):
        for k in range(len(T)):
            if T[i][k] == vivant and not n == N:
                n += 1
            elif T[i][k] == vivant and n == N:
                x,y = i,k
    if (x == 0 or x == 14) and (y == 0 or y == 14):
        voisin_mort += 5
    elif  (x-1 < 0 or x+1 > 14) or (y-1 < 0 or y+1 > 14):
        voisin_mort += 3

    for i in range(0,2):
        for k in range(0,2):
            if not i == k == 0:
                voisin_mort += (T[x+(i-1)][y+(k-1)] == mort)
    
    voisin_vivant = 8 - voisin_mort
    if voisin_vivant < 2 or voisin_vivant > 3:
        T[x][y] = mort





if __name__ == "__main__":
        
    mes_process = []                          # Liste des processus chevaux
    for i in range(nb_vivant):
        p = mp.Process(target=vie_ou_mort, args=(i))  # Crée le processus cheval
        p.start()                             # Lance le processus
        mes_process.append(p)                 # L’ajoute à la liste
