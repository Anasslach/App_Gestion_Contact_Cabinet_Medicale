class AddressBook:
    def __init__(self):
        # On initialise une liste vide pour stocker les objets Contact
        self.contacts = []

    def add_contact(self, contact_obj):
        """Ajoute un objet Contact à la liste."""
        self.contacts.append(contact_obj)
        print(f"Contact '{contact_obj.Nom}' ajouté avec succès.")

    def remove_contact(self, nom):
        """Supprime un contact de la liste par son nom."""
        # On garde tous les contacts dont le nom ne correspond pas à celui saisi
        taille_initiale = len(self.contacts)
        self.contacts = [c for c in self.contacts if c.Nom.lower() != nom.lower()]
        
        if len(self.contacts) < taille_initiale:
            print(f"Contact '{nom}' supprimé.")
        else:
            print(f"Erreur : Aucun contact trouvé au nom de '{nom}'.")

    def display_contact(self, nom):
        """Recherche et affiche un contact par son nom."""
        trouve = False
        for c in self.contacts:
            if c.Nom.lower() == nom.lower():
                print("\n--- Informations du Contact ---")
                print(f"Nom    : {c.Nom}")
                print(f"Email  : {c.adresse_el}")
                print(f"Tel    : {c.phone_number}")
                print("------------------------------")
                trouve = True
                break
        
        if not trouve:
            print(f"Aucun contact trouvé pour le nom : {nom}")

