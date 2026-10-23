def poser_quiz(nom):
    with open(f"{nom}.txt", "r", encoding="utf-8") as fichier:
        lignes = fichier.readlines()
    contenu = []
    for l in lignes:
        contenu.append(l.strip())
            
    questions = []
    propositions = []
    reponses = []

    for i in range(len(contenu)):
        if contenu[i] == "QUES":
            questions.append(contenu[i+1])
        elif contenu[i] == "REP":
                reponses.append(contenu[i+1])
        elif contenu[i] == "PROP":
            prop = []
            for j in range(i+1, len(contenu)):
                if contenu[j] != "REP":
                    prop.append(contenu[j])
                elif contenu[j] == "REP":
                    break
            propositions.append(prop)
#ici j'ai mon quiz trié
    bonnes_reponses = 0
    print("Début du quiz !")
    for i in range(len(questions)):
        if poser_question(questions[i], propositions[i], reponses[i]):
            bonnes_reponses += 1
    print(f"Score final : {bonnes_reponses} bonne(s) réponse(s) sur {len(questions)}")
    
def poser_question(quest, props, reps):
    print(quest)
    for i in props:
        print(i)
    rep = input("Votre réponse : ")
    if rep == reps:
        print("Bonne réponse !")
        return True
    else:
        print("T'es nuuuuuuul !!!")
        return False
