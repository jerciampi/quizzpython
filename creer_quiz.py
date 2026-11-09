def creer_fichier(titre):
    with open(f"Quiz/{titre}.txt", "w", encoding="utf-8"):
        return True 

def ajout_question(titre, question, liste_rep, rep):
    with open(f"Quiz/{titre}.txt", "w", encoding="utf-8") as new_file:
        new_file.write("QUES\n")
        new_file.write(f"{question} \n")
        new_file.write("PROP \n")
        for elt in liste_rep:
            new_file.write(f"{elt}\n")
        new_file.write("REP \n")
        new_file.write(f"{rep} \n")
        return True
