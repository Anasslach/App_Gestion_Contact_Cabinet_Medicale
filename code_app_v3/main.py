import tkinter as tk
from contact import Contact
from addressBook import AddressBook
from tkinter import messagebox

book = AddressBook()

def refresh_listbox():
    listbox.delete(0, tk.END)
    for c in book.get_all_contacts():
        listbox.insert(tk.END, c[0])

def add_contact():
    try:
        c = Contact(
            entry_name.get(),
            entry_email.get(),
            entry_phone.get()
        )
        book.add_contact(c)
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
root.geometry("350x400")

# ---------------- Frame Haut ----------------
frameH = tk.Frame(root)
frameH.pack(pady=10)

tk.Label(frameH, text="Carnet d’adresses", font=("Arial", 14, "bold")).pack()

# ---------------- Frame Formulaire ----------------
frameForm = tk.Frame(root)
frameForm.pack(pady=5)

tk.Label(frameForm, text="Nom").grid(row=0, column=0, sticky="e")
tk.Label(frameForm, text="Email").grid(row=1, column=0, sticky="e")
tk.Label(frameForm, text="Tel").grid(row=2, column=0, sticky="e")

entry_name = tk.Entry(frameForm, width=25)
entry_email = tk.Entry(frameForm, width=25)
entry_phone = tk.Entry(frameForm, width=25)

entry_name.grid(row=0, column=1)
entry_email.grid(row=1, column=1)
entry_phone.grid(row=2, column=1)

# ---------------- Frame Milieu ----------------
frameM = tk.Frame(root)
frameM.pack(pady=10)

scrollbar = tk.Scrollbar(frameM)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frameM, width=30, height=8, yscrollcommand=scrollbar.set)
listbox.pack()

scrollbar.config(command=listbox.yview)

# ---------------- Frame Bas ----------------
frameB = tk.Frame(root)
frameB.pack(pady=10)

tk.Button(frameB, text="Ajouter", width=10, command=add_contact).pack(side=tk.LEFT, padx=5)
tk.Button(frameB, text="Supprimer", width=10, command=delete_contact).pack(side=tk.LEFT, padx=5)
tk.Button(frameB, text="Afficher", width=10, command=show_contact).pack(side=tk.LEFT, padx=5)

refresh_listbox()
root.mainloop()
