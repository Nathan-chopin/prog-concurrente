import os
import sys

r1, w1 = os.pipe()
r2, w2 = os.pipe()
r3, w3 = os.pipe()

pid1 = os.fork()
if pid1 == 0:
    os.dup2(r1, 0)
    os.dup2(w2, 1)
    os.close(r1); os.close(w1)
    os.close(r2); os.close(w2)
    os.close(r3); os.close(w3)
    os.execlp("sort", "sort")
    sys.exit(1)

pid2 = os.fork()
if pid2 == 0:
    os.dup2(r2, 0)
    os.dup2(w3, 1)
    os.close(r1); os.close(w1)
    os.close(r2); os.close(w2)
    os.close(r3); os.close(w3)
    os.execlp("grep", "grep", "fichier")
    sys.exit(1)

pid3 = os.fork()
if pid3 == 0:
    os.dup2(r3, 0)
    sortie_fd = os.open("sortie", os.O_WRONLY | os.O_CREAT | os.O_TRUNC) #lecture seulement, si sortie n'existe pas, on le crée sinon on le remplace
    os.dup2(sortie_fd, 1)
    os.close(sortie_fd)
    os.close(r1); os.close(w1)
    os.close(r2); os.close(w2)
    os.close(r3); os.close(w3)
    os.execlp("tail", "tail", "-n", "5")
    sys.exit(1)

os.close(r1); os.close(r2); os.close(r3)
f = open("exercice2_1.txt", "rb")
data = f.read()
os.write(w1, data)
f.close()
os.close(w1); os.close(w2); os.close(w3)

os.wait(); os.wait(); os.wait()
sys.exit(0)
