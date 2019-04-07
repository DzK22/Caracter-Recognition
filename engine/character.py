import os
from pickle import Pickler, Unpickler

class Character:

    def __init__ (self, character):
        self.val = character
        self.positions = None
        self.files_path = 'engine/data/'

    def set_positions (self, positions):
        self.positions = positions

    def save_positions (self):
        """ Save the current character positions in a file """
        assert self.positions is not None
        with open(self.files_path + self.val, 'w+b') as file:
            pickler = Pickler(file)
            pickler.dump(self.positions)

    def load_positions (self):
        """ Load the character saved positions from a file """
        try:
            with open(self.files_path + self.val, 'rb') as file:
                unpickler = Unpickler(file)
                self.positions = unpickler.load()
        except OSError:
            # file not exist
            self.positions = None

    def delete_positions (self):
        """ Delete the character positions file """
        assert self.positions is not None
        os.remove(self.files_path + self.val)
