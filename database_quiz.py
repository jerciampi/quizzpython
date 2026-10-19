import sqlite3
from hashlib import sha512
import datetime


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
  except sqlite3.IntegrityError:
    print(
        f"Erreur : L'identifiant '{identifiant}' existe déjà dans la base de"
        " données."
    )
  finally:
    connexion.close()


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

def enregistrer_partie(identifiant, id_quiz, score):
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
        INSERT INTO Historique (score, date, heure, identifiant, id_quiz)
        VALUES (?, ?, ?, ?, ?)
    """,
      (score, date_jour, heure_actuelle, identifiant, id_quiz),
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

def menu_console():
  while True:
    print("\n==============================")
    print("      APPLICATION QUIZ        ")
    print("==============================")
    print("1. Créer un compte")
    print("2. Se connecter")
    print("3. Afficher la liste des identifiants")
    print("4. Quitter")

    choix = input("Votre choix (1, 2, 3 ou 4) : ")

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
          # TODO: Appeler ici le menu de création de quiz plus tard
        else:
          print("-> Vous êtes connecté en tant qu'Utilisateur classique.")
          # TODO: Appeler ici le menu pour jouer à un quiz plus tard

    elif choix == "3":
      connexion_temp = sqlite3.connect("quiz_database.db")
      curseur_temp = connexion_temp.cursor()
      
      curseur_temp.execute("SELECT identifiant FROM Compte")
      #fetchall() permet de récupérer tous les résultats sous forme de liste
      utilisateurs = curseur_temp.fetchall() 
      connexion_temp.close()
      
      print(f"\nVoici la liste des identifiants : {utilisateurs}")

    elif choix == "4":
      print("\nFermeture du programme. Au revoir !")
      break

    else:
      print("\n[Erreur] Choix invalide, veuillez choisir entre 1, 2, 3 et 4.")

menu_console()
