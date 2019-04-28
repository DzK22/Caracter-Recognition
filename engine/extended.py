from engine.character import Character

class Extended (Character):

    def __init__ (self, val):
        Character.__init__(self, val)

    def valid_extendeds (self):
        return ('•', 'ʻ', 'ʼ', '“', '”', '○', '+', '–', '£', '×', '÷', '¡', '=',
            'Ø', '$', '§', 'μ', '∫', 'ß', '¿', '©', '™', '®', '¢', '€', '¥')

    def __is_valid_extended (self, val):
        return (val is not None) and (val.upper() in self.valid_extendeds())
