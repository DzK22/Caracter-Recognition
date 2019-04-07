import math
from engine.character import Character
from ui.env import *

class Recognizer ():

    def __init__ (self):
        self.positions = []
        self.characters = []
        for c in CHARACTERS_LIST:
            self.characters.append(Character(c))
            self.characters[-1].load_positions()

    def recognize (self, positions):
        """ Return the character recognized (or ?) """
        self.positions = positions
        self.clean_extra_positions()
        self.stretch_positions()
        self.adjust_positions_number()

        best = self.best_match()
        if (best is None):
            return '?'
        else:
            return best.val

    def clean_extra_positions (self):
        """ Remove every position which is too closer with another """
        new_positions = []
        min_diff = DRAWING_AREA_SIZE // 100
        last_pos = None, None

        for key, (x, y) in enumerate(self.positions):
            if ((x, y) == (None, None)):
                continue
            none_neighbour = (last_pos == (None, None)) or \
                             (self.positions[key + 1] == (None, None))
            diff_ok = (not none_neighbour) and \
                      (math.fabs(x - last_pos[0]) >= min_diff) and \
                      (math.fabs(y - last_pos[1]) >= min_diff)
            if (none_neighbour or diff_ok):
                last_pos = x, y
                new_positions.append(last_pos)
        self.positions = new_positions

    def stretch_positions (self):
        """ Change the coords to scale them in a 100x100 area """
        new_size = 100
        min_pos_x, max_pos_x, min_pos_y, max_pos_y = None, None, None, None
        for x, y in self.positions:
            if ((min_pos_x is None) or (x < min_pos_x)):
                min_pos_x = x
            if ((max_pos_x is None) or (x > max_pos_x)):
                max_pos_x = x
            if ((min_pos_y is None) or (y < min_pos_y)):
                min_pos_y = y
            if ((max_pos_y is None) or (y > max_pos_y)):
                max_pos_y = y

        left_diff = min_pos_x
        right_diff = DRAWING_AREA_SIZE - max_pos_x
        top_diff = min_pos_y
        bottom_diff = DRAWING_AREA_SIZE - max_pos_y;

        for key, (x, y) in enumerate(self.positions):
            try:
                x_relative_pos = (x - left_diff) / \
                                 (DRAWING_AREA_SIZE - left_diff - right_diff)
            except ArithmeticError:
                x_relative_pos = 1
            new_x = math.floor((x + right_diff * x_relative_pos - \
                                left_diff * (1 - x_relative_pos)) * \
                                (new_size / DRAWING_AREA_SIZE))
            try:
                y_relative_pos = (y - top_diff) / \
                                 (DRAWING_AREA_SIZE - top_diff - bottom_diff)
            except ArithmeticError:
                y_relative_pos = 1
            new_y = math.floor((y + bottom_diff * y_relative_pos - top_diff *
                               (1 - y_relative_pos)) * \
                               (new_size / DRAWING_AREA_SIZE))
            self.positions[key] = new_x, new_y

    def adjust_positions_number (self):
        """ Add or remove some positions to have exactly 20 positions (to
            compare them easier) """
        number = 20
        size = len(self.positions)
        diff = int(math.fabs(size - number))
        if (diff > 0):
            k = size // diff - 1
            for i in range(0, diff):
                if (size < number):
                    self.positions.insert(k, self.positions[k])
                elif (size > number):
                    self.positions.remove(self.positions[k])
                k += size // diff - 1
            assert len(self.positions) == number

    def best_match (self):
        """ Return the most probable character (with comparison of
            positions) """
        best_char = None
        best_diff = None
        for char in self.characters:
            if char.positions is None:
                continue
            diff = 0
            for (key, (x, y)) in enumerate(char.positions):
                if (len(self.positions) <= key):
                    break
                diff += math.fabs(x - self.positions[key][0] + y - \
                                  self.positions[key][1])
            if ((best_diff is None) or (diff < best_diff)):
                best_char = char
                best_diff = diff
        return best_char

    def learn_from_positions (self, character):
        """ Tell the program the good character and save it for future
            recognition """
        for char in self.characters:
            if (char.val == character):
                char.set_positions(self.positions)
                char.save_positions()
                break

    def reset_all_positions (self):
        """ Delete all character files to reset the positions """
        for char in self.characters:
            if (char.positions is not None):
                char.delete_positions()
                char.positions = None
