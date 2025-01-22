import json
import datetime
import time
from pathlib import Path
import csv
import threading
import sys
from typing import Dict, List, Optional






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


class QCMApp:
    def __init__(self):
        self.current_user = None
        self.questions: Dict = {}
        self.users_data: Dict = {}
        self.categories = []
        self.initialize_files()

    def handle_user_login(self):
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
                                    "options": {
                                        "a": "int",
                                        "b": "str",
                                        "c": "list"
                                    },
                                    "correct": "b",
                                    "explanation": "str est le type pour les chaînes de caractères en Python"
                                },
                                {
                                    "question": "Quelle est la complexité moyenne de recherche dans un tableau trié ?",
                                    "options": {
                                        "a": "O(1)",
                                        "b": "O(log n)",
                                        "c": "O(n)"
                                    },
                                    "correct": "b",
                                    "explanation": "La recherche binaire dans un tableau trié a une complexité de O(log n)"
                                }
                            ],
                            "Réseaux": [
                                {
                                    "question": "Quel protocole est utilisé pour l'envoi d'emails ?",
                                    "options": {
                                        "a": "SMTP",
                                        "b": "HTTP",
                                        "c": "FTP"
                                    },
                                    "correct": "a",
                                    "explanation": "SMTP (Simple Mail Transfer Protocol) est le protocole standard pour l'envoi d'emails"
                                }
                            ],
                            "Algorithmes": [
                                {
                                    "question": "Quelle est la complexité du tri rapide (Quicksort) en moyenne ?",
                                    "options": {
                                        "a": "O(n)",
                                        "b": "O(n log n)",
                                        "c": "O(n²)"
                                    },
                                    "correct": "b",
                                    "explanation": "Le tri rapide a une complexité moyenne de O(n log n)"
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

    def select_category(self) -> str:
        """Permet à l'utilisateur de choisir une catégorie de questions"""
        print("\nCatégories disponibles:")
        for i, category in enumerate(self.categories, 1):
            print(f"{i}. {category}")
        
        while True:
            try:
                choice = int(input("\nChoisissez une catégorie (numéro) : "))
                if 1 <= choice <= len(self.categories):
                    return self.categories[choice - 1]
                print("Choix invalide.")
            except ValueError:
                print("Veuillez entrer un numéro valide.")

    def export_results(self, username: str, filename: str):
        """Exporte les résultats d'un utilisateur dans un fichier CSV"""
        if username not in self.users_data:
            print("Utilisateur non trouvé.")
            return

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Catégorie', 'Score', 'Temps total'])
            for entry in self.users_data[username]['history']:
                writer.writerow([
                    entry['date'],
                    entry['category'],
                    f"{entry['score']}/{entry['total']}",
                    f"{entry.get('time_taken', 'N/A')} secondes"
                ])
        print(f"\nRésultats exportés dans le fichier: {filename}")

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

    def save_quiz_result(self, result: dict):
        """Sauvegarde le résultat du QCM"""
        if not self.current_user:
            return

        result_entry = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "score": result["score"],
            "total": result["total"],
            "time_taken": result["time_taken"],
            "category": result["category"]
        }

        self.users_data[self.current_user]["history"].append(result_entry)
        self.save_users_data()

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

                


if __name__ == "__main__":
    app = QCMApp()
    app.run()