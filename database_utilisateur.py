import hashlib
import sqlite3

connection = sqlite3.connect("test.db")
print(connection.total_changes)
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS exemple (id INTEGER, nom TEXT, age INTEGER)")
cursor.execute("INSERT INTO exemple VALUES (1, 'alice', 20)")
cursor.execute("INSERT INTO exemple VALUES (2, 'bob', 30)")
cursor.execute("INSERT INTO exemple VALUES (3, 'eve', 40)")


connection.commit()


def hash_password(password: str) -> str:
    """Transforme le mot de passe en clair en empreinte SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_utilisateur(username: str, password: str, is_admin:bool =False):
    """enregistre un nouveau user renvoie True si l'inscription est réussie,
    False si le pseudo est déjà utilisé"""
    clean_username = username.strip()
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. On cherche si un utilisateur porte déjà ce nom
        cursor.execute("SELECT id FROM users WHERE username = ?", (clean_username,))
        existing_user = cursor.fetchone()
        
        # 2. Si fetchone() renvoie un résultat, le pseudo est déjà pris
        if existing_user is not None:
            return False
        
        # 3. Sinon, on insère le nouvel utilisateur
        password_hash = hash_password(password)
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, is_admin)
            VALUES (?, ?, ?)
            """,
            (clean_username, password_hash, int(is_admin))
        )
        conn.commit()
        return True
    