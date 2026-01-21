class Contact:
    def __init__(self,Nom,email,phone_number):
        assert isinstance(Nom, str) and Nom, "Nom doit être une chaîne non vide"
        assert isinstance(email, str)    and email,    "adresse_electronique doit être une chaîne non vide"
        assert isinstance(phone_number, str) and phone_number.isdigit(), "Num_tel doit être une chaîne de chiffres uniquement"
        self.Nom=Nom
        self.adresse_el=email
        self.phone_number=phone_number