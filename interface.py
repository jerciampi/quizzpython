# Importation de la bibliothèque Tkinter pour créer l'interface graphique
import os
import tkinter as tk
from database_quiz import *
from quiz import obtenir_donnees
import time



# ============================================================
# 1. INITIALISATION DE LA FENÊTRE PRINCIPALE
# ============================================================

# Création de la fenêtre principale de l'application
fenetre = tk.Tk()

# Définition du titre de la fenêtre
fenetre.title("SQuizi")

# Définition de la taille initiale de la fenêtre
fenetre.geometry("900x700")

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

    # Si on quitte la page Quiz, on arrête le chronomètre pour éviter qu'il tourne en fond
    if page_actuelle == "Quiz":
        arreter_chronometre()

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

    # Actualise la liste à chaque ouverture de l'onglet Quiz.
    if nom_page == "Quiz":
        afficher_liste_quiz()

    if nom_page == "Leaderboard":
        afficher_liste_quiz_leaderboard()

    # Mémorise la page actuellement affichée
    page_actuelle = nom_page


def se_deconnecter():
    # Permet de modifier les variables globales
    global connecte, page_actuelle

    arreter_chronometre()

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

image_logo = tk.PhotoImage(file="logo.png", master=fenetre)
image_reduite = image_logo.subsample(12, 12)
logo = tk.Button(
    zone_logo,
    command=lambda: afficher_page("Accueil"),
    image=image_reduite,
    bg="#d5d5d9",
    fg="#55565e",
    font=("Arial", 10, "bold"),
    width=60,
    height=80  ,
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
for nom_page in ("Quiz", "Mes activités","Leaderboard","Créer un quiz"):

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
contenu.pack(fill="both", expand=True)

# ============================================================
# 4.5 PAGE DU LEADERBOARD
# ============================================================
# La zone de contenu occupe tout l'espace disponible
def afficher_details_leaderboard(id_quiz, nom_quiz):
    scores = obtenir_leaderboard_quiz(id_quiz)
    
    fenetre_lb = tk.Toplevel(fenetre)
    fenetre_lb.title(f"Leaderboard - {nom_quiz}")
    fenetre_lb.geometry("450x400")
    fenetre_lb.configure(bg="#f7f8fc")

    tk.Label(fenetre_lb, text=f"Classement : {nom_quiz}", bg="#f7f8fc", font=("Arial", 16, "bold")).pack(pady=15)

    if not scores:
        tk.Label(fenetre_lb, text="Aucun score enregistré pour ce quiz.", bg="#f7f8fc", fg="#686a75").pack(pady=20)
        return

    for idx, (utilisateur, score, chrono, date) in enumerate(scores, 1):
        texte_ligne = f"{idx}. {utilisateur} — Score : {score} (Temps : {chrono}s) le {date}"
        tk.Label(fenetre_lb, text=texte_ligne, bg="white", font=("Arial", 11), padx=10, pady=5).pack(fill="x", padx=20, pady=2)

def afficher_liste_quiz_leaderboard():
    # Reconstruit la liste à partir des quiz enregistrés en base.
    for widget in contenu_liste_lb.winfo_children():
        widget.destroy()

    quizs = liste_quiz()
    if not quizs:
        tk.Label(
            contenu_liste_lb,
            text="Aucun quiz n'est disponible pour le moment.",
            bg="white",
            fg="#686a75",
            font=("Arial", 11),
        ).pack(anchor="w", pady=12)
        return

    for id_quiz, chemin_quiz in quizs:
        nom_quiz = os.path.splitext(
            os.path.basename(os.path.normpath(chemin_quiz))
        )[0]
        ligne_leaderboard = tk.Frame(
            contenu_liste_lb,
            bg="#f7f8fc",
            padx=14,
            pady=12,
        )
        ligne_leaderboard.pack(fill="x", pady=5)

        tk.Label(
            ligne_leaderboard,
            text=nom_quiz,
            bg="#f7f8fc",
            fg="#252633",
            font=("Arial", 12, "bold"),
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        tk.Button(
            ligne_leaderboard,
            text="Voir le leaderboard",
            command=lambda quiz_id=id_quiz, chemin=chemin_quiz: afficher_details_leaderboard(quiz_id, nom_quiz),
            bg="#5356f6",
            fg="white",
            activebackground="#4245df",
            relief="flat",
            padx=14,
            pady=8,
            font=("Arial", 10, "bold"),
            cursor="hand2",
        ).pack(side="right")

# ============================================================
# 6. DONNÉES DU QUIZ & CHRONOMÈTRE
# ============================================================

# Les questions sont chargées depuis le fichier du quiz sélectionné.
questions = []
reponses = []
question_actuelle = 0
quiz_actuel_id = None

# Variables pour le chronomètre (part de 0 et max 1 heure = 3600 secondes)
TEMPS_MAX_QUIZ = 3600
temps_ecoule = 0
temps_final = 0
chronometre_id = None

# ============================================================
# 7.1 CRÉATION DE LA PAGE DU QUIZ
# ============================================================

# Création du conteneur principal de la page Quiz
page_leaderboard = tk.Frame(
    contenu,
    bg="#f7f8fc"
)

# Enregistrement de la page dans le dictionnaire
pages["Leaderboard"] = page_leaderboard

# Positionnement de la page dans la zone de contenu
page_leaderboard.place(
    relx=0,
    rely=0,
    relwidth=1,
    relheight=1
)

# Affichage du titre de la page
tk.Label(
    page_leaderboard,
    text="Leaderboard disponibles",
    bg="#f7f8fc",
    fg="#252633",
    font=("Arial", 25, "bold"),
).pack(anchor="w")

# Affichage de la description du quiz
tk.Label(
    page_leaderboard,
    text="Choisissez le leaderboard du quiz souhaité.",
    bg="#f7f8fc",
    fg="#686a75",
    font=("Arial", 12),
).pack(anchor="w", pady=(8, 28))


# -------------------------
# Carte principale du quiz
# -------------------------

# Création de la carte blanche qui contient le quiz
carte_leaderboard = tk.Frame(
    page_leaderboard,
    bg="white",
    padx=24,
    pady=24
)

carte_leaderboard.pack(fill="x")


# -------------------------
# Écran d'introduction
# -------------------------

# Conteneur affiché avant le début du quiz
intro_leaderboard = tk.Frame(
    carte_leaderboard,
    bg="white"
)

# Introduction et liste défilante des quiz disponibles
tk.Label(
    intro_leaderboard,
    text="Tous les leaderboards",
    bg="white",
    fg="#252633",
    font=("Arial", 18, "bold"),
).pack(anchor="w")

# Instructions destinées à l'utilisateur
tk.Label(
    intro_leaderboard,
    text="Sélectionnez le leaderboard que vous souhaitez consulter",
    bg="white",
    fg="#686a75",
    font=("Arial", 11),
).pack(anchor="w", pady=(8, 18))

zone_liste_lb = tk.Frame(intro_leaderboard, bg="white")
zone_liste_lb.pack(fill="both", expand=True)

canvas_liste_lb = tk.Canvas(
    zone_liste_lb,
    bg="white",
    height=340,
    highlightthickness=0,
)
barre_defilement_lb = tk.Scrollbar(
    zone_liste_lb,
    orient="vertical",
    command=canvas_liste_lb.yview,
)
canvas_liste_lb.configure(yscrollcommand=barre_defilement_lb.set)
barre_defilement_lb.pack(side="right", fill="y")
canvas_liste_lb.pack(side="left", fill="both", expand=True)

contenu_liste_lb = tk.Frame(canvas_liste_lb, bg="white")
canvas_liste_lb.create_window(
    (0, 0),
    window=contenu_liste_lb,
    anchor="nw",
    tags="contenu_liste",
)

contenu_liste_lb.bind(
    "<Configure>",
    lambda _: canvas_liste_lb.configure(
        scrollregion=canvas_liste_lb.bbox("all")
    ),
)
canvas_liste_lb.bind(
    "<Configure>",
    lambda evenement: canvas_liste_lb.itemconfigure(
        "contenu_liste",
        width=evenement.width,
    ),
)
intro_leaderboard.pack(fill="x")
afficher_liste_quiz_leaderboard()

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
    text="Quiz disponibles",
    bg="#f7f8fc",
    fg="#252633",
    font=("Arial", 25, "bold"),
).pack(anchor="w")

# Affichage de la description du quiz
tk.Label(
    page_quiz,
    text="Choisissez un quiz pour commencer.",
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

# Introduction et liste défilante des quiz disponibles
tk.Label(
    intro_quiz,
    text="Tous les quiz",
    bg="white",
    fg="#252633",
    font=("Arial", 18, "bold"),
).pack(anchor="w")

# Instructions destinées à l'utilisateur
tk.Label(
    intro_quiz,
    text="Sélectionnez le quiz auquel vous souhaitez jouer.",
    bg="white",
    fg="#686a75",
    font=("Arial", 11),
).pack(anchor="w", pady=(8, 18))

zone_liste_quiz = tk.Frame(intro_quiz, bg="white")
zone_liste_quiz.pack(fill="both", expand=True)

canvas_liste_quiz = tk.Canvas(
    zone_liste_quiz,
    bg="white",
    height=340,
    highlightthickness=0,
)
barre_defilement_quiz = tk.Scrollbar(
    zone_liste_quiz,
    orient="vertical",
    command=canvas_liste_quiz.yview,
)
canvas_liste_quiz.configure(yscrollcommand=barre_defilement_quiz.set)
barre_defilement_quiz.pack(side="right", fill="y")
canvas_liste_quiz.pack(side="left", fill="both", expand=True)

contenu_liste_quiz = tk.Frame(canvas_liste_quiz, bg="white")
canvas_liste_quiz.create_window(
    (0, 0),
    window=contenu_liste_quiz,
    anchor="nw",
    tags="contenu_liste",
)

contenu_liste_quiz.bind(
    "<Configure>",
    lambda _: canvas_liste_quiz.configure(
        scrollregion=canvas_liste_quiz.bbox("all")
    ),
)
canvas_liste_quiz.bind(
    "<Configure>",
    lambda evenement: canvas_liste_quiz.itemconfigure(
        "contenu_liste",
        width=evenement.width,
    ),
)


# -------------------------
# Zone des questions & Entête avec Chrono
# -------------------------

zone_questions = tk.Frame(
    carte_quiz,
    bg="white"
)

entete_quiz_frame = tk.Frame(zone_questions, bg="white")
entete_quiz_frame.pack(fill="x", pady=(0, 10))

progression = tk.StringVar()
tk.Label(
    entete_quiz_frame,
    textvariable=progression,
    bg="white",
    fg="#5356f6",
    font=("Arial", 10, "bold"),
).pack(side="left")

# Label visuel du chronomètre pendant le quiz
texte_chronometre = tk.StringVar()
tk.Label(
    entete_quiz_frame,
    textvariable=texte_chronometre,
    bg="white",
    fg="#686a75",
    font=("Arial", 10, "bold"),
).pack(side="right")

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

zone_choix = tk.Frame(
    zone_questions,
    bg="white"
)
zone_choix.pack(fill="x")

statut_quiz = tk.StringVar()
tk.Label(
    zone_questions,
    textvariable=statut_quiz,
    bg="white",
    fg="#b33b3b",
    font=("Arial", 10),
).pack(anchor="w", pady=(10, 0))

navigation_quiz = tk.Frame(
    zone_questions,
    bg="white"
)
navigation_quiz.pack(fill="x", pady=(18, 0))


# -------------------------
# Écran des résultats
# -------------------------

resultat_quiz = tk.Frame(
    carte_quiz,
    bg="white"
)

score_final = tk.StringVar()
tk.Label(
    resultat_quiz,
    textvariable=score_final,
    bg="white",
    fg="#252633",
    font=("Arial", 21, "bold"),
).pack(anchor="w")

# Variable et Label pour afficher le temps sur l'écran des résultats
temps_resultat_str = tk.StringVar()
tk.Label(
    resultat_quiz,
    textvariable=temps_resultat_str,
    bg="white",
    fg="#5356f6",
    font=("Arial", 12, "bold"),
).pack(anchor="w", pady=(4, 8))

message_resultat = tk.StringVar()
tk.Label(
    resultat_quiz,
    textvariable=message_resultat,
    bg="white",
    fg="#686a75",
    font=("Arial", 12),
).pack(anchor="w", pady=(0, 18))


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
# 8.5. GESTION DU CHRONOMÈTRE (COMPTEUR UP DE 0)
# ============================================================

def demarrer_chronometre():
    global temps_ecoule, chronometre_id
    temps_ecoule = 0
    mettre_a_jour_chrono()

def mettre_a_jour_chrono():
    global temps_ecoule, chronometre_id
    if temps_ecoule < TEMPS_MAX_QUIZ:
        minutes = temps_ecoule // 60
        secondes = temps_ecoule % 60
        texte_chronometre.set(f"⏱️ Temps : {minutes:02d}:{secondes:02d}")
        temps_ecoule += 1
        # Relance la fonction dans exactement 1 seconde (1000 millisecondes)
        chronometre_id = fenetre.after(1000, mettre_a_jour_chrono)
    else:
        # Limite maximale d'une heure atteinte : validation automatique
        texte_chronometre.set("⏱️ 1h max atteinte !")
        statut_quiz.set("La limite de temps d'une heure a été atteinte.")
        afficher_resultat()

def arreter_chronometre():
    global chronometre_id
    if chronometre_id is not None:
        fenetre.after_cancel(chronometre_id)
        chronometre_id = None


# ============================================================
# 9. AFFICHAGE D'UNE QUESTION
# ============================================================

def afficher_liste_quiz():
    # Reconstruit la liste à partir des quiz enregistrés en base.
    for widget in contenu_liste_quiz.winfo_children():
        widget.destroy()

    quizs = liste_quiz()
    if not quizs:
        tk.Label(
            contenu_liste_quiz,
            text="Aucun quiz n'est disponible pour le moment.",
            bg="white",
            fg="#686a75",
            font=("Arial", 11),
        ).pack(anchor="w", pady=12)
        return

    for id_quiz, chemin_quiz in quizs:
        nom_quiz = os.path.splitext(
            os.path.basename(os.path.normpath(chemin_quiz))
        )[0]
        ligne_quiz = tk.Frame(
            contenu_liste_quiz,
            bg="#f7f8fc",
            padx=14,
            pady=12,
        )
        ligne_quiz.pack(fill="x", pady=5)

        tk.Label(
            ligne_quiz,
            text=nom_quiz,
            bg="#f7f8fc",
            fg="#252633",
            font=("Arial", 12, "bold"),
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        tk.Button(
            ligne_quiz,
            text="Commencer le quiz",
            command=lambda quiz_id=id_quiz, chemin=chemin_quiz: lancer_quiz(
                quiz_id, chemin
            ),
            bg="#5356f6",
            fg="white",
            activebackground="#4245df",
            relief="flat",
            padx=14,
            pady=8,
            font=("Arial", 10, "bold"),
            cursor="hand2",
        ).pack(side="right")


def lancer_quiz(id_quiz, chemin_quiz):
    # Charge les données à l'aide du lecteur existant du module quiz.
    global questions, reponses, quiz_actuel_id

    questions_brutes, propositions, bonnes_reponses = obtenir_donnees(
        chemin_quiz
    )
    questions = [
        {
            "question": question,
            "choix": choix,
            "reponse": bonne_reponse,
        }
        for question, choix, bonne_reponse in zip(
            questions_brutes, propositions, bonnes_reponses
        )
    ]
    if not questions:
        tk.Label(
            contenu_liste_quiz,
            text="Ce quiz ne contient aucune question.",
            bg="white",
            fg="#b33b3b",
            font=("Arial", 10),
        ).pack(anchor="w", pady=6)
        return

    quiz_actuel_id = id_quiz
    commencer_quiz()


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

    # Démarrage du chronomètre
    demarrer_chronometre()

    # Affiche la première question
    afficher_question()


# ============================================================
# 11. CALCUL ET AFFICHAGE DU SCORE FINAL & STOCKAGE DU TEMPS
# ============================================================

def afficher_resultat():
    global identifiant_bd, temps_final
    
    # Arrêt du chronomètre et stockage du temps final en secondes
    arreter_chronometre()
    temps_final = max(0, temps_ecoule - 1)

    # Formatage du temps
    mins = temps_final // 60
    secs = temps_final % 60
    secs2 = temps_final
    
    # 1. La string pure pour la base de données (ex: "02:15")
    temps_sql = f"{secs2:02d}"  

    # 2. Mise à jour de l'affichage visuel sur l'écran de fin
    temps_resultat_str.set(f"⏱️ Temps réalisé : {mins:02d} min {secs:02d} s")

    score = sum(
        reponse == question["reponse"]
        for reponse, question in zip(reponses, questions)
    )
    
    # Enregistrement dans l'historique en passant la string du temps
    enregistrer_partie(identifiant_bd, quiz_actuel_id, score, temps_sql)
    
    score_final.set(
        f"Votre score : {score} / {len(questions)}"
    )

    message_resultat.set(
        "Excellent travail !" if score == len(questions)
        else "Vous pouvez recommencer pour améliorer votre score."
    )

    zone_questions.pack_forget()
    resultat_quiz.pack(fill="x")


# ============================================================
# 12. PASSAGE À LA QUESTION SUIVANTE
# ============================================================

def valider_reponse():
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
        afficher_resultat()
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
    command=valider_reponse,
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

# Conteneur horizontal pour aligner les boutons sur l'écran des résultats
zone_boutons_resultat = tk.Frame(resultat_quiz, bg="white")
zone_boutons_resultat.pack(anchor="w")

# Bouton permettant de recommencer le quiz depuis le début
tk.Button(
    zone_boutons_resultat,
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
).pack(side="left", padx=(0, 10))

# Bouton permettant de revenir à la liste des quiz
tk.Button(
    zone_boutons_resultat,
    text="Retour à la liste des quiz",
    command=lambda: retour_liste_quiz(),
    bg="#eeeeef",
    fg="#454650",
    activebackground="#d5d5d9",
    relief="flat",
    padx=18,
    pady=9,
    font=("Arial", 10),
    cursor="hand2",
).pack(side="left")


# Affichage initial de l'écran d'introduction
intro_quiz.pack(fill="x")


def retour_liste_quiz():
    arreter_chronometre()
    # Réaffiche la liste et masque les vues de jeu et de résultat.
    zone_questions.pack_forget()
    resultat_quiz.pack_forget()
    intro_quiz.pack(fill="x")
    afficher_liste_quiz()


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
identifiant_bd = ""
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
admin=0
def envoyer_formulaire_auth():
    # Permet de modifier les variables globales
    global connecte, page_actuelle,identifiant_bd,admin

    # Récupère les valeurs des champs obligatoires
    # strip() supprime les espaces au début et à la fin de l'identifiant
    # Le mot de passe est récupéré sans modification
    champs_requis = [
        identifiant.get().strip(),
        mot_de_passe.get()
    ]
    identifiant_creer=champs_requis[0]
    mdp_creer=champs_requis[1]
    
    identifiant_bd=champs_requis[0]
    
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
            #récupération de la variable pour savoir si le compte est admin
            admin=verifier_connexion(identifiant_creer, mdp_creer)[1]
            print(admin)

    # Indique que l'utilisateur est considéré comme connecté
    connecte = True

    # Affiche la barre de navigation au-dessus de la zone de contenu
    bande_haut.pack(
        fill="x",
        before=contenu
    )

    # Réinitialise la page actuellement sélectionnée
    page_actuelle = None
    titre_accueil = tk.StringVar(value="Bienvenue sur SQuizi !")
    # Met à jour le titre de l'accueil avec l'identifiant saisi
    titre_accueil.set(
        f"Bienvenue sur SQuizi, {identifiant.get().strip()} !"
    )
    # ============================================================
    # CRÉATION DES PAGES ACCUEIL ET MES ACTIVITÉS
    # ============================================================

    # Chaque élément contient :
    # - le nom interne de la page
    # - le titre affiché
    # - une description
    # - un message dans la carte centrale
    # Variable dynamique pour personnaliser le titre de la page d'accueil
    
    historique = obtenir_historique(identifiant_bd)
    historique_afficher=""
    for k in historique:
        historique_afficher+=k+"\n\n"
    if admin==1:
        print("connexion administrateur")
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
                #mettre les valeurs de historique
                historique_afficher,
            ),
            (
                "Créer un quiz",
                "Création de quiz",
                "Créez un quiz",
                "Coucou",
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
    else:        
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
                #mettre les valeurs de historique
                historique_afficher,
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