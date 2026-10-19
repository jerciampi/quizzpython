
import sqlite3


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
    