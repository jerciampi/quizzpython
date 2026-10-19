with open("fichier.txt", "r", encoding="utf-8") as fichier:
    lignes = fichier.readlines()      

contenu = []
for l in lignes:
    contenu.append(l.strip())
print(contenu)
    
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
    


print(f"les questions sont : {questions}")
print(f"les propositions sont : {propositions}")
print(f"les reponses sont : {reponses}")

"""
with open("nouveau_quiz.txt", "w", encoding="utf-8") as new:
    new.write("inshalla ça marche")
"""