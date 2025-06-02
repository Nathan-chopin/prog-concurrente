import os

def executer_who():
    pid = os.fork()
    if pid == 0:
        os.execlp("who", "who")

def executer_ps():
    pid = os.fork()
    if pid == 0:
        os.execlp("ps", "ps")

def executer_ls():
    pid = os.fork()
    if pid == 0:
        os.execlp("ls", "ls", "-l")

pid = os.fork()
if pid == 0:
    os.execlp("who", "who")

os.waitpid(-1, 0)

pid = os.fork()
if pid == 0:
    os.execlp("ps", "ps")

os.waitpid(-1, 0)

pid = os.fork()
if pid == 0:
    os.execlp("ls", "ls", "-l")

os.waitpid(-1, 0)
