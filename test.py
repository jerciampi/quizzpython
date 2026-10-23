def nouveau_quiz():
    titre = input("Titre du quiz : ")
    with open(f"{titre}.txt", "w", encoding="utf-8") as new_file:    
        taille = int(input("Combien de questions comporte le quiz ? "))
        for i in range(taille):
            new_file.write("QUES\n")
            q1 = input("Question : ")
            new_file.write(f"{q1} \n")
            new_file.write("PROP \n")
            nb = int(input("Nombre de propositions : "))
            for j in range(nb):
                p = input(f"{j + 1} proposition : ")
                new_file.write(f"{p} \n")
            new_file.write("REP \n")
            r = input("La bonne réponse est : ")
            new_file.write(f"{r} \n")
    return True


nouveau_quiz()
