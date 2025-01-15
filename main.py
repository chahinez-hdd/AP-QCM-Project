def run(self):
    """Boucle principale de l'application"""
    print("=== Bienvenue au QCM Informatique ! ===")

    while True:
        self.handle_user_login()

        while True:
            print("\nMenu principal:")
            print("1. Commencer un nouveau QCM")
            print("2. Voir mon historique")
            print("3. Exporter mes résultats")
            print("4. Changer d'utilisateur")
            print("5. Quitter")

            choice = input("\nVotre choix : ")
