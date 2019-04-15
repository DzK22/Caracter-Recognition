from engine.character import Character

class Letter (Character):

    def __init__ (self, val):
        if self.__valid_letter(val) is True:
            Character.__init__(self, val)
        else:
            self.val = None

    def __valid_letter (self, val)
        return val.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
