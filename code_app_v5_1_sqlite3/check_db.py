import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

# Afficher tous les utilisateurs
print("=== UTILISATEURS ===")
cursor.execute("SELECT id, username, password FROM users")
for row in cursor.fetchall():
    print(row)

# Afficher tous les contacts
print("\n=== CONTACTS ===")
cursor.execute("SELECT id, nom, email, phone FROM contacts")
for row in cursor.fetchall():
    print(row)

conn.close()
