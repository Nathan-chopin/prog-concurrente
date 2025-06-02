import multiprocessing as mp                # Import du module multiprocessing pour la création de processus
import ctypes                               # Import pour les types C (utile pour les tableaux partagés)
import sys                                  # Module système (sortie standard, exit, etc.)
import time                                 # Pour les temporisations
import random                               # Pour les tirages aléatoires
import signal                               # Pour gérer les interruptions clavier (CTRL+C)

# Codes ANSI pour couleurs et commandes console
CLEARSCR = "\x1B[2J\x1B[;H"                 # Effacer l'écran et replacer le curseur en haut
CLEARELN = "\x1B[2K"                        # Effacer la ligne actuelle
CURSOR_OFF = "\x1B[?25l"                    # Masquer le curseur
CURSOR_ON = "\x1B[?25h"                     # Afficher le curseur
MOVE = "\x1B[%.2d;%.2dH"                    # Déplacement du curseur à une position (ligne;colonne)
NORMAL = "\x1B[0m"                          # Réinitialiser les attributs de texte

CL_WHITE="\033[01;37m"                     # Blanc vif
CL_RED="\033[22;31m"                       # Rouge
CL_GREEN="\033[22;32m"                     # Vert
CL_BROWN = "\033[22;33m"                   # Marron
CL_BLUE="\033[22;34m"                      # Bleu
CL_MAGENTA="\033[22;35m"                   # Magenta
CL_CYAN="\033[22;36m"                      # Cyan
CL_YELLOW="\033[01;33m"                    # Jaune vif
CL_LIGHTGREEN="\033[01;32m"                # Vert clair

lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_YELLOW, CL_LIGHTGREEN]  # Liste des couleurs utilisées pour les chevaux

# Le dessin du cheval, 6 lignes, simple et ascii:
cheval_dessin = [
    "_______\\/",                          # Ligne 1 du cheval
    "/- - - -_.\\",                       # Ligne 2
    "/|_____/   ",                        # Ligne 3
    "  /\\   /\\  ",                       # Ligne 4
    "           ",                        # Ligne 5 (vide)
    "           "                         # Ligne 6 (vide)
]

def move_to(lig, col):
    print(MOVE % (lig, col), end='')      # Déplace le curseur à la position (lig, col)

def erase_line():
    print(CLEARELN, end='')               # Efface la ligne courante

def curseur_invisible():
    print(CURSOR_OFF, end='')             # Masque le curseur

def curseur_visible():
    print(CURSOR_ON, end='')              # Affiche le curseur

def en_couleur(coul):
    print(coul, end='')                   # Applique une couleur au texte suivant

def effacer_ecran():
    print(CLEARSCR, end='')               # Efface l'écran

def detourner_signal(signum, frame):
    curseur_visible()                     # Réaffiche le curseur
    move_to(50,1)                         # Déplace le curseur ligne 50, colonne 1
    print("Interruption reçue, course arrêtée.")  # Message d'arrêt
    sys.exit(0)                           # Quitte proprement le programme

def un_cheval(idx, keep_running, positions, lock):
    LONGUEUR_COURSE = 50                  # Longueur totale de la course
    col = 1                               # Position de départ du cheval
    nb_lignes_cheval = len(cheval_dessin) # Nombre de lignes du dessin

    while col < LONGUEUR_COURSE and keep_running.value:  # Tant que la course n'est pas finie
        with lock:                        # Section critique (affichage + position)
            for i in range(nb_lignes_cheval):
                move_to(idx * nb_lignes_cheval + 1 + i, 1)  # Aller à l'ancienne position
                erase_line()                                # Effacer le dessin précédent

            for i, ligne in enumerate(cheval_dessin):
                move_to(idx * nb_lignes_cheval + 1 + i, col)    # Aller à la nouvelle position
                en_couleur(lyst_colors[idx % len(lyst_colors)]) # Choix couleur du cheval
                print(ligne, end='')                            # Affichage du dessin
            print(NORMAL, end='')                               # Réinitialiser la couleur
            sys.stdout.flush()                                  # Forcer l'affichage

        positions[idx] = col               # Mise à jour de la position du cheval
        col += 1                           # Le cheval avance
        time.sleep(0.05 * random.randint(1,5))  # Pause aléatoire (vitesse variable)

    keep_running.value = False            # Arrêt de la course dès qu’un cheval termine

def arbitre(positions, keep_running, lock, nb_chevaux, pari):
    nb_lignes_cheval = len(cheval_dessin)  # Nombre de lignes par cheval

    while keep_running.value:              # Boucle tant que la course continue
        with lock:                         # Accès exclusif à l'affichage
            pos_list = list(positions[:nb_chevaux])                # Liste des positions
            max_pos = max(pos_list)                                # Position la plus avancée
            min_pos = min(pos_list)                                # Position la plus faible
            leaders = [chr(ord('A')+i) for i, p in enumerate(pos_list) if p == max_pos]  # Chevaux en tête
            last = [chr(ord('A')+i) for i, p in enumerate(pos_list) if p == min_pos]     # Chevaux derniers

            base_line = nb_chevaux * nb_lignes_cheval + 2          # Ligne d'affichage de l'arbitre
            move_to(base_line, 1)
            erase_line()
            en_couleur(CL_YELLOW)
            print(f"Cheval en tête : {' '.join(leaders)}", end='') # Affiche les leaders

            move_to(base_line+1, 1)
            erase_line()
            print(f"Cheval dernier : {' '.join(last)}", end='')    # Affiche les derniers

            move_to(base_line+2, 1)
            erase_line()
            if pari and pari in leaders:
                print(f"Bravo ! Votre pari {pari} est en tête.", end='') # Pari gagnant en cours
            elif pari:
                print(f"Votre pari {pari} n'est pas en tête.", end='')   # Pari non gagnant
            else:
                print("Aucun pari.", end='')                              # Aucun pari choisi
            print(NORMAL, end='')                                         # Réinitialise couleur
            sys.stdout.flush()                                            # Rafraîchit affichage

        time.sleep(0.2)                        # Petite pause avant la prochaine vérification

    with lock:                                # Affichage final après la course
        pos_list = list(positions[:nb_chevaux])
        max_pos = max(pos_list)
        winners = [chr(ord('A')+i) for i, p in enumerate(pos_list) if p == max_pos]  # Liste des vainqueurs
        base_line = nb_chevaux * nb_lignes_cheval + 4
        effacer_ecran()
        move_to(base_line, 1)
        erase_line()
        en_couleur(CL_LIGHTGREEN)
        print(winners , 'a gagné')    # Affiche les gagnants
        move_to(base_line+1, 1)
        erase_line()
        print("Fini ...")                            # Fin de course
        print(NORMAL, end='')
        curseur_visible()                            # Réaffiche le curseur

if __name__ == "__main__":
    mp.set_start_method('fork')               # Définit le mode de création des processus (Linux/macOS)
    signal.signal(signal.SIGINT, detourner_signal)   # Gère l'interruption clavier (CTRL+C)

    Nb_process = 5                             # Nombre total de chevaux
    effacer_ecran()                            # Efface l'écran
    curseur_invisible()                        # Cache le curseur

    positions = mp.Array(ctypes.c_int, Nb_process)   # Tableau partagé pour les positions
    keep_running = mp.Value(ctypes.c_bool, True)     # Booléen partagé pour contrôle global
    lock = mp.Lock()                                 # Verrou pour section critique

    move_to(1,1)
    curseur_visible()                         # Affiche le curseur pour la saisie
    pari = input(f"Pariez sur un cheval (lettre A-{chr(ord('A')+Nb_process-1)}): ").upper()  # Demande de pari
    if pari < 'A' or pari > chr(ord('A')+Nb_process-1):
        pari = None                           # Si entrée invalide, pas de pari
    curseur_invisible()                       # Cache de nouveau le curseur

    mes_process = []                          # Liste des processus chevaux
    for i in range(Nb_process):
        p = mp.Process(target=un_cheval, args=(i, keep_running, positions, lock))  # Crée le processus cheval
        p.start()                             # Lance le processus
        mes_process.append(p)                 # L’ajoute à la liste

    arbitre_proc = mp.Process(target=arbitre, args=(positions, keep_running, lock, Nb_process, pari))  # Processus arbitre
    arbitre_proc.start()                      # Démarre l'arbitre

    move_to(Nb_process*len(cheval_dessin)+10, 1)
    print("Tous lancés, CTRL-C pour interrompre ...")  # Message utilisateur

    for p in mes_process:
        p.join()                              # Attend la fin de chaque cheval

    keep_running.value = False                # Signale la fin de la course à tous
    arbitre_proc.join()                       # Attend la fin de l'arbitre
    curseur_visible()                         # Réaffiche le curseur
