import sys

mots = sys.argv[1:]

mots_inversés = []
for mot in mots:
    mots_inversés.append(mot[::-1])

résultat = " ".join(mots_inversés)
print(résultat)