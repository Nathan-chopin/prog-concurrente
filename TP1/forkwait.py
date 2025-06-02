import os
import sys
import time

if len(sys.argv) != 2:
    print("Usage: python forkWait.py N")
    sys.exit(1)

try:
    N = int(sys.argv[1])
except ValueError:
    print("Veuillez entrer un entier valide.")
    sys.exit(1)

for i in range(N):
    pid = os.fork()
    if pid == 0:
        print(f"[Fils {i}] PID = {os.getpid()}, père = {os.getppid()}")
        time.sleep(2 * i)
        print(f"[Fils {i}] PID = {os.getpid()} reprend après pause.")
        sys.exit(i)

for i in range(N):
    pid, status = os.wait()
    code = os.WEXITSTATUS(status)
    print(f"[Père] Fils PID = {pid} terminé avec code de retour = {code}")
