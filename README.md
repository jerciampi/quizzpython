# Squizi

**Squizi** est une application de quiz développée en Python dans le cadre du module **PROJ531** (Gestion de projet informatique). Elle permet aux utilisateurs de créer un compte pour jouer à des quiz chronométrés et suivre leurs scores, tout en donnant aux administrateurs la possibilité d'ajouter et de gérer les questionnaires.

## Fonctionnalités

### Espace Joueur
* **Compte utilisateur :** Inscription et connexion sécurisée (mots de passe hachés).
* **Jeu :** Choix d'un quiz dans la liste disponible, chronomètre pendant la partie, calcul du score final et affichage des bonnes réponses.
* **Suivi :** Consultation de l'historique personnel (scores, dates, temps réalisés) et accès au classement général (*Leaderboard*).

### Espace Administrateur
* **Création de quiz :** Ajout d'un nouveau quiz directement depuis l'interface graphique ou par importation d'un fichier texte (`.txt`).
* **Gestion :** Affichage de la liste des quiz enregistrés et suppression de quiz.

## Installation et prérequis

L'application fonctionne avec **Python 3** et utilise principalement des modules inclus de base (`tkinter` pour l'interface graphique, `sqlite3` pour la base de données, `datetime`).

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/jerciampi/quizzpython.git
   cd quizzpython
   ```

2. **Installer les dépendances (si besoin) :**
   Si la bibliothèque `Pillow` est requise pour l'affichage du logo dans l'interface, installez-la via :
   ```bash
   pip install pillow
   ```
   *(Sur certaines distributions Linux, le paquet `python3-tk` peut aussi être nécessaire.)*

## Comment ça marche ?

1. **Lancer l'application :**
   Exécutez le fichier `interface.py` depuis le dossier du projet :
   ```bash
   python interface.py
   ```
   *(ou `python3 interface.py` selon votre installation)*

2. **Créer un compte et se connecter :**
   * Au démarrage, passez par l'écran d'inscription pour créer votre compte (ou connectez-vous si vous en avez déjà un) afin d'accéder aux quiz.

3. **Jouer ou administrer :**
   * **En tant que joueur :** Sélectionnez un quiz pour lancer la partie, répondez aux questions puis consultez votre résultat, votre historique ou le classement.
   * **En tant qu'administrateur :** Vous disposez d'un accès dédié dans l'interface pour créer et ajouter de nouveaux quiz dans la base de données.

## Structure du dépôt

* `interface.py` : Point d'entrée principal de l'application (interface graphique Tkinter).
* `database_quiz.py` : Gestion de la base de données SQLite (utilisateurs, quiz, historique).
* Documents et comptes-rendus d'avancement réalisés lors des séances de TP.

## Auteurs

Projet réalisé par Hugo Holdrinet, Bastien Cheneval, Alban Stora, Antoine Cizere, Jeremy Ciampi dans le cadre de l'UE PROJ531.
