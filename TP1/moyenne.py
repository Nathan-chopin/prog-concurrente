import sys

def calculer_moyenne():
    notes_str = sys.argv[1:]
    
    if len(notes_str) == 0:
        print("Aucune moyenne à calculer")
        return
    
    notes = []
    for note_str in notes_str:
        try:
            note = int(note_str)
            if note < 0 or note > 20:
                print("Note(s) non valide(s)")
                return
            notes.append(note)
        except ValueError:
            print("Note(s) non valide(s)")
            return
    
    moyenne = sum(notes) / len(notes)
    print("Moyenne = %.2f" % moyenne)

calculer_moyenne()