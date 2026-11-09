# ============================================================
# SQUIZI - APPLICATION COMPLÈTE (TOUTES FONCTIONNALITÉS REGROUPÉES)
# ============================================================

import os
import sqlite3
import time
import tkinter as tk

# Importation des modules backend du projet
from database_quiz import *
from quiz import obtenir_donnees
from creer_quiz import creer_fichier, ajout_question


# ============================================================
# 1. INITIALISATION DE LA FENÊTRE PRINCIPALE
# ============================================================

fenetre = tk.Tk()
fenetre.title("SQuizi")
fenetre.geometry("900x700")
fenetre.minsize(650, 450)
fenetre.configure(bg="#f7f8fc")

pages = {}
onglets = {}
page_actuelle = None
connecte = False
admin = 0


# ============================================================
# 2. GESTION DE LA NAVIGATION ENTRE LES PAGES
# ============================================================

def afficher_page(nom_page):
    global page_actuelle

    if not connecte:
        return

    # Si on quitte la page Quiz, on arrête le chronomètre
    if page_actuelle == "Quiz":
        arreter_chronometre()

    if page_actuelle == nom_page:
        return

    if page_actuelle in onglets:
        onglets[page_actuelle].configure(bg="#eeeeef", fg="#62636b")

    if nom_page in onglets:
        onglets[nom_page].configure(bg="#e2e3e7", fg="#30313a")

    pages[nom_page].tkraise()

    if nom_page == "Quiz":
        afficher_liste_quiz()

    if nom_page == "Leaderboard":
        afficher_liste_quiz_leaderboard()

    page_actuelle = nom_page


def se_deconnecter():
    global connecte, page_actuelle, admin

    arreter_chronometre()
    connecte = False
    admin = 0
    page_actuelle = None
    bande_haut.pack_forget()
    statut_auth.set("")
    pages["Connexion"].tkraise()


# ============================================================
# 3. CRÉATION DE LA BARRE DE NAVIGATION
# ============================================================

bande_haut = tk.Frame(fenetre, bg="#e6e6e8", height=64)
bande_haut.pack(fill="x")
bande_haut.pack_propagate(False)

# --- Logo ---
zone_logo = tk.Frame(bande_haut, bg="#e6e6e8")
zone_logo.pack(side="left", padx=(20, 24), pady=10)

try:
    image_logo = tk.PhotoImage(file="logo.png", master=fenetre)
    image_reduite = image_logo.subsample(12, 12)
    logo = tk.Button(
        zone_logo,
        command=lambda: afficher_page("Accueil"),
        image=image_reduite,
        bg="#d5d5d9",
        relief="flat",
        borderwidth=0,
        cursor="hand2",
    )
except Exception:
    logo = tk.Button(
        zone_logo,
        text="SQuizi",
        command=lambda: afficher_page("Accueil"),
        bg="#d5d5d9",
        fg="#55565e",
        font=("Arial", 10, "bold"),
        width=9,
        height=2,
        relief="flat",
        borderwidth=0,
        cursor="hand2",
    )

logo.pack()
onglets["Accueil"] = logo

# --- Boutons de Navigation ---
navigation = tk.Frame(bande_haut, bg="#e6e6e8")
navigation.pack(side="left", fill="y")

# --- Bouton Compte ---
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


def mettre_a_jour_barre_navigation():
    for widget in navigation.winfo_children():
        widget.destroy()

    liste_onglets = ["Quiz", "Mes activités", "Leaderboard"]
    if admin == 1:
        liste_onglets.append("Créer un quiz")

    for nom_page in liste_onglets:
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


# ============================================================
# 4. ZONE PRINCIPALE DE CONTENU
# ============================================================

contenu = tk.Frame(fenetre, bg="#f7f8fc", padx=48, pady=38)
contenu.pack(fill="both", expand=True)


# ============================================================
# 5. PAGE LEADERBOARD (CLASSEMENT)
# ============================================================

def afficher_details_leaderboard(id_quiz, nom_quiz):
    scores = obtenir_leaderboard_quiz(id_quiz)
    
    fenetre_lb = tk.Toplevel(fenetre)
    fenetre_lb.title(f"Leaderboard - {nom_quiz}")
    fenetre_lb.geometry("500x400")
    fenetre_lb.configure(bg="#f7f8fc")

    tk.Label(fenetre_lb, text=f"Classement : {nom_quiz}", bg="#f7f8fc", font=("Arial", 16, "bold")).pack(pady=15)

    if not scores:
        tk.Label(fenetre_lb, text="Aucun score enregistré pour ce quiz.", bg="#f7f8fc", fg="#686a75").pack(pady=20)
        return

    for idx, (utilisateur, score, chrono, date) in enumerate(scores, 1):
        try:
            val_sec = int(chrono)
            mins = val_sec // 60
            secs = val_sec % 60
            str_temps = f"{mins:02d}min{secs:02d}s"
        except Exception:
            str_temps = str(chrono)

        texte_ligne = f"{idx}. {utilisateur} — Score : {score} (Temps : {str_temps}) le {date}"
        tk.Label(fenetre_lb, text=texte_ligne, bg="white", font=("Arial", 10), padx=10, pady=5).pack(fill="x", padx=20, pady=2)


def afficher_liste_quiz_leaderboard():
    for widget in contenu_liste_lb.winfo_children():
        widget.destroy()

    quizs = liste_quiz()
    if not quizs:
        tk.Label(contenu_liste_lb, text="Aucun quiz disponible.", bg="white", fg="#686a75", font=("Arial", 11)).pack(anchor="w", pady=12)
        return

    for id_quiz, chemin_quiz in quizs:
        nom_quiz = os.path.splitext(os.path.basename(os.path.normpath(chemin_quiz)))[0]
        ligne = tk.Frame(contenu_liste_lb, bg="#f7f8fc", padx=14, pady=12)
        ligne.pack(fill="x", pady=5)

        tk.Label(ligne, text=nom_quiz, bg="#f7f8fc", fg="#252633", font=("Arial", 12, "bold"), anchor="w").pack(side="left", fill="x", expand=True)
        tk.Button(
            ligne,
            text="Voir le leaderboard",
            command=lambda q_id=id_quiz, n_quiz=nom_quiz: afficher_details_leaderboard(q_id, n_quiz),
            bg="#5356f6",
            fg="white",
            activebackground="#4245df",
            relief="flat",
            padx=14,
            pady=8,
            font=("Arial", 10, "bold"),
            cursor="hand2",
        ).pack(side="right")


page_leaderboard = tk.Frame(contenu, bg="#f7f8fc")
pages["Leaderboard"] = page_leaderboard
page_leaderboard.place(relx=0, rely=0, relwidth=1, relheight=1)

tk.Label(page_leaderboard, text="Leaderboards disponibles", bg="#f7f8fc", fg="#252633", font=("Arial", 25, "bold")).pack(anchor="w")
tk.Label(page_leaderboard, text="Choisissez le leaderboard du quiz souhaité.", bg="#f7f8fc", fg="#686a75", font=("Arial", 12)).pack(anchor="w", pady=(8, 28))

carte_leaderboard = tk.Frame(page_leaderboard, bg="white", padx=24, pady=24)
carte_leaderboard.pack(fill="x")

intro_leaderboard = tk.Frame(carte_leaderboard, bg="white")
tk.Label(intro_leaderboard, text="Tous les leaderboards", bg="white", fg="#252633", font=("Arial", 18, "bold")).pack(anchor="w")
tk.Label(intro_leaderboard, text="Sélectionnez le leaderboard à consulter", bg="white", fg="#686a75", font=("Arial", 11)).pack(anchor="w", pady=(8, 18))

zone_liste_lb = tk.Frame(intro_leaderboard, bg="white")
zone_liste_lb.pack(fill="both", expand=True)

canvas_liste_lb = tk.Canvas(zone_liste_lb, bg="white", height=340, highlightthickness=0)
barre_defilement_lb = tk.Scrollbar(zone_liste_lb, orient="vertical", command=canvas_liste_lb.yview)
canvas_liste_lb.configure(yscrollcommand=barre_defilement_lb.set)
barre_defilement_lb.pack(side="right", fill="y")
canvas_liste_lb.pack(side="left", fill="both", expand=True)

contenu_liste_lb = tk.Frame(canvas_liste_lb, bg="white")
canvas_liste_lb.create_window((0, 0), window=contenu_liste_lb, anchor="nw", tags="contenu_liste")

contenu_liste_lb.bind("<Configure>", lambda _: canvas_liste_lb.configure(scrollregion=canvas_liste_lb.bbox("all")))
canvas_liste_lb.bind("<Configure>", lambda e: canvas_liste_lb.itemconfigure("contenu_liste", width=e.width))
intro_leaderboard.pack(fill="x")


# ============================================================
# 6. DONNÉES ET CHRONOMÈTRE DU QUIZ
# ============================================================

questions = []
reponses = []
question_actuelle = 0
quiz_actuel_id = None

TEMPS_MAX_QUIZ = 3600
temps_ecoule = 0
temps_final = 0
chronometre_id = None


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
        chronometre_id = fenetre.after(1000, mettre_a_jour_chrono)
    else:
        texte_chronometre.set("⏱️ 1h max atteinte !")
        statut_quiz.set("La limite de temps d'une heure a été atteinte.")
        afficher_resultat()


def arreter_chronometre():
    global chronometre_id
    if chronometre_id is not None:
        fenetre.after_cancel(chronometre_id)
        chronometre_id = None


# ============================================================
# 7. PAGE DU QUIZ (JEU)
# ============================================================

page_quiz = tk.Frame(contenu, bg="#f7f8fc")
pages["Quiz"] = page_quiz
page_quiz.place(relx=0, rely=0, relwidth=1, relheight=1)

tk.Label(page_quiz, text="Quiz disponibles", bg="#f7f8fc", fg="#252633", font=("Arial", 25, "bold")).pack(anchor="w")
tk.Label(page_quiz, text="Choisissez un quiz pour commencer.", bg="#f7f8fc", fg="#686a75", font=("Arial", 12)).pack(anchor="w", pady=(8, 28))

carte_quiz = tk.Frame(page_quiz, bg="white", padx=24, pady=24)
carte_quiz.pack(fill="x")

intro_quiz = tk.Frame(carte_quiz, bg="white")
tk.Label(intro_quiz, text="Tous les quiz", bg="white", fg="#252633", font=("Arial", 18, "bold")).pack(anchor="w")
tk.Label(intro_quiz, text="Sélectionnez le quiz auquel vous souhaitez jouer.", bg="white", fg="#686a75", font=("Arial", 11)).pack(anchor="w", pady=(8, 18))

zone_liste_quiz = tk.Frame(intro_quiz, bg="white")
zone_liste_quiz.pack(fill="both", expand=True)

canvas_liste_quiz = tk.Canvas(zone_liste_quiz, bg="white", height=340, highlightthickness=0)
barre_defilement_quiz = tk.Scrollbar(zone_liste_quiz, orient="vertical", command=canvas_liste_quiz.yview)
canvas_liste_quiz.configure(yscrollcommand=barre_defilement_quiz.set)
barre_defilement_quiz.pack(side="right", fill="y")
canvas_liste_quiz.pack(side="left", fill="both", expand=True)

contenu_liste_quiz = tk.Frame(canvas_liste_quiz, bg="white")
canvas_liste_quiz.create_window((0, 0), window=contenu_liste_quiz, anchor="nw", tags="contenu_liste")

contenu_liste_quiz.bind("<Configure>", lambda _: canvas_liste_quiz.configure(scrollregion=canvas_liste_quiz.bbox("all")))
canvas_liste_quiz.bind("<Configure>", lambda e: canvas_liste_quiz.itemconfigure("contenu_liste", width=e.width))

# --- Zone de Questions ---
zone_questions = tk.Frame(carte_quiz, bg="white")
entete_quiz_frame = tk.Frame(zone_questions, bg="white")
entete_quiz_frame.pack(fill="x", pady=(0, 10))

progression = tk.StringVar()
tk.Label(entete_quiz_frame, textvariable=progression, bg="white", fg="#5356f6", font=("Arial", 10, "bold")).pack(side="left")

texte_chronometre = tk.StringVar()
tk.Label(entete_quiz_frame, textvariable=texte_chronometre, bg="white", fg="#686a75", font=("Arial", 10, "bold")).pack(side="right")

libelle_question = tk.Label(zone_questions, bg="white", fg="#252633", font=("Arial", 17, "bold"), wraplength=720, justify="left")
libelle_question.pack(anchor="w", pady=(14, 18))

choix_selectionne = tk.StringVar()
zone_choix = tk.Frame(zone_questions, bg="white")
zone_choix.pack(fill="x")

statut_quiz = tk.StringVar()
tk.Label(zone_questions, textvariable=statut_quiz, bg="white", fg="#b33b3b", font=("Arial", 10)).pack(anchor="w", pady=(10, 0))

navigation_quiz = tk.Frame(zone_questions, bg="white")
navigation_quiz.pack(fill="x", pady=(18, 0))

# --- Zone de Résultats ---
resultat_quiz = tk.Frame(carte_quiz, bg="white")
score_final = tk.StringVar()
tk.Label(resultat_quiz, textvariable=score_final, bg="white", fg="#252633", font=("Arial", 21, "bold")).pack(anchor="w")

temps_resultat_str = tk.StringVar()
tk.Label(resultat_quiz, textvariable=temps_resultat_str, bg="white", fg="#5356f6", font=("Arial", 12, "bold")).pack(anchor="w", pady=(4, 8))

message_resultat = tk.StringVar()
tk.Label(resultat_quiz, textvariable=message_resultat, bg="white", fg="#686a75", font=("Arial", 12)).pack(anchor="w", pady=(0, 18))

zone_boutons_resultat = tk.Frame(resultat_quiz, bg="white")
zone_boutons_resultat.pack(anchor="w")


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


def afficher_liste_quiz():
    for widget in contenu_liste_quiz.winfo_children():
        widget.destroy()

    quizs = liste_quiz()
    if not quizs:
        tk.Label(contenu_liste_quiz, text="Aucun quiz n'est disponible pour le moment.", bg="white", fg="#686a75", font=("Arial", 11)).pack(anchor="w", pady=12)
        return

    for id_quiz, chemin_quiz in quizs:
        nom_quiz = os.path.splitext(os.path.basename(os.path.normpath(chemin_quiz)))[0]
        ligne_quiz = tk.Frame(contenu_liste_quiz, bg="#f7f8fc", padx=14, pady=12)
        ligne_quiz.pack(fill="x", pady=5)

        tk.Label(ligne_quiz, text=nom_quiz, bg="#f7f8fc", fg="#252633", font=("Arial", 12, "bold"), anchor="w").pack(side="left", fill="x", expand=True)
        tk.Button(
            ligne_quiz,
            text="Commencer le quiz",
            command=lambda q_id=id_quiz, ch=chemin_quiz: lancer_quiz(q_id, ch),
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
    global questions, reponses, quiz_actuel_id

    questions_brutes, propositions, bonnes_reponses = obtenir_donnees(chemin_quiz)
    questions = [
        {"question": q, "choix": c, "reponse": r}
        for q, c, r in zip(questions_brutes, propositions, bonnes_reponses)
    ]
    if not questions:
        tk.Label(contenu_liste_quiz, text="Ce quiz ne contient aucune question.", bg="white", fg="#b33b3b", font=("Arial", 10)).pack(anchor="w", pady=6)
        return

    quiz_actuel_id = id_quiz
    commencer_quiz()


def afficher_question():
    question = questions[question_actuelle]
    progression.set(f"Question {question_actuelle + 1} sur {len(questions)}")
    libelle_question.configure(text=question["question"])
    bouton_suivant.configure(text="Terminer" if question_actuelle == len(questions) - 1 else "Suivant")
    choix_selectionne.set(reponses[question_actuelle] or "")
    statut_quiz.set("")

    for widget in zone_choix.winfo_children():
        widget.destroy()

    for choix in question["choix"]:
        tk.Button(
            zone_choix,
            text=choix,
            command=lambda r=choix: selectionner_reponse(r),
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
    demarrer_chronometre()
    afficher_question()


def afficher_resultat():
    global identifiant_bd, temps_final
    
    arreter_chronometre()
    temps_final = max(0, temps_ecoule - 1)

    mins = temps_final // 60
    secs = temps_final % 60
    temps_sql = f"{temps_final:02d}"

    temps_resultat_str.set(f"⏱️ Temps réalisé : {mins:02d} min {secs:02d} s")

    score = sum(reponse == question["reponse"] for reponse, question in zip(reponses, questions))
    
    enregistrer_partie(identifiant_bd, quiz_actuel_id, score, temps_sql)
    
    score_final.set(f"Votre score : {score} / {len(questions)}")
    message_resultat.set("Excellent travail !" if score == len(questions) else "Vous pouvez recommencer pour améliorer votre score.")

    zone_questions.pack_forget()
    resultat_quiz.pack(fill="x")


def valider_reponse():
    global question_actuelle
    reponse = choix_selectionne.get()

    if not reponse:
        statut_quiz.set("Sélectionnez une réponse pour continuer.")
        return

    reponses[question_actuelle] = reponse

    if question_actuelle == len(questions) - 1:
        afficher_resultat()
        return

    question_actuelle += 1
    afficher_question()


def question_precedente():
    global question_actuelle
    if question_actuelle > 0:
        reponses[question_actuelle] = choix_selectionne.get() or None
        question_actuelle -= 1
        afficher_question()


bouton_precedent = tk.Button(navigation_quiz, text="Précédent", command=question_precedente, bg="#eeeeef", fg="#454650", relief="flat", padx=16, pady=9, font=("Arial", 10), cursor="hand2")
bouton_precedent.pack(side="left")

bouton_suivant = tk.Button(navigation_quiz, text="Suivant", command=valider_reponse, bg="#5356f6", fg="white", activebackground="#4245df", relief="flat", padx=18, pady=9, font=("Arial", 10, "bold"), cursor="hand2")
bouton_suivant.pack(side="right")

tk.Button(zone_boutons_resultat, text="Recommencer", command=commencer_quiz, bg="#5356f6", fg="white", activebackground="#4245df", relief="flat", padx=18, pady=9, font=("Arial", 10, "bold"), cursor="hand2").pack(side="left", padx=(0, 10))
tk.Button(zone_boutons_resultat, text="Retour à la liste des quiz", command=lambda: retour_liste_quiz(), bg="#eeeeef", fg="#454650", activebackground="#d5d5d9", relief="flat", padx=18, pady=9, font=("Arial", 10), cursor="hand2").pack(side="left")

intro_quiz.pack(fill="x")


def retour_liste_quiz():
    arreter_chronometre()
    zone_questions.pack_forget()
    resultat_quiz.pack_forget()
    intro_quiz.pack(fill="x")
    afficher_liste_quiz()


# ============================================================
# 8. MODULE DE CRÉATION DE QUIZ (ADMINISTRATEUR)
# ============================================================

def afficher_creation_quiz(parent, page_suivante, etat_quiz):
    tk.Label(parent, text="Nom du quiz", bg="white", fg="#454650", font=("Arial", 11)).pack(anchor="w", pady=(12, 6))

    nom_quiz = tk.StringVar()
    statut_q = tk.StringVar()
    ligne_titre = tk.Frame(parent, bg="white")
    ligne_titre.pack(fill="x")

    tk.Entry(ligne_titre, textvariable=nom_quiz, font=("Arial", 12)).pack(side="left", fill="x", expand=True, ipady=6)

    def afficher_etape_suivante():
        if not nom_quiz.get().strip():
            statut_q.set("Saisissez le nom du quiz avant de continuer.")
            return
        creer_fichier(nom_quiz.get().strip())
        etat_quiz["nomQuiz"] = nom_quiz.get().strip()
        statut_q.set("")
        page_suivante.tkraise()

    tk.Button(ligne_titre, text="Suivant", command=afficher_etape_suivante, cursor="hand2").pack(side="left", padx=(12, 0), ipady=4)
    tk.Label(parent, textvariable=statut_q, bg="white", fg="#b00020", font=("Arial", 10)).pack(anchor="w", pady=(8, 0))
    return nom_quiz


def afficher_etape_nombre_questions(parent, etat_quiz, page_titre, page_questions):
    tk.Label(parent, text="Combien de questions voulez-vous dans votre quiz ?", bg="#f7f8fc", fg="#252633", font=("Arial", 16, "bold")).pack(anchor="w", pady=(24, 12))

    nombre_saisi = tk.StringVar()
    statut = tk.StringVar()

    tk.Entry(parent, textvariable=nombre_saisi, font=("Arial", 12)).pack(anchor="w", fill="x", ipady=6)
    tk.Label(parent, textvariable=statut, bg="#f7f8fc", fg="#b00020", font=("Arial", 10)).pack(anchor="w", pady=(8, 0))

    def valider_nombre():
        valeur = nombre_saisi.get().strip()
        if not valeur.isdecimal():
            statut.set("Saisissez un nombre entier entre 1 et 50.")
            return

        nombre = int(valeur)
        if not 1 <= nombre <= 50:
            statut.set("Le nombre de questions doit être compris entre 1 et 50.")
            return

        etat_quiz["nbQuestions"] = nombre
        etat_quiz["questionActuelle"] = 1
        etat_quiz["questions"].clear()
        statut.set("")
        page_questions.charger_question()
        page_questions.tkraise()

    nav = tk.Frame(parent, bg="#f7f8fc")
    nav.pack(side="bottom", fill="x", pady=20)
    tk.Button(nav, text="Retour", command=page_titre.tkraise, cursor="hand2").pack(side="left")
    tk.Button(nav, text="Suivant", command=valider_nombre, cursor="hand2").pack(side="right")


def afficher_etape_saisie_questions(parent, etat_quiz, page_nombre, page_recap):
    tk.Label(parent, text="Saisie des questions", bg="#f7f8fc", fg="#252633", font=("Arial", 25, "bold")).pack(anchor="w")

    progression_q = tk.StringVar()
    tk.Label(parent, textvariable=progression_q, bg="#f7f8fc", fg="#686a75", font=("Arial", 12)).pack(anchor="w", pady=(8, 20))

    formulaire = tk.Frame(parent, bg="white", padx=24, pady=24)
    formulaire.pack(fill="both", expand=True)

    tk.Label(formulaire, text="Énoncé de la question", bg="white", fg="#454650", font=("Arial", 11)).pack(anchor="w")
    enonce = tk.StringVar()
    tk.Entry(formulaire, textvariable=enonce, font=("Arial", 12)).pack(fill="x", ipady=6, pady=(6, 18))

    tk.Label(formulaire, text="Réponses possibles (sélectionnez la bonne réponse)", bg="white", fg="#454650", font=("Arial", 11)).pack(anchor="w", pady=(0, 8))

    lignes_reponses = tk.Frame(formulaire, bg="white")
    lignes_reponses.pack(fill="x")
    variables_reponses = []
    bonne_reponse = tk.IntVar(value=-1)
    statut = tk.StringVar()

    def afficher_lignes_reponses():
        for widget in lignes_reponses.winfo_children():
            widget.destroy()

        for index, variable in enumerate(variables_reponses):
            ligne = tk.Frame(lignes_reponses, bg="white")
            ligne.pack(fill="x", pady=3)
            tk.Entry(ligne, textvariable=variable, font=("Arial", 11)).pack(side="left", fill="x", expand=True, ipady=4)
            tk.Radiobutton(ligne, text="Bonne réponse", variable=bonne_reponse, value=index, bg="white", activebackground="white").pack(side="left", padx=8)
            tk.Button(ligne, text="Supprimer", command=lambda i=index: supprimer_reponse(i), cursor="hand2").pack(side="left")

    def ajouter_reponse():
        variables_reponses.append(tk.StringVar())
        afficher_lignes_reponses()

    def supprimer_reponse(index):
        if len(variables_reponses) <= 2:
            statut.set("Une question doit proposer au moins deux réponses.")
            return

        variables_reponses.pop(index)
        if bonne_reponse.get() == index:
            bonne_reponse.set(-1)
        elif bonne_reponse.get() > index:
            bonne_reponse.set(bonne_reponse.get() - 1)
        afficher_lignes_reponses()
        statut.set("")

    for _ in range(4):
        variables_reponses.append(tk.StringVar())
    afficher_lignes_reponses()

    tk.Button(formulaire, text="Ajouter une réponse", command=ajouter_reponse, cursor="hand2").pack(anchor="w", pady=(8, 0))
    tk.Label(formulaire, textvariable=statut, bg="white", fg="#b00020", font=("Arial", 10)).pack(anchor="w", pady=(12, 0))

    def charger_question():
        progression_q.set(f"Question {etat_quiz['questionActuelle']} / {etat_quiz['nbQuestions']}")
        enonce.set("")
        variables_reponses.clear()
        variables_reponses.extend(tk.StringVar() for _ in range(4))
        bonne_reponse.set(-1)
        statut.set("")
        afficher_lignes_reponses()

        btn_suiv.configure(text="Terminer" if etat_quiz["questionActuelle"] == etat_quiz["nbQuestions"] else "Suivant")

    def valider_question():
        texte_enonce = enonce.get().strip()
        reponses_saisies = [v.get().strip() for v in variables_reponses]
        index_correct = bonne_reponse.get()

        if not texte_enonce:
            statut.set("Saisissez l'énoncé de la question.")
            return

        if sum(bool(r) for r in reponses_saisies) < 2:
            statut.set("Saisissez au moins deux réponses non vides.")
            return

        if index_correct < 0 or index_correct >= len(reponses_saisies) or not reponses_saisies[index_correct]:
            statut.set("Sélectionnez une bonne réponse non vide.")
            return

        reps = [r for r in reponses_saisies if r]
        bonne_reponse_index = sum(bool(r) for r in reponses_saisies[:index_correct])

        try:
            ajout_question(etat_quiz["nomQuiz"], texte_enonce, reps, reps[bonne_reponse_index])
        except OSError as erreur:
            statut.set(f"Impossible d'enregistrer la question : {erreur}")
            return

        etat_quiz["questions"].append({
            "enonce": texte_enonce,
            "reponses": reps,
            "bonneReponse": bonne_reponse_index,
        })

        if etat_quiz["questionActuelle"] == etat_quiz["nbQuestions"]:
            etat_quiz["questionActuelle"] += 1
            page_recap.actualiser_recapitulatif()
            page_recap.tkraise()
            page_recap.enregistrer_quiz()
            return

        etat_quiz["questionActuelle"] += 1
        charger_question()

    nav = tk.Frame(parent, bg="#f7f8fc")
    nav.pack(side="bottom", fill="x", pady=20)
    tk.Button(nav, text="Retour", command=page_nombre.tkraise, cursor="hand2").pack(side="left")
    btn_suiv = tk.Button(nav, text="Suivant", command=valider_question, cursor="hand2")
    btn_suiv.pack(side="right")
    parent.charger_question = charger_question


def afficher_etape_recapitulatif(parent, etat_quiz):
    tk.Label(parent, text="Quiz terminé", bg="#f7f8fc", fg="#252633", font=("Arial", 25, "bold")).pack(anchor="w")

    recapitulatif = tk.StringVar()
    tk.Label(parent, textvariable=recapitulatif, justify="left", anchor="nw", bg="white", fg="#454650", font=("Arial", 12), padx=24, pady=24).pack(fill="both", expand=True, pady=(20, 0))

    def actualiser_recapitulatif():
        lignes = [f"Quiz : {etat_quiz['nomQuiz']}", f"Nombre de questions : {len(etat_quiz['questions'])}", ""]
        for numero, q in enumerate(etat_quiz["questions"], start=1):
            lignes.append(f"{numero}. {q['enonce']}")
            for index, rep in enumerate(q["reponses"]):
                marque = " (bonne réponse)" if index == q["bonneReponse"] else ""
                lignes.append(f"   - {rep}{marque}")
            lignes.append("")
        recapitulatif.set("\n".join(lignes))

    nav = tk.Frame(parent, bg="#f7f8fc")
    nav.pack(side="bottom", fill="x", pady=20)

    statut_enregistrement = tk.StringVar()
    tk.Label(nav, textvariable=statut_enregistrement, bg="#f7f8fc", fg="#b00020", font=("Arial", 10)).pack(side="left")

    def enregistrer_quiz():
        try:
            succes = ajouter_quiz_depuis_fichier(os.path.join("Quiz", etat_quiz["nomQuiz"]))
        except (OSError, sqlite3.Error) as erreur:
            statut_enregistrement.set(f"Échec de l'enregistrement : {erreur}")
            bouton_reessayer.pack(side="left", padx=8)
            return

        if not succes:
            statut_enregistrement.set("Fichier du quiz introuvable ; vérifiez son emplacement.")
            bouton_reessayer.pack(side="left", padx=8)
            return

        statut_enregistrement.set("")
        bouton_reessayer.pack_forget()

    bouton_reessayer = tk.Button(nav, text="Réessayer", command=enregistrer_quiz, cursor="hand2")
    tk.Button(nav, text="Accueil", command=lambda: afficher_page("Accueil"), cursor="hand2").pack(side="right")
    parent.actualiser_recapitulatif = actualiser_recapitulatif
    parent.enregistrer_quiz = enregistrer_quiz


# ============================================================
# 9. PAGES CONNEXION ET COMPTE
# ============================================================

page_connexion = tk.Frame(contenu, bg="#f7f8fc")
page_connexion.place(relx=0, rely=0, relwidth=1, relheight=1)
pages["Connexion"] = page_connexion

page_compte = tk.Frame(contenu, bg="#f7f8fc")
page_compte.place(relx=0, rely=0, relwidth=1, relheight=1)
pages["Compte"] = page_compte

# --- Contenu Page Compte ---
tk.Label(page_compte, text="Mon compte", bg="#f7f8fc", fg="#252633", font=("Arial", 25, "bold")).pack(anchor="w")
identite_compte = tk.StringVar()
tk.Label(page_compte, textvariable=identite_compte, bg="#f7f8fc", fg="#686a75", font=("Arial", 12)).pack(anchor="w", pady=(12, 0))
tk.Button(page_compte, text="Se déconnecter", command=se_deconnecter, bg="#eeeeef", fg="#454650", relief="flat", padx=16, pady=9, font=("Arial", 10), cursor="hand2").pack(anchor="w", pady=(20, 0))

# --- Contenu Page Connexion ---
tk.Label(page_connexion, text="Bienvenue sur SQuizi !", bg="#f7f8fc", fg="#252633", font=("Arial", 25, "bold")).pack(anchor="w")
tk.Label(page_connexion, text="Connectez-vous ou créez un compte pour accéder à SQuizi.", bg="#f7f8fc", fg="#686a75", font=("Arial", 12)).pack(anchor="w", pady=(8, 24))

carte_connexion = tk.Frame(page_connexion, bg="white", padx=28, pady=24)
carte_connexion.pack(fill="x")

mode_connexion = tk.StringVar(value="Connexion")
identifiant = tk.StringVar()
identifiant_bd = ""
mot_de_passe = tk.StringVar()
statut_auth = tk.StringVar()

tk.Label(carte_connexion, textvariable=mode_connexion, bg="white", fg="#252633", font=("Arial", 18, "bold")).pack(anchor="w", pady=(0, 18))

champ_nom = tk.Frame(carte_connexion, bg="white")
tk.Label(champ_nom, text="Nom", bg="white", fg="#454650", font=("Arial", 11)).pack(anchor="w", pady=(0, 6))
tk.Entry(champ_nom, font=("Arial", 12)).pack(fill="x", ipady=6)

tk.Label(carte_connexion, text="Identifiant", bg="white", fg="#454650", font=("Arial", 11)).pack(anchor="w", pady=(12, 6))
tk.Entry(carte_connexion, textvariable=identifiant, font=("Arial", 12)).pack(fill="x", ipady=6)

tk.Label(carte_connexion, text="Mot de passe", bg="white", fg="#454650", font=("Arial", 11)).pack(anchor="w", pady=(12, 6))
tk.Entry(carte_connexion, textvariable=mot_de_passe, show="*", font=("Arial", 12)).pack(fill="x", ipady=6)

bouton_action = tk.Button(carte_connexion, bg="#5356f6", fg="white", activebackground="#4245df", activeforeground="white", relief="flat", borderwidth=0, padx=18, pady=10, font=("Arial", 11, "bold"), cursor="hand2")
bouton_action.pack(anchor="w", pady=(20, 12))

tk.Label(carte_connexion, textvariable=statut_auth, bg="white", fg="#686a75", font=("Arial", 10), wraplength=650).pack(anchor="w")

bouton_changer_mode = tk.Button(carte_connexion, bg="white", fg="#5356f6", activebackground="white", activeforeground="#4245df", relief="flat", borderwidth=0, font=("Arial", 10), cursor="hand2")
bouton_changer_mode.pack(anchor="w", pady=(12, 0))


def changer_mode_auth():
    if mode_connexion.get() == "Connexion":
        nouveau_mode = "Créer mon compte"
    else:
        nouveau_mode = "Connexion"

    mode_connexion.set(nouveau_mode)
    statut_auth.set("")

    if nouveau_mode == "Créer mon compte":
        champ_nom.pack(fill="x", before=carte_connexion.winfo_children()[1])
        bouton_action.configure(text="Créer mon compte")
        bouton_changer_mode.configure(text="Déjà un compte ? Se connecter")
    else:
        champ_nom.pack_forget()
        bouton_action.configure(text="Se connecter")
        bouton_changer_mode.configure(text="Pas encore de compte ? Créer un compte")


def envoyer_formulaire_auth():
    global connecte, page_actuelle, identifiant_bd, admin

    champs_requis = [identifiant.get().strip(), mot_de_passe.get()]
    identifiant_creer = champs_requis[0]
    mdp_creer = champs_requis[1]
    identifiant_bd = champs_requis[0]

    if mode_connexion.get() == "Créer mon compte":
        if not all(champs_requis):
            statut_auth.set("Merci de remplir tous les champs.")
            return

        if not creer_compte(identifiant_creer, mdp_creer):
            statut_auth.set("L'identifiant existe déjà")
            return
        admin = 0
    else:
        if not all(champs_requis):
            statut_auth.set("Merci de remplir tous les champs.")
            return

        verif = verifier_connexion(identifiant_creer, mdp_creer)
        if not verif[0]:
            statut_auth.set("Mot de passe ou identifiant incorrect")
            return
        else:
            admin = verif[1]

    connecte = True

    # Mise à jour dynamique de la barre supérieure selon le rôle
    mettre_a_jour_barre_navigation()
    bande_haut.pack(fill="x", before=contenu)

    page_actuelle = None
    titre_accueil = tk.StringVar(value=f"Bienvenue sur SQuizi, {identifiant.get().strip()} !")
    identite_compte.set(f"Identifiant connecté : {identifiant_bd}\nStatut : {'Administrateur' if admin == 1 else 'Utilisateur'}")

    historique = obtenir_historique(identifiant_bd)
    historique_afficher = "".join([f"{k}\n\n" for k in historique]) or "Aucune activité enregistrée."

    # --- Initialisation des pages dynamiques post-connexion ---
    tuple_pages = [
        ("Accueil", "Bienvenue sur SQuizi !", "Votre espace pour apprendre en vous amusant.", "Prêt à commencer un quiz ?"),
        ("Mes activités", "Mes activités", "Retrouvez ici votre progression et vos résultats.", historique_afficher),
    ]

    if admin == 1:
        tuple_pages.append(("Créer un quiz", "Création de quiz", "Créez un quiz pour vos utilisateurs.", ""))

    for nom_page, titre, description, message in tuple_pages:
        page = tk.Frame(contenu, bg="#f7f8fc")

        if nom_page == "Accueil":
            tk.Label(page, textvariable=titre_accueil, bg="#f7f8fc", fg="#252633", font=("Arial", 25, "bold")).pack(anchor="w")
        else:
            tk.Label(page, text=titre, bg="#f7f8fc", fg="#252633", font=("Arial", 25, "bold")).pack(anchor="w")

        tk.Label(page, text=description, bg="#f7f8fc", fg="#686a75", font=("Arial", 12)).pack(anchor="w", pady=(8, 28))

        carte = tk.Frame(page, bg="white", padx=24, pady=24)
        carte.pack(fill="x")

        if message:
            tk.Label(carte, text=message, bg="white", fg="#686a75", font=("Arial", 12), justify="left").pack(anchor="w")

        if nom_page == "Créer un quiz":
            etat_quiz = {
                "nomQuiz": "",
                "nbQuestions": 0,
                "questionActuelle": 1,
                "questions": [],
            }
            page.etat_quiz = etat_quiz

            page_nombre = tk.Frame(contenu, bg="#f7f8fc")
            page_questions = tk.Frame(contenu, bg="#f7f8fc")
            page_recap = tk.Frame(contenu, bg="#f7f8fc")

            afficher_etape_nombre_questions(page_nombre, etat_quiz, page, page_questions)
            afficher_etape_saisie_questions(page_questions, etat_quiz, page_nombre, page_recap)
            afficher_etape_recapitulatif(page_recap, etat_quiz)

            for page_etape in (page_nombre, page_questions, page_recap):
                page_etape.place(relx=0, rely=0, relwidth=1, relheight=1)

            page.nom_quiz = afficher_creation_quiz(carte, page_nombre, etat_quiz)

        pages[nom_page] = page
        page.place(relx=0, rely=0, relwidth=1, relheight=1)

    afficher_page("Accueil")


# ============================================================
# 10. LANCEMENT DE L'APPLICATION
# ============================================================

bouton_action.configure(text="Se connecter", command=envoyer_formulaire_auth)
bouton_changer_mode.configure(text="Pas encore de compte ? Créer un compte", command=changer_mode_auth)

bande_haut.pack_forget()
pages["Connexion"].tkraise()

fenetre.mainloop()