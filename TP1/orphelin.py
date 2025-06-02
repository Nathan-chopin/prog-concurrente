import os,sys,time
c = 0 
print(os.getpid())
if( os.fork() == 0 ):
    print(os.getppid())
    time.sleep(10)
    print(os.getppid())
    sys.exit(10)
sys.exit(0)