import json
import datetime
import time
from pathlib import Path
import csv
import threading
import sys
from typing import Dict, List, Optional
import tkinter as tk
from tkinter import messagebox, ttk, filedialog

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
        if self.time_left <= 0:
            self.running = False

    def stop(self):
        """Arrête le chronomètre"""
        self.running = False
        if self._timer_thread:
            self._timer_thread.join()

    def is_time_up(self) -> bool:
        """Vérifie si le temps est écoulé"""
        return self.time_left <= 0


class QCMAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("QCM Informatique")
        self.current_user = None
        self.questions: Dict = {}
        self.users_data: Dict = {}
        self.categories = []
        self.initialize_files()
        self.create_login_screen()

    def create_login_screen(self):
        """Crée l'interface de connexion"""
        self.clear_screen()
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Nom d'utilisateur:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.login_frame, font=("Arial", 14))
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.login_frame, text="Connexion", font=("Arial", 14), command=self.handle_user_login, width=20, height=2).grid(row=1, column=0, columnspan=2, pady=10)

    def handle_user_login(self):
        """Gère la connexion de l'utilisateur"""
        username = self.username_entry.get().strip()
        
        if username in self.users_data:
            messagebox.showinfo("Bienvenue", f"Bienvenue de retour, {username}!")
            self.display_user_history(username)
        else:
            messagebox.showinfo("Nouvel utilisateur", f"Nouveau utilisateur créé : {username}")
            self.users_data[username] = {"history": []}
            self.save_users_data()
        
        self.current_user = username
        self.create_main_menu()

    def display_user_history(self, username: str):
        """Affiche l'historique QCM d'un utilisateur"""
        if not self.users_data[username]['history']:
            messagebox.showinfo("Historique", "Aucun historique disponible.")
            return

        history_window = tk.Toplevel(self.root)
        history_window.title(f"Historique de {username}")
        history_text = tk.Text(history_window, wrap=tk.WORD, font=("Arial", 12))
        history_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        for entry in self.users_data[username]['history']:
            history_text.insert(tk.END, f"- Date: {entry['date']}, "
                                      f"Catégorie: {entry['category']}, "
                                      f"Score: {entry['score']}/{entry['total']}, "
                                      f"Temps: {entry.get('time_taken', 'N/A')} secondes\n")

        history_text.config(state=tk.DISABLED)

    def save_users_data(self):
        """Sauvegarde les données des utilisateurs"""
        with open("data/users.json", "w", encoding="utf-8") as f:
            json.dump(self.users_data, f, ensure_ascii=False, indent=4)
    
    def initialize_files(self):
        """Initialise les fichiers nécessaires s'ils n'existent pas"""
        Path("data").mkdir(exist_ok=True)
        
        if not Path("data/users.json").exists():
            with open("data/users.json", "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        
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
        """Charge les données depuis les fichiers JSON"""
        with open("data/users.json", "r", encoding="utf-8") as f:
            self.users_data = json.load(f)
        with open("data/questions.json", "r", encoding="utf-8") as f:
            self.questions = json.load(f)
            self.categories = list(self.questions.keys())

    def create_main_menu(self):
        """Crée le menu principal"""
        self.clear_screen()
        self.main_menu_frame = tk.Frame(self.root)
        self.main_menu_frame.pack(pady=20)

        tk.Button(self.main_menu_frame, text="Commencer un nouveau QCM", font=("Arial", 14), command=self.start_new_quiz, width=30, height=2).pack(pady=10)
        tk.Button(self.main_menu_frame, text="Voir mon historique", font=("Arial", 14), command=lambda: self.display_user_history(self.current_user), width=30, height=2).pack(pady=10)
        tk.Button(self.main_menu_frame, text="Exporter mes résultats", font=("Arial", 14), command=self.export_results, width=30, height=2).pack(pady=10)
        tk.Button(self.main_menu_frame, text="Changer d'utilisateur", font=("Arial", 14), command=self.create_login_screen, width=30, height=2).pack(pady=10)
        tk.Button(self.main_menu_frame, text="Quitter", font=("Arial", 14), command=self.root.quit, width=30, height=2).pack(pady=10)

    def start_new_quiz(self):
        """Démarre un nouveau QCM"""
        self.clear_screen()
        self.quiz_frame = tk.Frame(self.root)
        self.quiz_frame.pack(pady=20)

        tk.Label(self.quiz_frame, text="Choisissez une catégorie:", font=("Arial", 14)).pack(pady=10)
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(self.quiz_frame, textvariable=self.category_var, font=("Arial", 14))
        self.category_menu['values'] = self.categories
        self.category_menu.pack(pady=10)

        tk.Button(self.quiz_frame, text="Commencer", font=("Arial", 14), command=self.run_quiz, width=20, height=2).pack(pady=10)
        tk.Button(self.quiz_frame, text="Retour", font=("Arial", 14), command=self.create_main_menu, width=20, height=2).pack(pady=10)

    def run_quiz(self):
        """Exécute le QCM pour une catégorie donnée"""
        category = self.category_var.get()
        if not category:
            messagebox.showwarning("Erreur", "Veuillez sélectionner une catégorie.")
            return

        self.clear_screen()
        self.quiz_questions = self.questions[category]
        self.current_question_index = 0
        self.score = 0
        self.start_time = time.time()

        self.quiz_question_frame = tk.Frame(self.root)
        self.quiz_question_frame.pack(pady=20)

        self.timer = Timer(30)
        self.timer.start()
        self.update_timer_display()

        self.display_question()

    def display_question(self):
        """Affiche la question actuelle"""
        self.clear_screen()
        self.quiz_question_frame = tk.Frame(self.root)
        self.quiz_question_frame.pack(pady=20)

        question = self.quiz_questions[self.current_question_index]
        tk.Label(self.quiz_question_frame, text=question["question"], font=("Arial", 14), wraplength=600).pack(pady=10)

        for opt, text in question["options"].items():
            # Dynamically adjust button width based on text length
            button_width = max(len(f"{opt}) {text}") + 5, 20)  # Minimum width of 20
            tk.Button(self.quiz_question_frame, text=f"{opt}) {text}", font=("Arial", 14), width=button_width, height=2, command=lambda opt=opt: self.check_answer(opt)).pack(pady=5)

    def check_answer(self, selected_option: str):
        """Vérifie la réponse de l'utilisateur"""
        if self.timer.is_time_up():
            messagebox.showinfo("Temps écoulé", "Temps écoulé! Question comptée comme incorrecte.")
        else:
            question = self.quiz_questions[self.current_question_index]
            if selected_option == question["correct"]:
                self.score += 1
                messagebox.showinfo("Résultat", "✓ Bonne réponse!")
            else:
                messagebox.showinfo("Résultat", f"✗ Mauvaise réponse. La bonne réponse était: {question['correct']}\nExplication: {question['explanation']}")

        self.current_question_index += 1
        if self.current_question_index < len(self.quiz_questions):
            self.display_question()
        else:
            self.finish_quiz()

    def finish_quiz(self):
        """Termine le QCM et affiche les résultats"""
        self.timer.stop()
        end_time = time.time()
        time_taken = round(end_time - self.start_time)

        result = {
            "score": self.score,
            "total": len(self.quiz_questions),
            "time_taken": time_taken,
            "category": self.category_var.get()
        }

        messagebox.showinfo("Résultat", f"Votre score final : {result['score']}/{result['total']}\nTemps total : {result['time_taken']} secondes")
        self.save_quiz_result(result)
        self.create_main_menu()

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

    def export_results(self):
        """Exporte les résultats de l'utilisateur dans un fichier CSV"""
        if not self.current_user:
            return

        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not filename:
            return

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Catégorie', 'Score', 'Temps total'])
            for entry in self.users_data[self.current_user]['history']:
                writer.writerow([
                    entry['date'],
                    entry['category'],
                    f"{entry['score']}/{entry['total']}",
                    f"{entry.get('time_taken', 'N/A')} secondes"
                ])
        messagebox.showinfo("Export réussi", f"Résultats exportés dans le fichier: {filename}")

    def update_timer_display(self):
        """Met à jour l'affichage du timer"""
        if self.timer.running:
            self.root.after(1000, self.update_timer_display)
            if hasattr(self, 'quiz_question_frame'):
                for widget in self.quiz_question_frame.winfo_children():
                    if isinstance(widget, tk.Label) and widget.cget("text").startswith("Temps restant:"):
                        widget.destroy()
                tk.Label(self.quiz_question_frame, text=f"Temps restant: {self.timer.time_left} secondes", font=("Arial", 14)).pack(pady=10)

    def clear_screen(self):
        """Efface l'écran actuel"""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QCMAppGUI(root)
    root.mainloop()