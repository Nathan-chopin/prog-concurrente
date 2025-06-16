from multiprocessing import Process, Queue
from random import randint
from time import sleep
import os
import sys

def effacer_ecran():
    print("\033[2J\033[H", end='')

def barre(valeur, minimum, maximum, longueur=30):
    val = max(min(valeur, maximum), minimum)
    ratio = (val - minimum) / (maximum - minimum)
    nb_blocs = int(ratio * longueur)
    return "█" * nb_blocs + "-" * (longueur - nb_blocs)

def capteur_temperature(file_temp):
    while True:
        temp = randint(15, 30)
        file_temp.put(temp)
        sleep(1)

def capteur_pression(file_pression):
    while True:
        pression = randint(900, 1100)
        file_pression.put(pression)
        sleep(1)

def controleur(file_temp, file_pression):
    while True:
        temp = file_temp.get()
        pression = file_pression.get()

        effacer_ecran()

        temp_bar = barre(temp, 15, 30)
        pression_bar = barre(pression, 900, 1100)

        temp_color = "\033[32m" if 18 <= temp <= 28 else "\033[31m"
        pression_color = "\033[34m" if 950 <= pression <= 1050 else "\033[31m"

        print(f"\033[1m🧪 CONTROLEUR TEMPERATURE / PRESSION\033[0m\n")
        print(f"🌡️  Température : {temp_color}{temp} °C\033[0m  [{temp_bar}]")
        print(f"📈 Pression    : {pression_color}{pression} hPa\033[0m  [{pression_bar}]")

        if temp < 18 or temp > 28:
            print("\n\033[41;97m⚠️  ALERTE TEMPÉRATURE ANORMALE !\033[0m")
        if pression < 950 or pression > 1050:
            print("\033[41;97m⚠️  ALERTE PRESSION ANORMALE !\033[0m")

        sys.stdout.flush()
        sleep(0.5)

if __name__ == "__main__":
    file_temp = Queue()
    file_pression = Queue()

    p1 = Process(target=capteur_temperature, args=(file_temp,))
    p2 = Process(target=capteur_pression, args=(file_pression,))
    p3 = Process(target=controleur, args=(file_temp, file_pression))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()