
class Timer:
    def __init__(self, duration: int):
        self.duration = duration
        self.time_left = duration
        self.running = False
        self._timer_thread = None

    def start(self):
        """Démarre le chronomètre"""
        self.running = True
        self._timer_thread = threading.Thread(target=self._run_timer)
        self._timer_thread.daemon = True
        self._timer_thread.start()

    def _run_timer(self):
        """Fait tourner le chronomètre"""
        while self.running and self.time_left > 0:
            time.sleep(1)
            self.time_left -= 1
            sys.stdout.write(f"\rTemps restant: {self.time_left} secondes")
            sys.stdout.flush()
        if self.time_left <= 0:
            print("\nTemps écoulé!")
            self.running = False

    def stop(self):
        """Arrête le chronomètre"""
        self.running = False
        if self._timer_thread:
            self._timer_thread.join()

    def is_time_up(self) -> bool:
        """Vérifie si le temps est écoulé"""
        return self.time_left <= 0

# Running the Quiz
def run_quiz(self, category: str) -> dict:
    """Exécute le QCM pour une catégorie donnée"""
    questions = self.questions[category]
    score = 0
    total_questions = len(questions)
    start_time = time.time()

    print(f"\nQCM de {category} - {total_questions} questions")
    print("Vous avez 30 secondes par question.")

    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}/{total_questions} :")
        print(q["question"])
        for opt, text in q["options"].items():
            print(f"{opt}) {text}")

        self.timer = Timer(30)
        self.timer.start()

        response = input("\nVotre réponse (a/b/c) : ").lower()
        
        self.timer.stop()
        if self.timer.is_time_up():
            print("Temps écoulé! Question comptée comme incorrecte.")
            continue

        if response == q["correct"]:
            print("✓ Bonne réponse!")
            score += 1
        else:
            print(f"✗ Mauvaise réponse. La bonne réponse était: {q['correct']}")
            print(f"Explication: {q['explanation']}")

    end_time = time.time()
    time_taken = round(end_time - start_time)

    result = {
        "score": score,
        "total": total_questions,
        "time_taken": time_taken,
        "category": category
    }




    return result



class QCMApp:
    def __init__(self):
        self.current_user = None
        self.questions: Dict = {}
        self.users_data: Dict = {}
        self.categories = []
        self.initialize_files()



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


