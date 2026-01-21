from contact import Contact 
from addressBook import AddressBook
def main():
    # Initialisation de l'annuaire (sans fichier)
    book = AddressBook()

    while True:
        print("\n--- GESTIONNAIRE DE CONTACTS ---")
        print("1. Add Contact")
        print("2. Remove Contact")
        print("3. Display Contact")
        print("4. Quit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter name: ")
            email = input("Enter email: ")
            phone = input("Enter phone number: ")
            
            try:
                # Création de l'objet Contact
                # C'est ici que les 'assert' de contact.py sont vérifiés
                nouveau_contact = Contact(name, email, phone)
                
                # Ajout à la liste dans AddressBook
                book.add_contact(nouveau_contact)
                
            except AssertionError as e:
                # Si un assert échoue, on affiche le message d'erreur sans quitter le programme
                print(f"ALERTE : {e}")
            except Exception as e:
                print(f"Une erreur inattendue est survenue : {e}")

        elif choice == "2":
            name = input("Enter name to remove: ")  
            book.remove_contact(name)

        elif choice == "3":
            name = input("Enter name to display: ")  
            book.display_contact(name) 

        elif choice == "4":
            print("Fin du programme. Au revoir !")
            break # Quitte la boucle while et donc le programme
            
        else:
            print("Choix invalide. Veuillez entrer un nombre entre 1 et 4.")

if __name__ == "__main__":
    main()
