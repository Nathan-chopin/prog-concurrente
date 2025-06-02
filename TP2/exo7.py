import os,sys

# 4**N bonjour
N = 4
for i in range(N) :
    os.fork()
    os.fork()
print("Bonjour")
sys.exit(0)