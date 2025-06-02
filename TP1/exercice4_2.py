import os

N = 5

pere_originel = os.getpid()

for i in range(N):
    if os.getpid() == pere_originel:
        pid = os.fork()
        
        if pid == 0:  # Je suis un enfant
            print(f"Je suis {os.getpid()}, mon père est {os.getppid()}")
