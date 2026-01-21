from contact import Contact
from addressBook import AddressBook

def main():
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
                contact = Contact(name, email, phone)
                book.add_contact(contact)
            except AssertionError as e:
                print(f"ALERTE : {e}")

        elif choice == "2":
            name = input("Enter name to remove: ")
            book.remove_contact(name)

        elif choice == "3":
            name = input("Enter name to display: ")
            book.display_contact(name)

        elif choice == "4":
            print("Fin du programme. Au revoir !")
            break

        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
