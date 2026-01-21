import tkinter as tk
from tkinter import messagebox
from contact import Contact
from addressBook import AddressBook
import os

USERS_FILE = "users.txt"

# ------------------ GESTION DES UTILISATEURS ------------------

def load_users(filename=USERS_FILE):
    """Charge tous les utilisateurs depuis le fichier"""
    users = {}
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if ";" in line:
                    username, password = line.strip().split(";")
                    users[username] = password
    return users

def save_user(username, password, filename=USERS_FILE):
    """Ajoute un nouvel utilisateur dans le fichier"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{username};{password}\n")

# ------------------ FONCTIONS AUTHENTIFICATION ------------------

def check_login():
    username = entry_user.get().strip()
    password = entry_pass.get().strip()
    users = load_users()

    if username in users and users[username] == password:
        login_window.destroy()
        open_main_app()
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")

def register_user():
    username = entry_user.get().strip()
    password = entry_pass.get().strip()
    users = load_users()

    if not username or not password:
        messagebox.showwarning("Attention", "Veuillez remplir tous les champs")
        return

    if username in users:
        messagebox.showerror("Erreur", "Nom d'utilisateur déjà utilisé")
    else:
        save_user(username, password)
        messagebox.showinfo("Succès", f"Utilisateur '{username}' créé avec succès")

# ------------------ APPLICATION PRINCIPALE ------------------

def open_main_app():
    book = AddressBook()

    def refresh_listbox():
        listbox.delete(0, tk.END)
        for c in book.get_all_contacts():
            listbox.insert(tk.END, c[0])

    def add_contact():
        try:
            contact = Contact(
                entry_name.get(),
                entry_email.get(),
                entry_phone.get()
            )
            book.add_contact(contact)
            refresh_listbox()
            clear_entries()
        except AssertionError as e:
            messagebox.showerror("Erreur", str(e))

    def delete_contact():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Aucun contact sélectionné")
            return

        nom = listbox.get(selection[0])
        book.remove_contact(nom)
        refresh_listbox()

    def show_contact():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Aucun contact sélectionné")
            return

        nom = listbox.get(selection[0])
        for c in book.get_all_contacts():
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

    # ---------------- Fenêtre principale ----------------
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

    frameB = tk.Frame(root)
    frameB.pack(pady=10)
    tk.Button(frameB, text="Ajouter", width=10, command=add_contact).pack(side=tk.LEFT, padx=5)
    tk.Button(frameB, text="Supprimer", width=10, command=delete_contact).pack(side=tk.LEFT, padx=5)
    tk.Button(frameB, text="Afficher", width=10, command=show_contact).pack(side=tk.LEFT, padx=5)

    refresh_listbox()
    root.mainloop()

# ------------------ FENÊTRE LOGIN / INSCRIPTION ------------------

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

# Boutons Connexion et Inscription
frame_buttons = tk.Frame(login_window)
frame_buttons.pack(pady=15)
tk.Button(frame_buttons, text="Connexion", width=12, command=check_login).pack(side=tk.LEFT, padx=5)
tk.Button(frame_buttons, text="Inscription", width=12, command=register_user).pack(side=tk.LEFT, padx=5)

login_window.mainloop()
