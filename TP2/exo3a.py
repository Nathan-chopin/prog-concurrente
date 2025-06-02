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

executer_who()
executer_ps()
executer_ls()

os.waitpid(-1, 0)
os.waitpid(-1, 0)
os.waitpid(-1, 0)
