
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
