import os

try:
    os.mkfifo("nombresPairs")
except FileExistsError:
    pass

try:
    os.mkfifo("sommePairs")
except FileExistsError:
    pass

fnombres = open("nombresPairs", "r")
fsomme = open("sommePairs", "w")

s = 0
while True:
    line = fnombres.readline().strip()
    if line == "-1":
        break
    s += int(line)

fnombres.close()

fsomme.write(str(s) + "\n")
fsomme.close()