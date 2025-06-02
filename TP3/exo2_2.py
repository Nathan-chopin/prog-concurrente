import os
import sys

dfr, dfw = os.pipe()
pid = os.fork()

if pid != 0:
    os.close(dfr)
    fichier = open("exercice2_1.txt", "rb")
    contenu = fichier.read()
    fichier.close()
    os.write(dfw, contenu)
    os.close(dfw)
    os.wait()
else:
    os.close(dfw)
    os.dup2(dfr, 0)
    os.close(dfr)
    os.execlp("wc", "wc")

sys.exit(0)