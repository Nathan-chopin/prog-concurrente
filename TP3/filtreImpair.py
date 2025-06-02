import os

try:
    os.mkfifo("nombresImpairs")
except FileExistsError:
    pass

try:
    os.mkfifo("sommeImpairs")
except FileExistsError:
    pass

fnombres = open("nombresImpairs", "r")
fsomme = open("sommeImpairs", "w")

s = 0
while True:
    line = fnombres.readline().strip()
    if line == "-1":
        break
    s += int(line)

fnombres.close()

fsomme.write(str(s) + "\n")
fsomme.close()