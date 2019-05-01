import math
from engine.character import Character
from engine.letter import Letter
from engine.symbol import Symbol
from engine.punctuation import Punctuation
from engine.extended import Extended
from engine.accent import Accent
from ui.env import *
import os

class Recognizer ():

    def __init__ (self, type):
        self.__positions = []
        self.__letters = list(Letter(None).valid_letters())
        self.__symbols = list(Symbol(None).valid_symbols())
        self.__punctuations = list(Punctuation(None).valid_punctuations())
        self.__extendeds = list(Extended(None).valid_extendeds())
        self.__accents = list(Accent(None).valid_accents())
        self.__all_characters = self.__letters + self.__symbols + \
            self.__punctuations + self.__extendeds + self.__accents
        self.valid_characters = []
        self.change_type(type);
        # If data/current/ directory is empty, put the default files in it
        if len(os.listdir('engine/data/current/')) < len(self.__all_characters):
            missing_characters = []
            for char in self.__all_characters:
                c = Character(char)
                c.load_positions()
                if c.positions is None:
                    missing_characters.append(char)
            self.reset_default_all_positions(missing_characters)

    def recognize (self, positions):
        """ Return the character recognized (or (?)) """
        self.__positions = positions.copy()
        self.__clean_none_positions()
        self.__stretch_positions()
        self.__delete_doublons()
        self.__fill_holes()
        self.__delete_doublons()
        self.__adjust_positions_number()
        self.__print_draw()

        best = self.__best_match()
        if best is None:
            return '(?)'
        else:
            return best.val

    def learn_from_positions (self, character):
        """ Tell the program the good character and save it for future
            recognition """
        for char in self.valid_characters:
            if char.val == character:
                char.set_positions(self.__positions)
                char.save_positions()
                break

    def reset_default_all_positions (self, characters = None):
        """ Delete all characters files (if characters is None) or only the
            positions of the characters (in array characters) to reset the
            positions """
        for char in self.__all_characters:
            if (characters is None) or (char in characters):
                Character(char).reset_default_positions()
                for c in self.valid_characters:
                    if (c.val == char):
                        c.load_positions()

    def change_type (self, type):
        """ Change the type with changing characters in self.valid_characters
            and load them """
        if type == 'letter':
            self.valid_characters = self.__letters.copy()
            for key, c in enumerate(self.valid_characters):
                self.valid_characters[key] = Letter(c)
                self.valid_characters[key].load_positions()
        elif type == 'symbol':
            self.valid_characters = self.__symbols.copy()
            for key, c in enumerate(self.valid_characters):
                self.valid_characters[key] = Symbol(c)
                self.valid_characters[key].load_positions()
        elif type == 'punctuation':
            self.valid_characters = self.__punctuations.copy()
            for key, c in enumerate(self.valid_characters):
                self.valid_characters[key] = Punctuation(c)
                self.valid_characters[key].load_positions()
        elif type == 'extended':
            self.valid_characters = self.__extendeds.copy()
            for key, c in enumerate(self.valid_characters):
                self.valid_characters[key] = Extended(c)
                self.valid_characters[key].load_positions()
        elif type == 'accent':
            self.valid_characters = self.__accents.copy()
            for key, c in enumerate(self.valid_characters):
                self.valid_characters[key] = Accent(c)
                self.valid_characters[key].load_positions()

    def __clean_none_positions (self):
        """ Remove the None values from the array """
        for key, (x, y) in enumerate(self.__positions):
            if (x is None) or (y is None):
                del self.__positions[key]

    def __stretch_positions (self):
        """ Change the coords to scale them (adjust and center) in a
            STRETCH_SIZE of size area """
        min_pos_x, max_pos_x, min_pos_y, max_pos_y = None, None, None, None
        assert len(self.__positions) > 1
        for x, y in self.__positions:
            if (min_pos_x is None) or (x < min_pos_x):
                min_pos_x = x
            if (max_pos_x is None) or (x > max_pos_x):
                max_pos_x = x
            if (min_pos_y is None) or (y < min_pos_y):
                min_pos_y = y
            if (max_pos_y is None) or (y > max_pos_y):
                max_pos_y = y

        left_diff = min_pos_x
        right_diff = DRAWING_AREA_SIZE - max_pos_x
        top_diff = min_pos_y
        bottom_diff = DRAWING_AREA_SIZE - max_pos_y;
        height = DRAWING_AREA_SIZE - top_diff - bottom_diff
        width = DRAWING_AREA_SIZE - left_diff - right_diff
        size_ratio = STRETCH_SIZE / DRAWING_AREA_SIZE

        if width == 0:
            width = 1
        if height == 0:
            height = 1

        if (width / height) < 0.15:
            # hack for 1, i and SHIFT
            left_diff = 0
            right_diff = 0
            width = DRAWING_AREA_SIZE
            new_x = math.floor(DRAWING_AREA_SIZE * 0.4) if \
                self.__positions[0][1] < self.__positions[-1][1] else \
                math.floor(DRAWING_AREA_SIZE * 0.6)
            for key in range(len(self.__positions)):
                self.__positions[key] = (new_x, self.__positions[key][1])
        elif (height / width) < 0.15:
            # hack for SPACE and BACK-SPACE
            top_diff = 0
            bottom_diff = 0
            height = DRAWING_AREA_SIZE
            new_y = math.floor(DRAWING_AREA_SIZE * 0.4) if \
                self.__positions[0][0] < self.__positions[-1][0] else \
                math.floor(DRAWING_AREA_SIZE * 0.6)
            for key in range(len(self.__positions)):
                self.__positions[key] = (self.__positions[key][0], new_y)

        for key, (x, y) in enumerate(self.__positions):
            try:
                x_relative_pos = (x - left_diff) / width
            except ArithmeticError: # zero division error
                x_relative_pos = 1
            try:
                y_relative_pos = (y - top_diff) / height
            except ArithmeticError: # zero division error
                y_relative_pos = 1

            new_x = math.floor((x + right_diff * x_relative_pos - left_diff * \
                (1 - x_relative_pos)) * size_ratio)
            new_y = math.floor((y + bottom_diff * y_relative_pos - top_diff * \
               (1 - y_relative_pos)) * size_ratio)
            self.__positions[key] = new_x, new_y

    def __fill_holes (self):
        """ Add new positions to avoid any hole between 2 positions """
        new_positions = []
        last_pos = (None, None)
        for (x, y) in self.__positions:
            if last_pos is not (None, None):
                x_diff = x - last_pos[0]
                y_diff = y - last_pos[1]
                if (math.fabs(x_diff) > 1) or (math.fabs(y_diff) > 1):
                    next_x = last_pos[0]
                    next_y = last_pos[1]

                    add_x = 1 if math.fabs(x_diff) >= math.fabs(y_diff) \
                              else x_diff / (y_diff if y_diff != 0 else x_diff)
                    if (x_diff * add_x) < 0:
                        add_x *= -1
                    add_y = 1 if math.fabs(y_diff) >= math.fabs(x_diff) \
                              else y_diff / (x_diff if x_diff != 0 else y_diff)
                    if (y_diff * add_y) < 0:
                        add_y *= -1

                    counter = 0
                    while True:
                        increase_x = ((next_x < x) and (x_diff > 0)) or \
                                     ((next_x > x) and (x_diff < 0))
                        increase_y = ((next_y < y) and (y_diff > 0)) or \
                                     ((next_y > y) and (y_diff < 0))
                        if increase_x and increase_y:
                            if (counter % 2) == 0:
                                next_x += add_x
                            else:
                                next_y += add_y
                        elif increase_x:
                            next_x += add_x
                        elif increase_y:
                            next_y += add_y
                        else:
                            break
                        new_positions.append((math.floor(next_x),
                                              math.floor(next_y)))
                        counter += 1
            new_positions.append((x, y))
            last_pos = (x, y)
        self.__positions = new_positions

    def __adjust_positions_number (self):
        """ Add or remove some positions to have exactly ADJUST_POS_NUMBER
            positions (to compare them easier) """
        size = len(self.__positions)
        diff = int(math.fabs(size - ADJUST_POS_NUMBER))
        if diff > 0:
            incr = size / diff
            k = incr
            for i in range(0, diff):
                q = math.floor(k)
                if q < 1:
                    q = 1
                elif q >= size:
                    q = size - 1

                if size < ADJUST_POS_NUMBER:
                    xMoy = (self.__positions[q-1][0] + self.__positions[q][0]) \
                        // 2
                    yMoy = (self.__positions[q-1][1] + self.__positions[q][1]) \
                        // 2
                    self.__positions.insert(q, (xMoy, yMoy))
                    size += 1
                    k += 1
                elif size > ADJUST_POS_NUMBER:
                    self.__positions.remove(self.__positions[q])
                    size -= 1
                    k -= 1
                k += incr

    def __best_match (self):
        """ Return the most probable character (with comparison of
            positions) """
        best_char = None
        best_diff = None
        for char in self.valid_characters:
            if char.positions is None:
                continue
            diff = 0
            pos_len = len(self.__positions)
            for key, (x, y) in enumerate(char.positions):
                if pos_len <= key:
                    break
                diff += math.fabs(x - self.__positions[key][0]) + \
                    math.fabs(y - self.__positions[key][1])
            if (best_diff is None) or (diff < best_diff):
                best_char = char
                best_diff = diff
        return best_char

    def __delete_doublons (self):
        """ Delete doublons is self.__positions and keep the correct order """
        new_positions = []
        for (x, y) in self.__positions:
            if (x, y) not in new_positions:
                new_positions.append((x, y))
        self.__positions = new_positions

    def __print_draw (self):
        """ Print the positions """
        print()
        for i in range(STRETCH_SIZE + 2):
            print('-', end = '')
        for i in range(STRETCH_SIZE):
            print('\n|', end = '')
            for j in range(STRETCH_SIZE):
                if (j, i) in self.__positions:
                    print('*', end = '')
                else:
                    print(' ', end = '')
            print('|', end = '')
        print()
        for i in range(STRETCH_SIZE + 2):
            print('-', end = '')
        print()
