import tkinter as tk


fenetre = tk.Tk()
fenetre.title("SQuizi")
fenetre.geometry("900x600")
fenetre.minsize(650, 450)
fenetre.configure(bg="#f7f8fc")

pages = {}
onglets = {}
page_actuelle = None
connecte = False


def afficher_page(nom_page):
    global page_actuelle
    if not connecte:
        return
    if page_actuelle == nom_page:
        return

    if page_actuelle in onglets:
        onglets[page_actuelle].configure(bg="#eeeeef", fg="#62636b")

    onglets[nom_page].configure(bg="#e2e3e7", fg="#30313a")
    pages[nom_page].tkraise()
    page_actuelle = nom_page


def se_deconnecter():
    global connecte, page_actuelle
    connecte = False
    page_actuelle = None
    bande_haut.pack_forget()
    statut_auth.set("")
    pages["Connexion"].tkraise()


bande_haut = tk.Frame(fenetre, bg="#e6e6e8", height=64)
bande_haut.pack(fill="x")
bande_haut.pack_propagate(False)

zone_logo = tk.Frame(bande_haut, bg="#e6e6e8")
zone_logo.pack(side="left", padx=(20, 24), pady=10)
logo = tk.Button(
    zone_logo,
    text="LOGO",
    command=lambda: afficher_page("Accueil"),
    bg="#d5d5d9",
    fg="#55565e",
    font=("Arial", 10, "bold"),
    width=9,
    height=2,
    relief="flat",
    borderwidth=0,
    activebackground="#c9c9ce",
    cursor="hand2",
)
logo.pack()
onglets["Accueil"] = logo

navigation = tk.Frame(bande_haut, bg="#e6e6e8")
navigation.pack(side="left", fill="y")

for nom_page in ("Quiz", "Mes activités"):
    bouton = tk.Button(
        navigation,
        text=nom_page,
        command=lambda page=nom_page: afficher_page(page),
        bg="#eeeeef",
        fg="#62636b",
        activebackground="#d5d5d9",
        activeforeground="#30313a",
        relief="flat",
        borderwidth=0,
        padx=16,
        pady=10,
        font=("Arial", 11),
        cursor="hand2",
    )
    bouton.pack(side="left", padx=4, pady=12)
    onglets[nom_page] = bouton

bouton_compte = tk.Button(
    bande_haut,
    text="Compte",
    command=lambda: afficher_page("Compte"),
    bg="#eeeeef",
    fg="#62636b",
    activebackground="#d5d5d9",
    activeforeground="#30313a",
    relief="flat",
    borderwidth=0,
    padx=18,
    pady=10,
    font=("Arial", 11),
    cursor="hand2",
)
bouton_compte.pack(side="right", padx=20, pady=12)
onglets["Compte"] = bouton_compte

contenu = tk.Frame(fenetre, bg="#f7f8fc", padx=48, pady=38)
contenu.pack(fill="both", expand=True)

for nom_page, titre, description, message in (
    (
        "Accueil",
        "Bienvenue sur SQuizi !",
        "Votre espace pour apprendre en vous amusant.",
        "Les activités seront bientôt disponibles.",
    ),
    (
        "Mes activités",
        "Mes activités",
        "Retrouvez ici votre progression et vos résultats.",
        "Vous n’avez pas encore d’activité.",
    ),
):
    page = tk.Frame(contenu, bg="#f7f8fc")
    tk.Label(
        page,
        text=titre,
        bg="#f7f8fc",
        fg="#252633",
        font=("Arial", 25, "bold"),
    ).pack(anchor="w")
    tk.Label(
        page,
        text=description,
        bg="#f7f8fc",
        fg="#686a75",
        font=("Arial", 12),
    ).pack(anchor="w", pady=(8, 28))

    carte = tk.Frame(page, bg="white", padx=24, pady=24)
    carte.pack(fill="x")
    tk.Label(
        carte,
        text=message,
        bg="white",
        fg="#686a75",
        font=("Arial", 12),
    ).pack(anchor="w")
    pages[nom_page] = page
    page.place(relx=0, rely=0, relwidth=1, relheight=1)

questions = [
    {
        "question": "Quelle est la capitale de la France ?",
        "choix": ["Lille", "Annecy", "Paris", "Dunkerque"],
        "reponse": "Paris",
    },
    {
        "question": "Combien la France a-t-elle de frontières ?",
        "choix": ["5", "8", "11", "13"],
        "reponse": "11",
    },
    {
        "question": "Combien y a-t-il de régions en France métropolitaine ?",
        "choix": ["13", "18", "22", "8"],
        "reponse": "18",
    },
    {
        "question": "Quelle est la région la plus touristique de France ?",
        "choix": [
            "Ile de France",
            "Provence Alpes Côte d’Azur",
            "Auvergne Rhône Alpes",
            "Occitanie",
        ],
        "reponse": "Ile de France",
    },
]
reponses = [None] * len(questions)
question_actuelle = 0

page_quiz = tk.Frame(contenu, bg="#f7f8fc")
pages["Quiz"] = page_quiz
page_quiz.place(relx=0, rely=0, relwidth=1, relheight=1)

tk.Label(
    page_quiz,
    text="Quiz : La France",
    bg="#f7f8fc",
    fg="#252633",
    font=("Arial", 25, "bold"),
).pack(anchor="w")
tk.Label(
    page_quiz,
    text="Répondez aux questions et découvrez votre score.",
    bg="#f7f8fc",
    fg="#686a75",
    font=("Arial", 12),
).pack(anchor="w", pady=(8, 28))

carte_quiz = tk.Frame(page_quiz, bg="white", padx=24, pady=24)
carte_quiz.pack(fill="x")
intro_quiz = tk.Frame(carte_quiz, bg="white")
tk.Label(
    intro_quiz,
    text=f"{len(questions)} questions",
    bg="white",
    fg="#252633",
    font=("Arial", 18, "bold"),
).pack(anchor="w")
tk.Label(
    intro_quiz,
    text="Prenez le temps de choisir une réponse à chaque question.",
    bg="white",
    fg="#686a75",
    font=("Arial", 11),
).pack(anchor="w", pady=(8, 18))

zone_questions = tk.Frame(carte_quiz, bg="white")
progression = tk.StringVar()
tk.Label(
    zone_questions,
    textvariable=progression,
    bg="white",
    fg="#5356f6",
    font=("Arial", 10, "bold"),
).pack(anchor="w")
libelle_question = tk.Label(
    zone_questions,
    bg="white",
    fg="#252633",
    font=("Arial", 17, "bold"),
    wraplength=720,
    justify="left",
)
libelle_question.pack(anchor="w", pady=(14, 18))
choix_selectionne = tk.StringVar()
zone_choix = tk.Frame(zone_questions, bg="white")
zone_choix.pack(fill="x")
statut_quiz = tk.StringVar()
tk.Label(
    zone_questions,
    textvariable=statut_quiz,
    bg="white",
    fg="#b33b3b",
    font=("Arial", 10),
).pack(anchor="w", pady=(10, 0))
navigation_quiz = tk.Frame(zone_questions, bg="white")
navigation_quiz.pack(fill="x", pady=(18, 0))

resultat_quiz = tk.Frame(carte_quiz, bg="white")
score_final = tk.StringVar()
tk.Label(
    resultat_quiz,
    textvariable=score_final,
    bg="white",
    fg="#252633",
    font=("Arial", 21, "bold"),
).pack(anchor="w")
message_resultat = tk.StringVar()
tk.Label(
    resultat_quiz,
    textvariable=message_resultat,
    bg="white",
    fg="#686a75",
    font=("Arial", 12),
).pack(anchor="w", pady=(8, 18))


def actualiser_selection_choix():
    for bouton in zone_choix.winfo_children():
        selectionne = bouton.cget("text") == choix_selectionne.get()
        bouton.configure(
            bg="#e7e8ff" if selectionne else "#f7f8fc",
            fg="#3031a5" if selectionne else "#454650",
            activebackground="#dfe0ff" if selectionne else "#eeeeef",
            font=("Arial", 12, "bold" if selectionne else "normal"),
        )


def selectionner_reponse(reponse):
    choix_selectionne.set(reponse)
    actualiser_selection_choix()


def afficher_question():
    question = questions[question_actuelle]
    progression.set(f"Question {question_actuelle + 1} sur {len(questions)}")
    libelle_question.configure(text=question["question"])
    bouton_suivant.configure(
        text="Terminer" if question_actuelle == len(questions) - 1 else "Suivant"
    )
    choix_selectionne.set(reponses[question_actuelle] or "")
    statut_quiz.set("")
    for widget in zone_choix.winfo_children():
        widget.destroy()
    for choix in question["choix"]:
        tk.Button(
            zone_choix,
            text=choix,
            command=lambda reponse=choix: selectionner_reponse(reponse),
            bg="#f7f8fc",
            fg="#454650",
            activebackground="#eeeeef",
            relief="flat",
            borderwidth=0,
            font=("Arial", 12),
            anchor="w",
            padx=14,
            pady=12,
            cursor="hand2",
        ).pack(fill="x", anchor="w", pady=4)
    actualiser_selection_choix()


def commencer_quiz():
    global question_actuelle
    question_actuelle = 0
    reponses[:] = [None] * len(questions)
    intro_quiz.pack_forget()
    resultat_quiz.pack_forget()
    zone_questions.pack(fill="x")
    afficher_question()


def terminer_quiz():
    score = sum(
        reponse == question["reponse"]
        for reponse, question in zip(reponses, questions)
    )
    score_final.set(f"Votre score : {score} / {len(questions)}")
    message_resultat.set(
        "Excellent travail !" if score == len(questions)
        else "Vous pouvez recommencer pour améliorer votre score."
    )
    zone_questions.pack_forget()
    resultat_quiz.pack(fill="x")


def question_suivante():
    global question_actuelle
    reponse = choix_selectionne.get()
    if not reponse:
        statut_quiz.set("Sélectionnez une réponse pour continuer.")
        return
    reponses[question_actuelle] = reponse
    if question_actuelle == len(questions) - 1:
        terminer_quiz()
        return
    question_actuelle += 1
    afficher_question()


def question_precedente():
    global question_actuelle
    if question_actuelle > 0:
        reponses[question_actuelle] = choix_selectionne.get() or None
        question_actuelle -= 1
        afficher_question()


bouton_precedent = tk.Button(
    navigation_quiz,
    text="Précédent",
    command=question_precedente,
    bg="#eeeeef",
    fg="#454650",
    relief="flat",
    padx=16,
    pady=9,
    font=("Arial", 10),
    cursor="hand2",
)
bouton_precedent.pack(side="left")
bouton_suivant = tk.Button(
    navigation_quiz,
    text="Suivant",
    command=question_suivante,
    bg="#5356f6",
    fg="white",
    activebackground="#4245df",
    relief="flat",
    padx=18,
    pady=9,
    font=("Arial", 10, "bold"),
    cursor="hand2",
)
bouton_suivant.pack(side="right")
tk.Button(
    resultat_quiz,
    text="Recommencer",
    command=commencer_quiz,
    bg="#5356f6",
    fg="white",
    activebackground="#4245df",
    relief="flat",
    padx=18,
    pady=9,
    font=("Arial", 10, "bold"),
    cursor="hand2",
).pack(anchor="w")
tk.Button(
    intro_quiz,
    text="Commencer le quiz",
    command=commencer_quiz,
    bg="#5356f6",
    fg="white",
    activebackground="#4245df",
    relief="flat",
    padx=18,
    pady=10,
    font=("Arial", 11, "bold"),
    cursor="hand2",
).pack(anchor="w")
intro_quiz.pack(fill="x")

for widget in page_quiz.winfo_children():
    widget.destroy()

page_connexion = tk.Frame(contenu, bg="#f7f8fc")
page_connexion.place(relx=0, rely=0, relwidth=1, relheight=1)
pages["Connexion"] = page_connexion

page_compte = tk.Frame(contenu, bg="#f7f8fc")
page_compte.place(relx=0, rely=0, relwidth=1, relheight=1)
pages["Compte"] = page_compte

tk.Label(
    page_compte,
    text="Mon compte",
    bg="#f7f8fc",
    fg="#252633",
    font=("Arial", 25, "bold"),
).pack(anchor="w")
identite_compte = tk.StringVar()
tk.Label(
    page_compte,
    textvariable=identite_compte,
    bg="#f7f8fc",
    fg="#686a75",
    font=("Arial", 12),
).pack(anchor="w", pady=(12, 0))
tk.Button(
    page_compte,
    text="Se déconnecter",
    command=se_deconnecter,
    bg="#eeeeef",
    fg="#454650",
    relief="flat",
    padx=16,
    pady=9,
    font=("Arial", 10),
    cursor="hand2",
).pack(anchor="w", pady=(20, 0))

tk.Label(
    page_connexion,
    text="Bienvenue sur SQuizi !",
    bg="#f7f8fc",
    fg="#252633",
    font=("Arial", 25, "bold"),
).pack(anchor="w")
tk.Label(
    page_connexion,
    text="Connectez-vous ou créez un compte pour accéder à SQuizi.",
    bg="#f7f8fc",
    fg="#686a75",
    font=("Arial", 12),
).pack(anchor="w", pady=(8, 24))

carte_connexion = tk.Frame(page_connexion, bg="white", padx=28, pady=24)
carte_connexion.pack(fill="x")

mode_connexion = tk.StringVar(value="Connexion")
nom_utilisateur = tk.StringVar()
adresse_email = tk.StringVar()
mot_de_passe = tk.StringVar()
statut_auth = tk.StringVar()

tk.Label(
    carte_connexion,
    textvariable=mode_connexion,
    bg="white",
    fg="#252633",
    font=("Arial", 18, "bold"),
).pack(anchor="w", pady=(0, 18))

champ_nom = tk.Frame(carte_connexion, bg="white")
tk.Label(champ_nom, text="Nom", bg="white", fg="#454650", font=("Arial", 11)).pack(
    anchor="w", pady=(0, 6)
)
tk.Entry(champ_nom, textvariable=nom_utilisateur, font=("Arial", 12)).pack(
    fill="x", ipady=6
)

tk.Label(
    carte_connexion, text="Adresse e-mail", bg="white", fg="#454650", font=("Arial", 11)
).pack(anchor="w", pady=(12, 6))
tk.Entry(carte_connexion, textvariable=adresse_email, font=("Arial", 12)).pack(
    fill="x", ipady=6
)

tk.Label(
    carte_connexion, text="Mot de passe", bg="white", fg="#454650", font=("Arial", 11)
).pack(anchor="w", pady=(12, 6))
tk.Entry(
    carte_connexion, textvariable=mot_de_passe, show="*", font=("Arial", 12)
).pack(fill="x", ipady=6)

bouton_action = tk.Button(
    carte_connexion,
    bg="#5356f6",
    fg="white",
    activebackground="#4245df",
    activeforeground="white",
    relief="flat",
    borderwidth=0,
    padx=18,
    pady=10,
    font=("Arial", 11, "bold"),
    cursor="hand2",
)
bouton_action.pack(anchor="w", pady=(20, 12))

statut_label = tk.Label(
    carte_connexion,
    textvariable=statut_auth,
    bg="white",
    fg="#686a75",
    font=("Arial", 10),
    wraplength=650,
)
statut_label.pack(anchor="w")

bouton_changer_mode = tk.Button(
    carte_connexion,
    bg="white",
    fg="#5356f6",
    activebackground="white",
    activeforeground="#4245df",
    relief="flat",
    borderwidth=0,
    font=("Arial", 10),
    cursor="hand2",
)
bouton_changer_mode.pack(anchor="w", pady=(12, 0))


def changer_mode_auth():
    nouveau_mode = "Créer un compte" if mode_connexion.get() == "Connexion" else "Connexion"
    mode_connexion.set(nouveau_mode)
    statut_auth.set("")
    if nouveau_mode == "Créer un compte":
        champ_nom.pack(fill="x", before=carte_connexion.winfo_children()[1])
        bouton_action.configure(text="Créer mon compte")
        bouton_changer_mode.configure(text="Déjà un compte ? Se connecter")
    else:
        champ_nom.pack_forget()
        bouton_action.configure(text="Se connecter")
        bouton_changer_mode.configure(text="Pas encore de compte ? Créer un compte")


def envoyer_formulaire_auth():
    global connecte, page_actuelle
    champs_requis = [adresse_email.get().strip(), mot_de_passe.get()]
    if mode_connexion.get() == "Créer un compte":
        champs_requis.append(nom_utilisateur.get().strip())
    if not all(champs_requis):
        statut_auth.set("Merci de remplir tous les champs.")
        return
    identite = nom_utilisateur.get().strip() or adresse_email.get().strip()
    identite_compte.set(
        f"{identite} — {adresse_email.get().strip()}\n"
        "Session provisoire : les identifiants ne sont pas enregistrés."
    )
    connecte = True
    bande_haut.pack(fill="x", before=contenu)
    page_actuelle = None
    afficher_page("Accueil")


bouton_action.configure(
    text="Se connecter",
    command=envoyer_formulaire_auth,
)
bouton_changer_mode.configure(
    text="Pas encore de compte ? Créer un compte",
    command=changer_mode_auth,
)

bande_haut.pack_forget()
pages["Connexion"].tkraise()
fenetre.mainloop()
