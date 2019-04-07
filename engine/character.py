from pickle import Pickler, Unpickler

class Character:

    def __init__ (self, character):
        self.val = character
        self.positions = None
        self.files_path = 'engine/data/'

    def set_positions (self, positions):
        self.positions = positions

    def save_positions (self):
        assert self.positions is not None
        with open(self.files_path + self.val, 'w+b') as file:
            pickler = Pickler(file)
            pickler.dump(self.positions)

    def load_positions (self):
        try:
            with open(self.files_path + self.val, 'rb') as file:
                unpickler = Unpickler(file)
                self.positions = unpickler.load()
        except OSError:
            # file not exist
            self.positions = None
