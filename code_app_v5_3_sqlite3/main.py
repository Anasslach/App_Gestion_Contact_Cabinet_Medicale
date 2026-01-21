import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

DB_FILE = "app.db"
ADMIN_USERS = ["Anass1"]  # utilisateurs admins

# ------------------ HASH MOT DE PASSE ------------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

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
    # Table contacts liée à l'utilisateur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

# ------------------ UTILISATEURS ------------------
def register_user_db(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_login_db(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user  # retourne l'utilisateur complet

# ------------------ CONTACTS ------------------
def add_contact_db(nom, email, phone, user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (nom, email, phone, user_id) VALUES (?, ?, ?, ?)", (nom, email, phone, user_id))
    conn.commit()
    conn.close()

def update_contact_db(old_nom, nom, email, phone, user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE contacts SET nom=?, email=?, phone=? WHERE nom=? AND user_id=?", (nom, email, phone, old_nom, user_id))
    conn.commit()
    conn.close()

def get_all_contacts_db(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT nom, email, phone FROM contacts WHERE user_id=? ORDER BY nom COLLATE NOCASE", (user_id,))
    contacts = cursor.fetchall()
    conn.close()
    return contacts

def delete_contact_db(nom, user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE nom=? AND user_id=?", (nom, user_id))
    conn.commit()
    conn.close()

# ------------------ LOGIN / INSCRIPTION ------------------
def check_login():
    global CURRENT_USER, CURRENT_USER_ID
    username = entry_user.get().strip()
    password = entry_pass.get().strip()
    user = check_login_db(username, password)
    if user:
        CURRENT_USER = username
        CURRENT_USER_ID = user[0]  # id de l'utilisateur
        login_window.withdraw()
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

# ------------------ FENÊTRE CONTACTS ------------------
def open_main_app():
    root = tk.Toplevel()
    root.title(f"Carnet d’adresses - {CURRENT_USER}")
    root.geometry("500x500")

    # ---- HEADER ----
    tk.Label(root, text=f"Carnet d’adresses - Connecté : {CURRENT_USER}", font=("Arial", 14, "bold")).pack(pady=10)

    # ---- FORM ----
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

    # ---- LISTBOX ----
    frameM = tk.Frame(root)
    frameM.pack(pady=10)
    scrollbar = tk.Scrollbar(frameM)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox = tk.Listbox(frameM, width=50, height=10, yscrollcommand=scrollbar.set)
    listbox.pack()
    scrollbar.config(command=listbox.yview)

    # ---- FONCTIONS ----
    def refresh_listbox(filter_text=""):
        listbox.delete(0, tk.END)
        for c in get_all_contacts_db(CURRENT_USER_ID):
            if filter_text.lower() in c[0].lower() or filter_text.lower() in c[1].lower():
                listbox.insert(tk.END, c[0])

    def clear_entries():
        entry_name.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_phone.delete(0, tk.END)

    def add_contact():
        nom, email, phone = entry_name.get().strip(), entry_email.get().strip(), entry_phone.get().strip()
        if not nom or not email or not phone:
            messagebox.showwarning("Attention", "Tous les champs sont requis")
            return
        add_contact_db(nom, email, phone, CURRENT_USER_ID)
        refresh_listbox()
        clear_entries()

    def delete_contact():
        sel = listbox.curselection()
        if not sel:
            messagebox.showwarning("Attention", "Aucun contact sélectionné")
            return
        nom = listbox.get(sel[0])
        delete_contact_db(nom, CURRENT_USER_ID)
        refresh_listbox()

    def show_contact():
        sel = listbox.curselection()
        if not sel:
            messagebox.showwarning("Attention", "Aucun contact sélectionné")
            return
        nom = listbox.get(sel[0])
        for c in get_all_contacts_db(CURRENT_USER_ID):
            if c[0] == nom:
                entry_name.delete(0, tk.END)
                entry_name.insert(0, c[0])
                entry_email.delete(0, tk.END)
                entry_email.insert(0, c[1])
                entry_phone.delete(0, tk.END)
                entry_phone.insert(0, c[2])

    def update_contact():
        sel = listbox.curselection()
        if not sel:
            messagebox.showwarning("Attention", "Sélectionnez un contact à modifier")
            return
        old_nom = listbox.get(sel[0])
        nom, email, phone = entry_name.get().strip(), entry_email.get().strip(), entry_phone.get().strip()
        if not nom or not email or not phone:
            messagebox.showwarning("Attention", "Tous les champs sont requis")
            return
        update_contact_db(old_nom, nom, email, phone, CURRENT_USER_ID)
        refresh_listbox()
        clear_entries()

    def search_contact():
        filter_text = entry_search.get().strip()
        refresh_listbox(filter_text)

    def logout():
        root.destroy()
        login_window.deiconify()

    # ---- SEARCH ----
    frameSearch = tk.Frame(root)
    frameSearch.pack(pady=5)
    tk.Label(frameSearch, text="Recherche:").pack(side=tk.LEFT)
    entry_search = tk.Entry(frameSearch)
    entry_search.pack(side=tk.LEFT)
    tk.Button(frameSearch, text="OK", command=search_contact).pack(side=tk.LEFT)

    # ---- BUTTONS ----
    frameB = tk.Frame(root)
    frameB.pack(pady=10)
    tk.Button(frameB, text="Ajouter", width=10, command=add_contact).pack(side=tk.LEFT, padx=5)
    tk.Button(frameB, text="Modifier", width=10, command=update_contact).pack(side=tk.LEFT, padx=5)
    tk.Button(frameB, text="Supprimer", width=10, command=delete_contact).pack(side=tk.LEFT, padx=5)
    tk.Button(frameB, text="Afficher", width=10, command=show_contact).pack(side=tk.LEFT, padx=5)
    if CURRENT_USER in ADMIN_USERS:
        tk.Button(frameB, text="Admin", width=10, command=open_admin_panel).pack(side=tk.LEFT, padx=5)
    tk.Button(frameB, text="Déconnexion", width=12, fg="red", command=logout).pack(side=tk.LEFT, padx=5)

    refresh_listbox()
    root.mainloop()

# ------------------ PANEL ADMIN ------------------
def open_admin_panel():
    admin_win = tk.Toplevel()
    admin_win.title("Admin - Visualisation DB")
    admin_win.geometry("600x400")

    frame_users = tk.Frame(admin_win)
    frame_users.pack(side=tk.LEFT, padx=10, pady=10)
    tk.Label(frame_users, text="UTILISATEURS", font=("Arial", 12, "bold")).pack()
    list_users = tk.Listbox(frame_users, width=30)
    list_users.pack()

    frame_contacts = tk.Frame(admin_win)
    frame_contacts.pack(side=tk.RIGHT, padx=10, pady=10)
    tk.Label(frame_contacts, text="CONTACTS", font=("Arial", 12, "bold")).pack()
    list_contacts = tk.Listbox(frame_contacts, width=40)
    list_contacts.pack()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users")
    users = cursor.fetchall()
    list_users.delete(0, tk.END)
    for u in users:
        list_users.insert(tk.END, f"ID:{u[0]} | {u[1]} | {u[2]}")
    cursor.execute("SELECT id, nom, email, phone, user_id FROM contacts")
    contacts = cursor.fetchall()
    list_contacts.delete(0, tk.END)
    for c in contacts:
        list_contacts.insert(tk.END, f"ID:{c[0]} | {c[1]} | {c[2]} | {c[3]} | UserID:{c[4]}")
    conn.close()

# ------------------ LOGIN / INSCRIPTION ------------------
CURRENT_USER = None
CURRENT_USER_ID = None
init_db()

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
