from engine.character import Character

class Punctuation (Character):

    def __init__ (self, val):
        Character.__init__(self, val)

    def valid_punctuations (self):
        return ('?', '.', ',', '\'', '`', '-', '_', '"', ':', '(', ')', '{',
            '}', '[', ']', '<', '>', ';', '@', '#', '$', '%', '^', '&', '*',
            '!', '~', '+', '=', '\\', '|', '/', 'TB')

    def __is_valid_punctuation (self, val):
        return (val is not None) and (val.upper() in self.valid_punctuations())
