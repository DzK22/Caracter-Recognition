from engine.character import Character

class Accent (Character):

    def __init__ (self, val):
        Character.__init__(self, val)

    def valid_accents (self):
        return ('Ç', 'Æ', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å')

    def __is_valid_accent (self, val):
        return (val is not None) and (val.upper() in self.valid_accents())
