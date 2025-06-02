import os
import sys

message = b"Bonjour fils\n"
dfr, dfw = os.pipe()
pid = os.fork()

if pid != 0:
    os.close(dfr)
    os.write(dfw, message)
    print("Père : message envoyé")
    os.close(dfw)
else:
    os.close(dfw)
    msg_recu = os.read(dfr, 100)
    print("Fils : message reçu =", msg_recu.decode())
    os.close(dfr)

sys.exit(0)