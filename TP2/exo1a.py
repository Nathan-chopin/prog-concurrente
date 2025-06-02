import os
import time

def traitement_1():
    for i in range(5):
        print(f"[FILS] Étape {i+1} du processus 1")
        time.sleep(1)

def traitement_2():
    for i in range(5):
        print(f"[PARENT] Étape {i+1} du processus 2")
        time.sleep(1)

pid = os.fork()

if pid == 0:
    traitement_1()
else:
    traitement_2()
    os.wait()
