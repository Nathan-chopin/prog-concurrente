import multiprocessing as mp
import ctypes
import sys
import time
import random
import signal

CLEARSCR = "\x1B[2J\x1B[;H"
CLEARELN = "\x1B[2K"
CURSOR_OFF = "\x1B[?25l"
CURSOR_ON = "\x1B[?25h"
MOVE = "\x1B[%.2d;%.2dH"
NORMAL = "\x1B[0m"

CL_WHITE="\033[01;37m"
CL_RED="\033[22;31m"
CL_GREEN="\033[22;32m"
CL_BROWN = "\033[22;33m"
CL_BLUE="\033[22;34m"
CL_MAGENTA="\033[22;35m"
CL_CYAN="\033[22;36m"
CL_YELLOW="\033[01;33m"
CL_LIGHTGREEN="\033[01;32m"

lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN, CL_BLUE, CL_MAGENTA, CL_CYAN, CL_YELLOW, CL_LIGHTGREEN]

cheval_dessin = [
    "  __//*>",
    "//___/",
    " /> />",
    "   ",
    "           ",
    "           "
]

def move_to(lig, col):
    print(MOVE % (lig, col), end='')

def erase_line():
    print(CLEARELN, end='')

def curseur_invisible():
    print(CURSOR_OFF, end='')

def curseur_visible():
    print(CURSOR_ON, end='')

def en_couleur(coul):
    print(coul, end='')

def effacer_ecran():
    print(CLEARSCR, end='')

def detourner_signal(signum, frame):
    curseur_visible()
    move_to(50,1)
    print("Interruption reçue, course arrêtée.")
    sys.exit(0)

def un_cheval(idx, keep_running, positions, lock):
    LONGUEUR_COURSE = 100
    col = 1
    nb_lignes_cheval = len(cheval_dessin)

    while col < LONGUEUR_COURSE and keep_running.value:
        with lock:
            for i in range(nb_lignes_cheval):
                move_to(idx * nb_lignes_cheval + 1 + i, 1)
                erase_line()

            for i, ligne in enumerate(cheval_dessin):
                move_to(idx * nb_lignes_cheval +2 + i, col)
                en_couleur(lyst_colors[idx % len(lyst_colors)])
                print(ligne, end='')
            print(NORMAL, end='')
            sys.stdout.flush()

        positions[idx] = col
        col += 1
        if chr(idx+65)+'*' == pari:
            time.sleep(0.5 * random.randint(1,5)/col)
        elif chr(idx+65) == pari:
            time.sleep(0.1 * random.randint(1,5))
        else:
            time.sleep(0.03 * random.randint(1,5))
    keep_running.value = False

def arbitre(positions, keep_running, lock, nb_chevaux, pari):
    nb_lignes_cheval = len(cheval_dessin)

    while keep_running.value:
        with lock:
            pos_list = list(positions[:nb_chevaux])
            max_pos = max(pos_list)
            min_pos = min(pos_list)
            leaders = [chr(ord('A')+i) for i, p in enumerate(pos_list) if p == max_pos]
            last = [chr(ord('A')+i) for i, p in enumerate(pos_list) if p == min_pos]

            base_line = nb_chevaux * nb_lignes_cheval + 2
            move_to(base_line, 0)
            erase_line()
            en_couleur(CL_YELLOW)
            print(f"Cheval en tête : {' '.join(leaders)}", end='')

            move_to(base_line+1, 0)
            erase_line()
            print(f"Cheval dernier : {' '.join(last)}", end='')
            sys.stdout.flush()
        time.sleep(0.2)

    with lock:
        pos_list = list(positions[:nb_chevaux])
        max_pos = max(pos_list)
        winners = [chr(ord('A')+i) for i, p in enumerate(pos_list) if p == max_pos]
        base_line = nb_chevaux * nb_lignes_cheval + 4
        move_to(base_line, 1)
        erase_line()
        en_couleur(CL_LIGHTGREEN)
        print(f"{winners} a gagné")
        move_to(base_line+1, 1)
        erase_line()
        if '*' in pari:
            pari = pari[0] 
        if pari in winners:
            print(f"Bravo ! Votre pari {pari} est en tête.")
        elif pari:
            print(f"Votre pari {pari} n'est pas en tête.")
        else:
            print("Aucun pari.")
        
        move_to(base_line+2, 1)
        erase_line()
        print("Fini ...")
        print(NORMAL, end='')
        curseur_visible()

if __name__ == "__main__":
    mp.set_start_method('fork')
    signal.signal(signal.SIGINT, detourner_signal)

    Nb_process = 5
    effacer_ecran()
    curseur_invisible()

    positions = mp.Array(ctypes.c_int, Nb_process)
    keep_running = mp.Value(ctypes.c_bool, True)
    lock = mp.Lock()

    move_to(1,1)
    curseur_visible()
    pari = input(f"Pariez sur un cheval (lettre A-{chr(ord('A')+Nb_process-1)}): ").upper()
    if pari < 'A' or pari > chr(ord('A')+Nb_process-1):
        pari = None
    curseur_invisible()

    mes_process = []
    for i in range(Nb_process):
        p = mp.Process(target=un_cheval, args=(i, keep_running, positions, lock))
        p.start()
        mes_process.append(p)

    arbitre_proc = mp.Process(target=arbitre, args=(positions, keep_running, lock, Nb_process, pari))
    arbitre_proc.start()

    move_to(Nb_process*len(cheval_dessin)+10, 1)
    print("Tous lancés, CTRL-C pour interrompre ...")

    for p in mes_process:
        p.join()

    keep_running.value = False
    arbitre_proc.join()
    curseur_visible()