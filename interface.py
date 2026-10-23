# Importation de la bibliothèque Tkinter pour créer l'interface graphique
import tkinter as tk
from PIL import Image, ImageTk
from database_quiz import verifier_connexion,enregistrer_partie,creer_compte


# ============================================================
# 1. INITIALISATION DE LA FENÊTRE PRINCIPALE
# ============================================================

# Création de la fenêtre principale de l'application
fenetre = tk.Tk()

# Définition du titre de la fenêtre
fenetre.title("SQuizi")

# Définition de la taille initiale de la fenêtre
fenetre.geometry("900x600")

# Définition de la taille minimale de la fenêtre
fenetre.minsize(650, 450)

# Définition de la couleur de fond générale
fenetre.configure(bg="#f7f8fc")


# Dictionnaire qui associe chaque nom de page à son objet Frame
pages = {}

# Dictionnaire qui associe chaque page à son bouton de navigation
onglets = {}

# Mémorise le nom de la page actuellement affichée
page_actuelle = None

# Indique si un utilisateur est connecté
connecte = False


# ============================================================
# 2. GESTION DE LA NAVIGATION ENTRE LES PAGES
# ============================================================

def afficher_page(nom_page):
    # Permet de modifier la variable globale page_actuelle
    global page_actuelle

    # Empêche l'accès aux pages si l'utilisateur n'est pas connecté
    if not connecte:
        return

    # Évite de réafficher une page déjà ouverte
    if page_actuelle == nom_page:
        return

    # Réinitialise l'apparence du bouton de l'ancienne page
    if page_actuelle in onglets:
        onglets[page_actuelle].configure(
            bg="#eeeeef",
            fg="#62636b"
        )

    # Met en évidence le bouton correspondant à la nouvelle page
    onglets[nom_page].configure(
        bg="#e2e3e7",
        fg="#30313a"
    )

    # Place la page demandée au premier plan
    pages[nom_page].tkraise()

    # Mémorise la page actuellement affichée
    page_actuelle = nom_page


def se_deconnecter():
    # Permet de modifier les variables globales
    global connecte, page_actuelle

    # Indique que l'utilisateur n'est plus connecté
    connecte = False

    # Réinitialise la page actuelle
    page_actuelle = None

    # Masque la barre de navigation supérieure
    bande_haut.pack_forget()

    # Efface le message lié à l'authentification
    statut_auth.set("")

    # Affiche la page de connexion
    pages["Connexion"].tkraise()


# ============================================================
# 3. CRÉATION DE LA BARRE DE NAVIGATION
# ============================================================

# Création de la barre supérieure de l'application
bande_haut = tk.Frame(
    fenetre,
    bg="#e6e6e8",
    height=64
)

# Affiche la barre sur toute la largeur de la fenêtre
bande_haut.pack(fill="x")

# Empêche la hauteur du Frame de changer selon son contenu
bande_haut.pack_propagate(False)


# -------------------------
# Zone du logo
# -------------------------

# Création de la zone contenant le logo
zone_logo = tk.Frame(
    bande_haut,
    bg="#e6e6e8"
)

# Positionnement de la zone du logo à gauche
zone_logo.pack(
    side="left",
    padx=(20, 24),
    pady=10
)

# Création du bouton servant de logo
# Un clic permet de revenir à la page d'accueil

logo = tk.Button(
    zone_logo,
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

# Affichage du bouton logo
logo.pack()

# Association du bouton à la page d'accueil
onglets["Accueil"] = logo


# -------------------------
# Boutons de navigation
# -------------------------

# Création de la zone contenant les boutons de navigation
navigation = tk.Frame(
    bande_haut,
    bg="#e6e6e8"
)

# Positionnement de la navigation à gauche
navigation.pack(side="left", fill="y")

# Création des boutons Quiz et Mes activités
for nom_page in ("Quiz", "Mes activités"):

    # Création d'un bouton pour chaque page
    bouton = tk.Button(
        navigation,
        text=nom_page,

        # La valeur par défaut page=nom_page permet à chaque
        # bouton d'ouvrir la bonne page lors du clic
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

    # Positionnement horizontal du bouton
    bouton.pack(side="left", padx=4, pady=12)

    # Enregistrement du bouton dans le dictionnaire
    onglets[nom_page] = bouton


# -------------------------
# Bouton Compte
# -------------------------

# Création du bouton permettant d'ouvrir la page du compte
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

# Positionnement du bouton à droite de la barre
bouton_compte.pack(side="right", padx=20, pady=12)

# Enregistrement du bouton dans le dictionnaire
onglets["Compte"] = bouton_compte


# ============================================================
# 4. ZONE PRINCIPALE DE CONTENU
# ============================================================

# Frame contenant toutes les pages de l'application
contenu = tk.Frame(
    fenetre,
    bg="#f7f8fc",
    padx=48,
    pady=38
)

# La zone de contenu occupe tout l'espace disponible
contenu.pack(fill="both", expand=True)


# ============================================================
# 5. CRÉATION DES PAGES ACCUEIL ET MES ACTIVITÉS
# ============================================================

# Chaque élément contient :
# - le nom interne de la page
# - le titre affiché
# - une description
# - un message dans la carte centrale
# Variable dynamique pour personnaliser le titre de la page d'accueil
titre_accueil = tk.StringVar(value="Bienvenue sur SQuizi !")

for nom_page, titre, description, message in (
    (
        "Accueil",
        "Bienvenue sur SQuizi !",
        "Votre espace pour apprendre en vous amusant.",
        "Est-ce que c'est bon pour vous ?",
    ),
    (
        "Mes activités",
        "Mes activités",
        "Retrouvez ici votre progression et vos résultats.",
        "Vous n’avez pas encore d’activité.",
    ),
):

    # Création du conteneur de la page
    page = tk.Frame(
        contenu,
        bg="#f7f8fc"
    )

    # Affichage du titre de la page
    # Le titre de l'accueil est dynamique et pourra afficher l'identifiant saisi
    if nom_page == "Accueil":
        tk.Label(
            page,
            textvariable=titre_accueil,
            bg="#f7f8fc",
            fg="#252633",
            font=("Arial", 25, "bold"),
        ).pack(anchor="w")
    else:
        tk.Label(
            page,
            text=titre,
            bg="#f7f8fc",
            fg="#252633",
            font=("Arial", 25, "bold"),
        ).pack(anchor="w")

    # Affichage de la description sous le titre
    tk.Label(
        page,
        text=description,
        bg="#f7f8fc",
        fg="#686a75",
        font=("Arial", 12),
    ).pack(anchor="w", pady=(8, 28))

    # Création d'une carte blanche contenant le message
    carte = tk.Frame(
        page,
        bg="white",
        padx=24,
        pady=24
    )

    # Affichage de la carte sur toute la largeur disponible
    carte.pack(fill="x")

    # Affichage du message de la carte
    tk.Label(
        carte,
        text=message,
        bg="white",
        fg="#686a75",
        font=("Arial", 12),
    ).pack(anchor="w")

    # Enregistrement de la page dans le dictionnaire
    pages[nom_page] = page

    # Superposition de la page avec les autres pages
    # relwidth et relheight lui donnent toute la zone de contenu
    page.place(
        relx=0,
        rely=0,
        relwidth=1,
        relheight=1
    )


# ============================================================
# 6. DONNÉES DU QUIZ
# ============================================================

# Liste contenant toutes les questions du quiz
# Chaque question est représentée par un dictionnaire avec :
# - question : le texte de la question
# - choix : la liste des réponses possibles
# - reponse : la bonne réponse

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

# Liste qui mémorise les réponses de l'utilisateur
# Chaque position correspond à une question
# None signifie que la question n'a pas encore de réponse enregistrée
reponses = [None] * len(questions)

# Indice de la question actuellement affichée
# La première question possède l'indice 0
question_actuelle = 0


# ============================================================
# 7. CRÉATION DE LA PAGE DU QUIZ
# ============================================================

# Création du conteneur principal de la page Quiz
page_quiz = tk.Frame(
    contenu,
    bg="#f7f8fc"
)

# Enregistrement de la page dans le dictionnaire
pages["Quiz"] = page_quiz

# Positionnement de la page dans la zone de contenu
page_quiz.place(
    relx=0,
    rely=0,
    relwidth=1,
    relheight=1
)

# Affichage du titre du quiz
tk.Label(
    page_quiz,
    text="Quiz : La France",
    bg="#f7f8fc",
    fg="#252633",
    font=("Arial", 25, "bold"),
).pack(anchor="w")

# Affichage de la description du quiz
tk.Label(
    page_quiz,
    text="Répondez aux questions et découvrez votre score.",
    bg="#f7f8fc",
    fg="#686a75",
    font=("Arial", 12),
).pack(anchor="w", pady=(8, 28))


# -------------------------
# Carte principale du quiz
# -------------------------

# Création de la carte blanche qui contient le quiz
carte_quiz = tk.Frame(
    page_quiz,
    bg="white",
    padx=24,
    pady=24
)

carte_quiz.pack(fill="x")


# -------------------------
# Écran d'introduction
# -------------------------

# Conteneur affiché avant le début du quiz
intro_quiz = tk.Frame(
    carte_quiz,
    bg="white"
)

# Affichage du nombre de questions
tk.Label(
    intro_quiz,
    text=f"{len(questions)} questions",
    bg="white",
    fg="#252633",
    font=("Arial", 18, "bold"),
).pack(anchor="w")

# Instructions destinées à l'utilisateur
tk.Label(
    intro_quiz,
    text="Prenez le temps de choisir une réponse à chaque question.",
    bg="white",
    fg="#686a75",
    font=("Arial", 11),
).pack(anchor="w", pady=(8, 18))


# -------------------------
# Zone des questions
# -------------------------

# Conteneur affichant les questions pendant le quiz
zone_questions = tk.Frame(
    carte_quiz,
    bg="white"
)

# Variable dynamique affichant la progression du quiz
progression = tk.StringVar()

tk.Label(
    zone_questions,
    textvariable=progression,
    bg="white",
    fg="#5356f6",
    font=("Arial", 10, "bold"),
).pack(anchor="w")

# Label qui affichera le texte de la question actuelle
libelle_question = tk.Label(
    zone_questions,
    bg="white",
    fg="#252633",
    font=("Arial", 17, "bold"),
    wraplength=720,
    justify="left",
)

libelle_question.pack(anchor="w", pady=(14, 18))

# Variable qui mémorise le choix sélectionné par l'utilisateur
choix_selectionne = tk.StringVar()

# Conteneur dans lequel seront créés les boutons de réponse
zone_choix = tk.Frame(
    zone_questions,
    bg="white"
)

zone_choix.pack(fill="x")

# Variable permettant d'afficher un message d'erreur
statut_quiz = tk.StringVar()

tk.Label(
    zone_questions,
    textvariable=statut_quiz,
    bg="white",
    fg="#b33b3b",
    font=("Arial", 10),
).pack(anchor="w", pady=(10, 0))

# Conteneur des boutons Précédent et Suivant
navigation_quiz = tk.Frame(
    zone_questions,
    bg="white"
)

navigation_quiz.pack(fill="x", pady=(18, 0))


# -------------------------
# Écran des résultats
# -------------------------

# Conteneur affiché à la fin du quiz
resultat_quiz = tk.Frame(
    carte_quiz,
    bg="white"
)

# Variable dynamique contenant le score final
score_final = tk.StringVar()

tk.Label(
    resultat_quiz,
    textvariable=score_final,
    bg="white",
    fg="#252633",
    font=("Arial", 21, "bold"),
).pack(anchor="w")

# Variable dynamique contenant le message de résultat
message_resultat = tk.StringVar()

tk.Label(
    resultat_quiz,
    textvariable=message_resultat,
    bg="white",
    fg="#686a75",
    font=("Arial", 12),
).pack(anchor="w", pady=(8, 18))


# ============================================================
# 8. GESTION DES RÉPONSES SÉLECTIONNÉES
# ============================================================

def actualiser_selection_choix():
    # Parcourt tous les boutons de réponse présents dans la zone
    for bouton in zone_choix.winfo_children():

        # Vérifie si le texte du bouton correspond à la réponse choisie
        selectionne = bouton.cget("text") == choix_selectionne.get()

        # Modifie l'apparence du bouton selon son état
        # Un bouton sélectionné est violet clair
        # Les autres conservent leur fond habituel
        bouton.configure(
            bg="#e7e8ff" if selectionne else "#f7f8fc",
            fg="#3031a5" if selectionne else "#454650",
            activebackground="#dfe0ff" if selectionne else "#eeeeef",
            font=(
                "Arial",
                12,
                "bold" if selectionne else "normal"
            ),
        )


def selectionner_reponse(reponse):
    # Enregistre la réponse choisie dans la variable Tkinter
    choix_selectionne.set(reponse)

    # Actualise l'apparence des boutons
    actualiser_selection_choix()


# ============================================================
# 9. AFFICHAGE D'UNE QUESTION
# ============================================================

def afficher_question():
    # Récupère les données de la question actuelle
    question = questions[question_actuelle]

    # Met à jour l'indicateur de progression
    progression.set(
        f"Question {question_actuelle + 1} sur {len(questions)}"
    )

    # Affiche le texte de la question
    libelle_question.configure(text=question["question"])

    # Le bouton devient Terminer pour la dernière question
    # Sinon, il conserve le texte Suivant
    bouton_suivant.configure(
        text="Terminer"
        if question_actuelle == len(questions) - 1
        else "Suivant"
    )

    # Restaure la réponse précédemment enregistrée
    # Si aucune réponse n'existe, la sélection reste vide
    choix_selectionne.set(
        reponses[question_actuelle] or ""
    )

    # Efface un éventuel message d'erreur précédent
    statut_quiz.set("")

    # Supprime les anciens boutons de réponse
    for widget in zone_choix.winfo_children():
        widget.destroy()

    # Crée un bouton pour chaque réponse possible
    for choix in question["choix"]:
        tk.Button(
            zone_choix,
            text=choix,

            # Associe chaque bouton à sa propre réponse
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
        ).pack(
            fill="x",
            anchor="w",
            pady=4
        )

    # Met en évidence la réponse déjà sélectionnée, le cas échéant
    actualiser_selection_choix()


# ============================================================
# 10. DÉMARRAGE ET RÉINITIALISATION DU QUIZ
# ============================================================

def commencer_quiz():
    # Permet de modifier l'indice global de la question
    global question_actuelle

    # Retour à la première question
    question_actuelle = 0

    # Réinitialisation de toutes les réponses
    reponses[:] = [None] * len(questions)

    # Masque l'écran d'introduction
    intro_quiz.pack_forget()

    # Masque les anciens résultats
    resultat_quiz.pack_forget()

    # Affiche la zone contenant les questions
    zone_questions.pack(fill="x")

    # Affiche la première question
    afficher_question()


# ============================================================
# 11. CALCUL ET AFFICHAGE DU SCORE FINAL
# ============================================================

def terminer_quiz():
    # Calcule le nombre de bonnes réponses
    # zip associe chaque réponse à la question correspondante
    # La comparaison renvoie True si la réponse est correcte
    # En Python, True vaut 1 et False vaut 0
    score = sum(
        reponse == question["reponse"]
        for reponse, question in zip(reponses, questions)
    )

    # Affiche le score obtenu sur le nombre total de questions
    score_final.set(
        f"Votre score : {score} / {len(questions)}"
    )

    # Affiche un message selon le résultat obtenu
    message_resultat.set(
        "Excellent travail !" if score == len(questions)
        else "Vous pouvez recommencer pour améliorer votre score."
    )

    # Masque la zone des questions
    zone_questions.pack_forget()

    # Affiche l'écran des résultats
    resultat_quiz.pack(fill="x")


# ============================================================
# 12. PASSAGE À LA QUESTION SUIVANTE
# ============================================================

def question_suivante():
    # Permet de modifier l'indice global de la question
    global question_actuelle

    # Récupère la réponse sélectionnée
    reponse = choix_selectionne.get()

    # Empêche de continuer sans avoir choisi de réponse
    if not reponse:
        statut_quiz.set(
            "Sélectionnez une réponse pour continuer."
        )
        return

    # Enregistre la réponse de la question actuelle
    reponses[question_actuelle] = reponse

    # Si la dernière question est atteinte, termine le quiz
    if question_actuelle == len(questions) - 1:
        terminer_quiz()
        return

    # Passe à la question suivante
    question_actuelle += 1

    # Affiche la nouvelle question
    afficher_question()


# ============================================================
# 13. RETOUR À LA QUESTION PRÉCÉDENTE
# ============================================================

def question_precedente():
    # Permet de modifier l'indice global de la question
    global question_actuelle

    # Vérifie qu'il existe une question précédente
    if question_actuelle > 0:

        # Enregistre la réponse actuelle avant de revenir en arrière
        # Si aucun choix n'est fait, la réponse devient None
        reponses[question_actuelle] = (
            choix_selectionne.get() or None
        )

        # Retourne à la question précédente
        question_actuelle -= 1

        # Réaffiche la question précédente et sa réponse éventuelle
        afficher_question()


# ============================================================
# 14. CRÉATION DES BOUTONS DE NAVIGATION DU QUIZ
# ============================================================

# Bouton permettant de revenir à la question précédente
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

# Positionnement du bouton à gauche
bouton_precedent.pack(side="left")


# Bouton permettant de passer à la question suivante
# Sur la dernière question, il permet de terminer le quiz
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

# Positionnement du bouton à droite
bouton_suivant.pack(side="right")


# ============================================================
# 15. BOUTONS DE L'ÉCRAN DES RÉSULTATS ET D'INTRODUCTION
# ============================================================

# Bouton permettant de recommencer le quiz depuis le début
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


# Bouton permettant de lancer le quiz
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

# Affichage initial de l'écran d'introduction
intro_quiz.pack(fill="x")


# La page Quiz est conservée telle qu'elle a été construite.
# Ne pas détruire ses widgets ici : cela supprimerait le titre et la carte du quiz.


# ============================================================
# 17. CRÉATION DES PAGES CONNEXION ET COMPTE
# ============================================================

# Création du conteneur de la page de connexion
page_connexion = tk.Frame(
    contenu,
    bg="#f7f8fc"
)

# Positionnement de la page de connexion
page_connexion.place(
    relx=0,
    rely=0,
    relwidth=1,
    relheight=1
)

# Enregistrement dans le dictionnaire des pages
pages["Connexion"] = page_connexion


# Création du conteneur de la page du compte utilisateur
page_compte = tk.Frame(
    contenu,
    bg="#f7f8fc"
)

# Positionnement de la page du compte
page_compte.place(
    relx=0,
    rely=0,
    relwidth=1,
    relheight=1
)

# Enregistrement dans le dictionnaire des pages
pages["Compte"] = page_compte


# ============================================================
# 18. CONTENU DE LA PAGE COMPTE
# ============================================================

# Affichage du titre de la page du compte
tk.Label(
    page_compte,
    text="Mon compte",
    bg="#f7f8fc",
    fg="#252633",
    font=("Arial", 25, "bold"),
).pack(anchor="w")

# Variable contenant les informations de l'utilisateur connecté
identite_compte = tk.StringVar()

# Affichage du nom et de l'identifiant de l'utilisateur
tk.Label(
    page_compte,
    textvariable=identite_compte,
    bg="#f7f8fc",
    fg="#686a75",
    font=("Arial", 12),
).pack(anchor="w", pady=(12, 0))


# Bouton permettant de fermer la session utilisateur
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


# ============================================================
# 19. CONTENU DE LA PAGE DE CONNEXION
# ============================================================

# Affichage du titre de la page de connexion
tk.Label(
    page_connexion,
    text="Bienvenue sur SQuizi !",
    bg="#f7f8fc",
    fg="#252633",
    font=("Arial", 25, "bold"),
).pack(anchor="w")

# Affichage des instructions de connexion
tk.Label(
    page_connexion,
    text="Connectez-vous ou créez un compte pour accéder à SQuizi.",
    bg="#f7f8fc",
    fg="#686a75",
    font=("Arial", 12),
).pack(anchor="w", pady=(8, 24))


# Création de la carte blanche contenant le formulaire
carte_connexion = tk.Frame(
    page_connexion,
    bg="white",
    padx=28,
    pady=24
)

carte_connexion.pack(fill="x")


# ============================================================
# 20. VARIABLES DU FORMULAIRE D'AUTHENTIFICATION
# ============================================================

# Indique le mode actuel : connexion ou création de compte
mode_connexion = tk.StringVar(value="Connexion")

# Variables associées aux champs de saisie
# Tkinter les met à jour automatiquement lorsque l'utilisateur écrit

identifiant = tk.StringVar()
mot_de_passe = tk.StringVar()

# Variable utilisée pour afficher les messages d'information ou d'erreur
statut_auth = tk.StringVar()


# Affichage du titre du formulaire selon le mode choisi
tk.Label(
    carte_connexion,
    textvariable=mode_connexion,
    bg="white",
    fg="#252633",
    font=("Arial", 18, "bold"),
).pack(anchor="w", pady=(0, 18))


# ============================================================
# 21. CHAMP NOM
# ============================================================

# Conteneur du champ Nom
# Ce champ est affiché uniquement lors de la création d'un compte
champ_nom = tk.Frame(
    carte_connexion,
    bg="white"
)

# Étiquette du champ Nom
tk.Label(
    champ_nom,
    text="Nom",
    bg="white",
    fg="#454650",
    font=("Arial", 11)
).pack(anchor="w", pady=(0, 6))

# Champ de saisie du nom de l'utilisateur
tk.Entry(
    champ_nom,
    font=("Arial", 12)
).pack(fill="x", ipady=6)


# ============================================================
# 22. CHAMP IDENTIFIANT
# ============================================================

# Étiquette du champ identifiant
tk.Label(
    carte_connexion,
    text="Identifiant",
    bg="white",
    fg="#454650",
    font=("Arial", 11)
).pack(anchor="w", pady=(12, 6))

# Champ de saisie associé à la variable identifiant
tk.Entry(
    carte_connexion,
    textvariable=identifiant,
    font=("Arial", 12)
).pack(fill="x", ipady=6)


# ============================================================
# 23. CHAMP MOT DE PASSE
# ============================================================

# Étiquette du champ mot de passe
tk.Label(
    carte_connexion,
    text="Mot de passe",
    bg="white",
    fg="#454650",
    font=("Arial", 11)
).pack(anchor="w", pady=(12, 6))

# Champ de saisie du mot de passe
# show="*" masque les caractères saisis à l'écran
tk.Entry(
    carte_connexion,
    textvariable=mot_de_passe,
    show="*",
    font=("Arial", 12)
).pack(fill="x", ipady=6)


# ============================================================
# 24. BOUTON D'ACTION DU FORMULAIRE
# ============================================================

# Bouton qui permettra de se connecter ou de créer un compte
# Son texte et sa commande seront définis plus bas
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


# Label affichant les messages liés à l'authentification
statut_label = tk.Label(
    carte_connexion,
    textvariable=statut_auth,
    bg="white",
    fg="#686a75",
    font=("Arial", 10),
    wraplength=650,
)

statut_label.pack(anchor="w")


# Bouton permettant de passer de la connexion à la création de compte
# ou inversement
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


# ============================================================
# 25. CHANGEMENT DE MODE D'AUTHENTIFICATION
# ============================================================

def changer_mode_auth():
    # Si le mode actuel est Connexion, passer à Créer un compte
    # Sinon, revenir au mode Connexion

    if mode_connexion.get() == "Connexion":
        nouveau_mode = "Créer mon compte"
    else:
        nouveau_mode = "Connexion"

    # Met à jour le titre du formulaire
    mode_connexion.set(nouveau_mode)

    # Efface les éventuels messages d'erreur précédents
    statut_auth.set("")

    # Si l'utilisateur souhaite créer un compte
    if nouveau_mode == "Créer mon compte":


        # Modifie le texte du bouton principal
        bouton_action.configure(text="Créer mon compte")

        # Modifie le texte du bouton de changement de mode
        bouton_changer_mode.configure(
            text="Déjà un compte ? Se connecter"
        )

    # Si l'utilisateur revient au mode Connexion
    else:

        # Masque le champ Nom
        champ_nom.pack_forget()

        # Met à jour le bouton principal
        bouton_action.configure(text="Se connecter")

        # Met à jour le bouton de changement de mode
        bouton_changer_mode.configure(
            text="Pas encore de compte ? Créer un compte"
        )


# ============================================================
# 26. VALIDATION DU FORMULAIRE ET CONNEXION
# ============================================================

def envoyer_formulaire_auth():
    # Permet de modifier les variables globales
    global connecte, page_actuelle

    # Récupère les valeurs des champs obligatoires
    # strip() supprime les espaces au début et à la fin de l'identifiant
    # Le mot de passe est récupéré sans modification
    champs_requis = [
        identifiant.get().strip(),
        mot_de_passe.get()
    ]
    identifiant_creer=champs_requis[0]
    mdp_creer=champs_requis[1]

    # En mode création de compte, le nom devient obligatoire
    if mode_connexion.get() == "Créer mon compte":
        # Vérifie que tous les champs requis sont remplis
        if not all(champs_requis):
            # Affiche un message si un champ est vide
            statut_auth.set(
                "Merci de remplir tous les champs."
            )
            return
        
        #verifie la connexion avec la bd
        if not(creer_compte(identifiant_creer, mdp_creer)):
            statut_auth.set(
                "L'identifiant existe déjà"
            )
            return
    else:
        # Vérifie que tous les champs requis sont remplis
        if not all(champs_requis):
            # Affiche un message si un champ est vide
            statut_auth.set(
                "Merci de remplir tous les champs."
            )
            return
        
        #verifie la connexion avec la bd
        if not(verifier_connexion(identifiant_creer, mdp_creer)[0]):
            statut_auth.set(
                "Mot de passe ou identifiant incorrect"
            )
            return
        else:
            admin=verifier_connexion(identifiant_creer, mdp_creer)[1]


    # Indique que l'utilisateur est considéré comme connecté
    connecte = True

    # Affiche la barre de navigation au-dessus de la zone de contenu
    bande_haut.pack(
        fill="x",
        before=contenu
    )

    # Réinitialise la page actuellement sélectionnée
    page_actuelle = None

    # Met à jour le titre de l'accueil avec l'identifiant saisi
    titre_accueil.set(
        f"Bienvenue sur SQuizi, {identifiant.get().strip()} !"
    )

    # Redirige l'utilisateur vers la page d'accueil
    afficher_page("Accueil")


# ============================================================
# 27. CONFIGURATION INITIALE DES BOUTONS D'AUTHENTIFICATION
# ============================================================

# Configure le bouton principal pour le mode Connexion
bouton_action.configure(
    text="Se connecter",
    command=envoyer_formulaire_auth,
)

# Configure le bouton permettant de changer de mode
bouton_changer_mode.configure(
    text="Pas encore de compte ? Créer un compte",
    command=changer_mode_auth,
)




# ============================================================
# 28. AFFICHAGE INITIAL ET LANCEMENT DE L'APPLICATION
# ============================================================

# Masque la barre de navigation au démarrage
# L'utilisateur doit d'abord passer par la page de connexion
bande_haut.pack_forget()

# Affiche la page de connexion en premier
pages["Connexion"].tkraise()

# Lance la boucle principale de Tkinter
# Elle maintient la fenêtre ouverte et gère les clics,
# les saisies et les autres événements de l'interface
fenetre.mainloop()

