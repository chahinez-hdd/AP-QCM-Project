class QCMApp:
    def __init__(self):
        self.current_user = None
        self.questions: Dict = {}
        self.users_data: Dict = {}
        self.categories = []
        self.initialize_files()



 