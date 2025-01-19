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
            
            if choice == "1":
                category = self.select_category()
                result = self.run_quiz(category)
                print(f"\nVotre score final : {result['score']}/{result['total']}")
                print(f"Temps total : {result['time_taken']} secondes")
                self.save_quiz_result(result)
            
            elif choice == "2":
                self.display_user_history(self.current_user)
            
            elif choice == "3":
                filename = f"resultats_{self.current_user}_{datetime.datetime.now().strftime('%Y%m%d')}.csv"
                self.export_results(self.current_user, filename)
            
            elif choice == "4":
                break
            
            elif choice == "5":
                print("\nMerci d'avoir utilisé l'application QCM!")
                return
            
            else:
                print("\nChoix invalide. Veuillez réessayer.")
