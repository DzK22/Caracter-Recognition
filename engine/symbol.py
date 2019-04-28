from engine.character import Character

class Symbol (Character):

    def __init__ (self, val):
        Character.__init__(self, val)

    def valid_symbols (self):
        return ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'SP', 'CR', 'SH', 'CL', 'BS')

    def __is_valid_symbol (self, val):
        return (val is not None) and (val.upper() in self.valid_symbols())
