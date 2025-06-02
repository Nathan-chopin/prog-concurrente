import os

N = 5

for i in range(N):
    pid = os.fork()
    
    if pid == 0: # Je suis un enfant
        print(f"Je suis {os.getpid()}, mon père est {os.getppid()}")
    else:
        os.wait()
        break