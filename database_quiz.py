import sqlite3
from hashlib import sha512
from datetime import datetime
import os

connexion = sqlite3.connect("quiz_database.db")
curseur = connexion.cursor()

curseur.execute("PRAGMA foreign_keys = ON;")

curseur.execute("""
CREATE TABLE IF NOT EXISTS Compte (
    identifiant TEXT PRIMARY KEY,
    mdp TEXT NOT NULL,
    hscore INTEGER DEFAULT 0,
    admin INTEGER DEFAULT 0
)
""")

curseur.execute("""
CREATE TABLE IF NOT EXISTS Quiz (
    id_quiz INTEGER PRIMARY KEY AUTOINCREMENT,
    fiche_quiz TEXT NOT NULL
)
""")

curseur.execute("""
CREATE TABLE IF NOT EXISTS Historique (
    id_hist INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL,
    date TEXT NOT NULL,
    heure TEXT NOT NULL,
    chronometre TEXT,
    identifiant TEXT,
    id_quiz INTEGER,
    FOREIGN KEY (identifiant) REFERENCES Compte(identifiant) ON DELETE CASCADE,
    FOREIGN KEY (id_quiz) REFERENCES Quiz(id_quiz) ON DELETE CASCADE
)
""")


connexion.commit()
connexion.close()

print("Base de données et tables créées avec succès !")
    

# FONCTIONS de création de compte et login

def hachage(mdp):
  """Fonction pour hacher un mot de passe avec SHA-512"""
  mdp_encode = mdp.encode()
  return sha512(mdp_encode).hexdigest()


def creer_compte(identifiant, mdp_en_clair):
  """Fonction pour hacher le mot de passe et l'insérer dans la base"""
  mdp_securise = hachage(mdp_en_clair)

  connexion = sqlite3.connect("quiz_database.db")
  curseur = connexion.cursor()

  try:
    curseur.execute(
        """
        INSERT INTO Compte (identifiant, mdp, hscore, admin)
        VALUES (?, ?, 0, 0)
        """,
        (identifiant, mdp_securise),
    )
    connexion.commit()
    print(f"Compte de '{identifiant}' créé avec succès !")
    res=True
  except sqlite3.IntegrityError:
    print(
        f"Erreur : L'identifiant '{identifiant}' existe déjà dans la base de"
        " données."
    )
    res=False
  finally:
    connexion.close()
    return res


def verifier_connexion(identifiant, mdp_en_clair):
    "Fonction pour se connecter"
    "On hache le mdp taper par l'utilisateur"
    connexion = sqlite3.connect("quiz_database.db")
    curseur = connexion.cursor()

    # Rechercher le compte par son identifiant
    curseur.execute(
        "SELECT mdp, admin FROM Compte WHERE identifiant = ?", (identifiant,)
    )
    resultat = curseur.fetchone()
    connexion.close()

    if resultat:
        mdp_stocke, admin_statut = resultat
    # On hache le mot de passe entré pour le comparer à celui stocké
        if hachage(mdp_en_clair) == mdp_stocke:
            print(f"Connexion réussie ! Bienvenue {identifiant}.")
            return True, admin_statut  # Renvoie True et le statut (admin ou non)
        else:
            print("Erreur : Mot de passe incorrect.")
            return False, None
    else:
        print(f"Erreur : L'identifiant '{identifiant}' n'existe pas.")
        return False, None

def enregistrer_partie(identifiant, id_quiz, score, chronometre):
  """Enregistre le score dans l'historique et met à jour le hscore si besoin."""
  connexion = sqlite3.connect("quiz_database.db")
  curseur = connexion.cursor()

  # Récupérer la date et l'heure actuelles automatiquement
  maintenant = datetime.now()
  date_jour = maintenant.strftime("%Y-%m-%d")
  heure_actuelle = maintenant.strftime("%H:%M:%S")

  # 1. Insertion dans la table Historique
  curseur.execute(
      """
        INSERT INTO Historique (score, date, heure, chronometre, identifiant, id_quiz)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
      (score, date_jour, heure_actuelle, chronometre, identifiant, id_quiz),
  )

  # 2. Vérifier et mettre à jour le meilleur score (hscore) de l'utilisateur
  curseur.execute(
      "SELECT hscore FROM Compte WHERE identifiant = ?", (identifiant,)
  )
  ancien_hscore = curseur.fetchone()[0]

  if score > ancien_hscore:
    curseur.execute(
        "UPDATE Compte SET hscore = ? WHERE identifiant = ?",
        (score, identifiant),
    )
    print(
        f"🏆 Nouveau record personnel ! Votre meilleur score passe à {score}."
    )

  connexion.commit()
  print("Partie enregistrée dans l'historique avec succès.")   

def supprimer_quiz(id_ou_nom):
    """Fonction pour supprimer un quiz de la base de données par son ID ou son nom."""
    connexion = sqlite3.connect("quiz_database.db")
    curseur = connexion.cursor()

    if str(id_ou_nom).isdigit():
        curseur.execute("DELETE FROM Quiz WHERE id_quiz = ?", (int(id_ou_nom),))
    else:
        recherche_titre = f"TITRE:{id_ou_nom}"
        curseur.execute("DELETE FROM Quiz WHERE fiche_quiz LIKE ?", (f"%{recherche_titre}%",))

    if curseur.rowcount > 0:
        print(f"Le quiz '{id_ou_nom}' a été supprimé avec succès !")
    else:
        print(f"Aucun quiz trouvé avec l'identifiant ou le nom '{id_ou_nom}'.")

    connexion.commit()
    connexion.close()

def ajouter_quiz_depuis_fichier(chemin_fichier):
    """Fonction pour lire un fichier texte de quiz et l'insérer dans la base de données."""
    try:
        nom_quiz = os.path.splitext(os.path.basename(chemin_fichier))[0]

        with open(chemin_fichier, "r", encoding="utf-8") as fichier:
            contenu_texte = fichier.read()
            
        connexion = sqlite3.connect("quiz_database.db")
        curseur = connexion.cursor()


        curseur.execute(
            """
            INSERT INTO Quiz (fiche_quiz)
            VALUES (?)
            """,
            (chemin_fichier,),
        )
        
        connexion.commit()
        connexion.close()
        print(f"Quiz '{nom_quiz}' ajouté avec succès !")
        
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{chemin_fichier}' est introuvable.")

def liste_quiz():
  """Affiche la liste des quizs."""
  connexion = sqlite3.connect("quiz_database.db")
  curseur = connexion.cursor()

  curseur.execute("SELECT id_quiz, fiche_quiz FROM Quiz")
  quizs = curseur.fetchall()
    
  connexion.close()

  if quizs:
      print("\n--- LISTE DES QUIZS DISPONIBLES ---")
      for q in quizs:
          id_q = q[0]
          chemin_quiz = q[1]  # Contient le chemin (ex: "fichier.txt")
          
          # On extrait le nom du fichier sans l'extension
          nom_quiz = chemin_quiz.split("/")[-1]
                
          print(f"ID Quiz : {id_q} | Nom du Quiz : {nom_quiz}")
  else:
     print("\n[Info] Aucun quiz n'est enregistré dans la base de données pour l'instant.")

  return quizs

def liste_nom_quiz():
  """Affiche la liste des quizs."""
  connexion = sqlite3.connect("quiz_database.db")
  curseur = connexion.cursor()

  curseur.execute("SELECT id_quiz, fiche_quiz FROM Quiz")
  quizs = curseur.fetchall()
  liste_nom_quiz=[]
  connexion.close()

  if quizs:
      for q in quizs:
          id_q = q[0]
          chemin_quiz = q[1]  # Contient le chemin (ex: "fichier.txt")
          
          # On extrait le nom du fichier sans l'extension
          nom_quiz = chemin_quiz.split("/")[-1]
          liste_nom_quiz.append(nom_quiz)

  return liste_nom_quiz
print(liste_nom_quiz())


def afficher_tous_les_comptes():
    connexion = sqlite3.connect("quiz_database.db")
    curseur = connexion.cursor()

    curseur.execute(
        "SELECT identifiant, hscore, admin, substr(mdp, 1, 12) FROM Compte"
    )
    comptes = curseur.fetchall()
    connexion.close()

    return [c[0] for c in comptes]

def ajouter_historique(identifiant, id_quiz, score):
    """Ajoute une entrée dans l'historique avec le score, la date et l'heure actuelles."""
    connexion = sqlite3.connect("quiz_database.db") 
    curseur = connexion.cursor()

    maintenant = datetime.now()
    date_jour = maintenant.strftime("%Y-%m-%d")
    heure_actuelle = maintenant.strftime("%H:%M:%S")

    curseur.execute(
        """
        INSERT INTO Historique (score, date, heure, identifiant, id_quiz)
        VALUES (?, ?, ?, ?, ?)
        """,
        (score, date_jour, heure_actuelle, identifiant, id_quiz),
    )
    curseur.execute(
        "SELECT hscore FROM Compte WHERE identifiant = ?", (identifiant,)
    )
    resultat = curseur.fetchone()
    if resultat:
        ancien_hscore = resultat[0]
        if score > ancien_hscore:
            curseur.execute(
                "UPDATE Compte SET hscore = ? WHERE identifiant = ?",
                (score, identifiant),
            )

    connexion.commit()
    connexion.close()
    print("Partie enregistrée dans l'historique avec succès !")

def obtenir_historique(identifiant):
    """Récupère l'historique et renvoie chaque ligne sous forme de chaîne de caractères formatée."""
    connexion = sqlite3.connect("quiz_database.db")
    curseur = connexion.cursor()

    curseur.execute(
        """
        SELECT h.id_hist, h.score, h.date, h.heure, h.chronometre, h.id_quiz , Quiz.fiche_quiz
        FROM Historique h
        JOIN Quiz ON h.id_quiz = Quiz.id_quiz
        WHERE h.identifiant = ?
        ORDER BY h.date DESC, h.heure DESC

        """,
        (identifiant,),
    )
    
    historique_utilisateur = curseur.fetchall()
    connexion.close()

    liste_chaines = []
    
    for h in historique_utilisateur:
        id_hist, score, date, heure, chronometre, id_quiz, fiche_quiz = h
        nom_quiz = fiche_quiz.split("/")[-1]
        mins = chronometre // 60
        secs = chronometre % 60
        texte_partie = f'Quiz : {nom_quiz} | le score est de {score} en {mins:02d}min{secs:02d}s secondes réalisé à {heure} le {date}'
        liste_chaines.append(texte_partie)

    return liste_chaines

def obtenir_leaderboard_quiz(id_quiz):
    """Récupère les scores enregistrés pour un quiz donné, du plus grand au plus petit."""
    connexion = sqlite3.connect("quiz_database.db")
    curseur = connexion.cursor()

    curseur.execute(
        """
        SELECT Compte.identifiant, Historique.score, Historique.chronometre, Historique.date
        FROM Historique
        JOIN Compte ON Historique.identifiant = Compte.identifiant
        WHERE Historique.id_quiz = ?
        ORDER BY Historique.score DESC, Historique.chronometre ASC
        """,
        (id_quiz,),
    )
    resultats = curseur.fetchall()
    connexion.close()
    return resultats
   

def menu_console():
  while True:
    print("\n==============================")
    print("      APPLICATION QUIZ        ")
    print("==============================")
    print("1. Créer un compte")
    print("2. Se connecter")
    print("3. Afficher la liste des identifiants")
    print("4. Ajouter un quiz")
    print("5. Afficher la liste des quiz")
    print("6. Supprimer un quiz")
    print("7. Quitter")

    choix = input("Votre choix (1, 2, 3, 4, 5, 6 ou 7) : ")

    if choix == "1":
      print("\n--- INSCRIPTION ---")
      identifiant = input("Choisissez un identifiant : ")
      mdp = input("Choisissez un mot de passe : ")
      creer_compte(identifiant, mdp)

    elif choix == "2":
      print("\n--- CONNEXION ---")
      identifiant = input("Identifiant : ")
      mdp = input("Mot de passe : ")

      # On appelle votre fonction de vérification
      connecte, admin = verifier_connexion(identifiant, mdp)

      if connecte:
        print(f"\n[Succès] Bienvenue {identifiant} !")
        if admin == 1:
          print("-> Vous êtes connecté en tant qu'Administrateur.")
          
        else:
          print("-> Vous êtes connecté en tant qu'Utilisateur classique.")
          

    elif choix == "3":
      connexion_temp = sqlite3.connect("quiz_database.db")
      curseur_temp = connexion_temp.cursor()

      curseur_temp.execute("SELECT identifiant FROM Compte")
      utilisateurs = curseur_temp.fetchall() 
      connexion_temp.close()

      print(f"\nVoici la liste des identifiants : {utilisateurs}")

    elif choix == "4":
      print("\n--- AJOUTER UN QUIZ DEPUIS UN FICHIER ---")
      nom_fichier = input("Entrez le nom du fichier texte (ex: fichier.txt) : ")
      ajouter_quiz_depuis_fichier(nom_fichier)

    elif choix == "5":
      liste_quiz()

    elif choix == "6":
      print("\n--- SUPPRIMER UN QUIZ ---")
      liste_quiz()
      valeur = input("Entrez l'ID du quiz ou son nom (ex: fichier) à supprimer : ")
      supprimer_quiz(valeur)

    elif choix == "7":
      print("\nFermeture du programme. Au revoir !")
      break

    else:
      print("\n[Erreur] Choix invalide, veuillez choisir entre 1, 2, 3, 4, 5, 6 et 7.")

#connexion = sqlite3.connect("quiz_database.db")
#curseur = connexion.cursor() 
#curseur.execute(
#     """UPDATE Historique SET chronometre = 120 WHERE chronometre IS NULL;""",
#)
#connexion.commit()
#connexion.close()
      



