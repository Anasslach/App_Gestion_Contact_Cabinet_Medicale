import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_FILE = "app.db"

# ------------------ INITIALISATION DE LA BASE ------------------

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Table utilisateurs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Table contacts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# ------------------ FONCTIONS UTILISATEURS ------------------

def register_user_db(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_login_db(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# ------------------ FONCTIONS CONTACTS ------------------

def add_contact_db(nom, email, phone):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (nom, email, phone) VALUES (?, ?, ?)", (nom, email, phone))
    conn.commit()
    conn.close()

def get_all_contacts_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT nom, email, phone FROM contacts ORDER BY nom COLLATE NOCASE")
    contacts = cursor.fetchall()
    conn.close()
    return contacts

def delete_contact_db(nom):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE nom=?", (nom,))
    conn.commit()
    conn.close()

# ------------------ INTERFACE TKINTER ------------------

# Connexion / Inscription
def check_login():
    username = entry_user.get().strip()
    password = entry_pass.get().strip()
    if check_login_db(username, password):
        login_window.destroy()
        open_main_app()
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")

def register_user():
    username = entry_user.get().strip()
    password = entry_pass.get().strip()

    if not username or not password:
        messagebox.showwarning("Attention", "Veuillez remplir tous les champs")
        return

    if register_user_db(username, password):
        messagebox.showinfo("Succès", f"Utilisateur '{username}' créé avec succès")
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur déjà utilisé")

# Fenêtre principale contacts
def open_main_app():
    root = tk.Tk()
    root.title("Carnet d’adresses")
    root.geometry("360x420")

    frameH = tk.Frame(root)
    frameH.pack(pady=10)
    tk.Label(frameH, text="Carnet d’adresses", font=("Arial", 14, "bold")).pack()

    frameForm = tk.Frame(root)
    frameForm.pack(pady=5)

    tk.Label(frameForm, text="Nom").grid(row=0, column=0, sticky="e")
    tk.Label(frameForm, text="Email").grid(row=1, column=0, sticky="e")
    tk.Label(frameForm, text="Téléphone").grid(row=2, column=0, sticky="e")

    entry_name = tk.Entry(frameForm, width=25)
    entry_email = tk.Entry(frameForm, width=25)
    entry_phone = tk.Entry(frameForm, width=25)
    entry_name.grid(row=0, column=1)
    entry_email.grid(row=1, column=1)
    entry_phone.grid(row=2, column=1)

    frameM = tk.Frame(root)
    frameM.pack(pady=10)
    scrollbar = tk.Scrollbar(frameM)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox = tk.Listbox(frameM, width=30, height=8, yscrollcommand=scrollbar.set)
    listbox.pack()
    scrollbar.config(command=listbox.yview)

    def refresh_listbox():
        listbox.delete(0, tk.END)
        for c in get_all_contacts_db():
            listbox.insert(tk.END, c[0])

    def add_contact():
        nom = entry_name.get().strip()
        email = entry_email.get().strip()
        phone = entry_phone.get().strip()
        if not nom or not email or not phone:
            messagebox.showwarning("Attention", "Tous les champs sont requis")
            return
        add_contact_db(nom, email, phone)
        refresh_listbox()
        clear_entries()

    def delete_contact():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Aucun contact sélectionné")
            return
        nom = listbox.get(selection[0])
        delete_contact_db(nom)
        refresh_listbox()

    def show_contact():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Aucun contact sélectionné")
            return
        nom = listbox.get(selection[0])
        for c in get_all_contacts_db():
            if c[0] == nom:
                entry_name.delete(0, tk.END)
                entry_name.insert(0, c[0])
                entry_email.delete(0, tk.END)
                entry_email.insert(0, c[1])
                entry_phone.delete(0, tk.END)
                entry_phone.insert(0, c[2])

    def clear_entries():
        entry_name.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_phone.delete(0, tk.END)

    frameB = tk.Frame(root)
    frameB.pack(pady=10)
    tk.Button(frameB, text="Ajouter", width=10, command=add_contact).pack(side=tk.LEFT, padx=5)
    tk.Button(frameB, text="Supprimer", width=10, command=delete_contact).pack(side=tk.LEFT, padx=5)
    tk.Button(frameB, text="Afficher", width=10, command=show_contact).pack(side=tk.LEFT, padx=5)

    refresh_listbox()
    root.mainloop()

# ------------------ FENÊTRE LOGIN / INSCRIPTION ------------------

init_db()  # créer tables si nécessaire

login_window = tk.Tk()
login_window.title("Authentification")
login_window.geometry("320x220")

tk.Label(login_window, text="Authentification", font=("Arial", 12, "bold")).pack(pady=10)

tk.Label(login_window, text="Nom d'utilisateur").pack()
entry_user = tk.Entry(login_window)
entry_user.pack()

tk.Label(login_window, text="Mot de passe").pack()
entry_pass = tk.Entry(login_window, show="*")
entry_pass.pack()

frame_buttons = tk.Frame(login_window)
frame_buttons.pack(pady=15)
tk.Button(frame_buttons, text="Connexion", width=12, command=check_login).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="Inscription", width=12, command=register_user).pack(side=tk.LEFT, padx=5)

login_window.mainloop()
