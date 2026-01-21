from contact import Contact

class AddressBook:
    def __init__(self, filename="contacts.txt"):
        self.filename = filename

    def add_contact(self, contact_obj):
        """Ajoute un contact dans le fichier"""
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"{contact_obj.Nom};{contact_obj.adresse_el};{contact_obj.phone_number}\n")
        print(f"Contact '{contact_obj.Nom}' ajouté avec succès.")

    def remove_contact(self, nom):
        """Supprime un contact du fichier"""
        contacts_restants = []
        trouve = False

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    Nom, email, phone = line.strip().split(";")
                    if Nom.lower() != nom.lower():
                        contacts_restants.append(line)
                    else:
                        trouve = True

            with open(self.filename, "w", encoding="utf-8") as f:
                f.writelines(contacts_restants)

            if trouve:
                print(f"Contact '{nom}' supprimé.")
            else:
                print(f"Aucun contact trouvé au nom de '{nom}'.")

        except FileNotFoundError:
            print("Aucun fichier de contacts trouvé.")

    def display_contact(self, nom):
        """Affiche un contact depuis le fichier"""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    Nom, email, phone = line.strip().split(";")
                    if Nom.lower() == nom.lower():
                        print("\n--- Informations du Contact ---")
                        print(f"Nom   : {Nom}")
                        print(f"Email : {email}")
                        print(f"Tel   : {phone}")
                        print("------------------------------")
                        return

            print(f"Aucun contact trouvé pour le nom : {nom}")

        except FileNotFoundError:
            print("Aucun fichier de contacts trouvé.")
