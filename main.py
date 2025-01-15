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
