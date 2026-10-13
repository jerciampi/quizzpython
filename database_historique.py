import sqlite3

connection = sqlite3.connect("historique.db")
print(connection.total_changes)
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS historique (id_hist INTEGER, score INTEGER, date TEXT, heure TEXT)")
#cursor.execute("INSERT INTO historique VALUES (1, 32, '2025-10-10', '15:25')")
# cursor.execute("INSERT INTO historique VALUES (2, 24, '2026-12-07', '11:22')")
# cursor.execute("INSERT INTO historique VALUES (3, 67, '2024-06-26', '14:48')")


cursor.execute("SELECT * FROM historique")
rows = cursor.fetchall()
for row in rows:
    print(row)

#cursor.execute("DELETE FROM historique WHERE id_hist = 1")
# cursor.execute("DELETE FROM historique WHERE id_hist = 2")
# cursor.execute("DELETE FROM historique WHERE id_hist = 3")

cursor.execute("UPDATE historique SET score = 31 WHERE id_hist = 1")

cursor.execute("SELECT * FROM historique")
rows = cursor.fetchall()
for row in rows:
    print(row)

connection.commit()