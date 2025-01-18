class QCMApp:
    def __init__(self):
        self.current_user = None
        self.questions: Dict = {}
        self.users_data: Dict = {}
        self.categories = []
        self.initialize_files()

    """ici je gère la connexion de l'utilisateur"""
    username = input("Entrez votre nom d'utilisateur : ").strip()
    
    if username in self.users_data:
        print(f"\nBienvenue de retour, {username}!")
        self.display_user_history(username)
    else:
        print(f"\nNouveau utilisateur créé : {username}")
        self.users_data[username] = {"history": []}
        self.save_users_data()
    
    self.current_user = username

    def display_user_history(self, username: str):
        """j'affiche ici l'historique QCM d'un utilisateur"""
        if not self.users_data[username]['history']:
            print("Aucun historique disponible.")
            return

        print("\nHistorique de", username, ":")
        for entry in self.users_data[username]['history']:
            print(f"- Date: {entry['date']}, "
                f"Catégorie: {entry['category']}, "
                f"Score: {entry['score']}/{entry['total']}, "
                f"Temps: {entry.get('time_taken', 'N/A')} secondes")


    def save_users_data(self):
        """je sauvgarde ici les données des users"""
        with open("data/users.json", "w", encoding="utf-8") as f:
            json.dump(self.users_data, f, ensure_ascii=False, indent=4)
    
    def initialize_files(self):
        #j'initialise les fichiers nécessaires s'ils n'existent pas
        Path("data").mkdir(exist_ok=True)
        
        if not Path("data/users.json").exists():
            with open("data/users.json", "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        
        # remplir le fichier de questions au debut
        if not Path("data/questions.json").exists():
            sample_questions = {
                "Python": [
                    {
                        "question": "Quel est le type de données en Python pour représenter du texte ?",
                        "options": {"a": "int", "b": "str", "c": "list"},
                        "correct": "b",
                        "explanation": "str est le type pour les chaînes de caractères en Python"
                    }
                ]
            }
            with open("data/questions.json", "w", encoding="utf-8") as f:
                json.dump(sample_questions, f, ensure_ascii=False, indent=4)

        self.load_data()

    def load_data(self):
        # ici je charge les données depuis les fichiers JSON

        with open("data/users.json", "r", encoding="utf-8") as f:
            self.users_data = json.load(f)
        with open("data/questions.json", "r", encoding="utf-8") as f:
            self.questions = json.load(f)
            self.categories = list(self.questions.keys())
