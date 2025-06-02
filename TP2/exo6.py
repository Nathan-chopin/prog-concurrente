import os, time, random, sys 

for i in range(4) : 
    
    if os.fork() != 0 : 
        break 

random.seed() 
delai = random.randint(0,4) 
time.sleep(delai) 


#Question 3 : Affichage dans l'odre inverse de l'alphabet
try:
    os.wait()
    print("Mon nom est " + chr(ord('A')+i) + " j ai dormi " + str(delai) + " secondes") 
except:
    print("Mon nom est " + chr(ord('A')+i) + " j ai dormi " + str(delai) + " secondes") 

sys.exit(0) 

#Question 2 : Le programme affiche les lettres dans un ordre aléatoire
