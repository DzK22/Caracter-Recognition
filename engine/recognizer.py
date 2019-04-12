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
        min_dist = DRAWING_AREA_SIZE // 40
        last_pos = None, None

        for key, (x, y) in enumerate(self.positions):
            if ((x, y) == (None, None)):
                continue
            none_neighbour = (last_pos == (None, None)) or \
                             (self.positions[key + 1] == (None, None))
            dist_ok = (not none_neighbour) and \
                      (math.sqrt(math.pow(x - last_pos[0], 2) + \
                                 math.pow(y - last_pos[1], 2)) >= min_dist)
            if (none_neighbour or dist_ok):
                last_pos = x, y
                new_positions.append(last_pos)
        self.positions = new_positions

    def stretch_positions (self):
        """ Change the coords to scale them (adjust and center) in a 100x100
            area """
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
            except ArithmeticError: # zero division error
                x_relative_pos = 1
            try:
                y_relative_pos = (y - top_diff) / \
                                 (DRAWING_AREA_SIZE - top_diff - bottom_diff)
            except ArithmeticError: # zero division error
                y_relative_pos = 1

            new_x = math.floor((x + right_diff * x_relative_pos - \
                                left_diff * (1 - x_relative_pos)) * \
                                (new_size / DRAWING_AREA_SIZE))
            new_y = math.floor((y + bottom_diff * y_relative_pos - top_diff *
                               (1 - y_relative_pos)) * \
                               (new_size / DRAWING_AREA_SIZE))
            self.positions[key] = new_x, new_y
        print('\n@@@ STRETCH POSITIONS @@@\n')
        self.print_draw(100)

    def adjust_positions_number (self):
        """ Add or remove some positions to have exactly 40 positions (to
            compare them easier) """
        number = 60
        size = len(self.positions)
        diff = int(math.fabs(size - number))
        incr = size / diff
        k = incr
        if (diff > 0):
            for i in range(0, diff):
                q = math.floor(k)
                if q < 1:
                    q = 1
                elif q >= size:
                    q = size - 1

                if (size < number):
                    xMoy = (self.positions[q-1][0] + self.positions[q][0]) // 2
                    yMoy = (self.positions[q-1][1] + self.positions[q][1]) // 2
                    self.positions.insert(q, (xMoy, yMoy))
                    size += 1
                    k += 1
                elif (size > number):
                    self.positions.remove(self.positions[q])
                    size -= 1
                    k -= 1
                k += incr
            assert len(self.positions) == number
        print('\n@@@ ADJUST POSITIONS NUMBER @@@\n')
        self.print_draw(100)

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

    def print_draw (self, max):
        for j in range(max):
            print('\n|', end = '')
            for i in range(max):
                if ((i, j) in self.positions):
                    print('*', end = '')
                else:
                    print(' ', end = '')
            print('|', end = '')
