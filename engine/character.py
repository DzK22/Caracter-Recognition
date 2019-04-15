from shutil import copyfile
from pickle import Pickler, Unpickler

class Character:

    def __init__ (self, character):
        self.val = character
        self.positions = None
        self.__data_path = 'engine/data/'

    def set_positions (self, positions):
        self.positions = positions

    def save_positions (self):
        """ Save the current character positions in a file """
        assert self.positions is not None
        with open(self.__data_path + 'current/' + self.val, 'w+b') as file:
            pickler = Pickler(file)
            pickler.dump(self.positions)

    def load_positions (self):
        """ Load the character saved positions from a file """
        try:
            with open(self.__data_path + 'current/' + self.val, 'rb') as file:
                unpickler = Unpickler(file)
                self.positions = unpickler.load()
        except OSError:
            # file not exist
            self.positions = None

    def reset_default_positions (self):
        """ Reset current character position file (in data/current/) by the
            default (in data/default/) """
        assert self.positions is not None
        copyfile(self.__data_path + 'default/' + self.val,
                 self.__data_path + 'current/' + self.val)
