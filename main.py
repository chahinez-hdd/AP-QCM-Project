import json
import csv
from typing import List, Dict

class QuizManager:
    def __init__(self):
        """Initialize the quiz manager with questions and categories"""
        self.categories: List[str] = []
        self.questions: Dict = {}
        self.users_data: Dict = {}
        self.load_questions()

    def load_questions(self):
        """Load questions and categories from the JSON file"""
        try:
            with open('data/questions.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.questions = data
                self.categories = list(data.keys())
        except FileNotFoundError:
            print("Error: Questions file not found.")
            self.questions = {}
            self.categories = []
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in questions file.")
            self.questions = {}
            self.categories = []

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
