from engine.character import Character

class Letter (Character):

    def __init__ (self, val):
        if self.__is_valid_letter(val) is True:
            Character.__init__(self, val)
        else:
            self.val = None

    def valid_letters (self):
        return ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')

    def __is_valid_letter (self, val):
        return (val is not None) and (val.upper() in self.valid_letters())
