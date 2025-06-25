class Player:
    def __init__(self, name):
        self.name = name
        self.current_occupation = None

    def set_occupation(self, occupation : str):
        self.current_occupation = occupation

    def get_occupation(self):
        return self.current_occupation

    def is_spy(self):
        return self.current_occupation == "spy"