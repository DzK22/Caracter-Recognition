import math
from engine.scoreCharacters import *
from ui.env import *

class LetterRecognizer ():

    def __init__ (self):
        self.letter = 'A'
        self.cursor_positions = []

    def calculate (self, old_cursor_positions):
        # delete extra amount of positions
        self.cursor_positions.clear()
        self.clean_extra_positions(old_cursor_positions)
        self.stretch_positions()
        assert len(self.cursor_positions) >= 2
        score = self.gen_score()
        print('gen score = ' + str(score))

        closestDiff, closestChar = None, None
        for key, val in SCORE_CHARACTERS.items():
            diff = math.fabs(score - val)
            if ((closestDiff is None) or (diff < closestDiff)):
                closestDiff, closestChar = diff, key

        self.letter = closestChar

    def clean_extra_positions (self, old_cursor_positions):
        min_diff = DRAWING_AREA_SIZE // 40
        last_pos = None, None

        for key, (x, y) in enumerate(old_cursor_positions):
            if ((x, y) == (None, None)):
                continue
            none_neighbour = (last_pos == (None, None)) or (old_cursor_positions[key + 1] == (None, None))
            diff_ok = (not none_neighbour) and (math.fabs(x - last_pos[0]) >= min_diff) and (math.fabs(y - last_pos[1]) >= min_diff)
            if (none_neighbour or diff_ok):
                last_pos = x, y
                self.cursor_positions.append(last_pos)

    def stretch_positions (self):
        new_size = 100
        min_pos_x, max_pos_x, min_pos_y, max_pos_y = None, None, None, None
        for x, y in self.cursor_positions:
            if ((min_pos_x is None) or (x < min_pos_x)):
                min_pos_x = x
            if ((max_pos_x is None) or (x > max_pos_x)):
                max_pos_x = x
            if ((min_pos_y is None) or (y < min_pos_y)):
                min_pos_y = y
            if ((max_pos_y is None) or (y > max_pos_y)):
                max_pos_y = y

        left_diff, right_diff, top_diff, bottom_diff = min_pos_x, DRAWING_AREA_SIZE - max_pos_x, min_pos_y, DRAWING_AREA_SIZE - max_pos_y;

        for key, (x, y) in enumerate(self.cursor_positions):
            try:
                x_relative_pos = (x - left_diff) / (DRAWING_AREA_SIZE - left_diff - right_diff)
            except ArithmeticError:
                x_relative_pos = 1
            new_x = math.floor((x + right_diff * x_relative_pos - left_diff * (1 - x_relative_pos)) * (new_size / DRAWING_AREA_SIZE))
            try:
                y_relative_pos = (y - top_diff) / (DRAWING_AREA_SIZE - top_diff - bottom_diff)
            except ArithmeticError:
                y_relative_pos = 1
            new_y = math.floor((y + bottom_diff * y_relative_pos - top_diff * (1 - y_relative_pos)) * (new_size / DRAWING_AREA_SIZE))
            self.cursor_positions[key] = new_x, new_y
            print('new pos #' + str(key) + ' = (' + str(new_x) + ', ' + str(new_y) + ')')

    def gen_score (self):
        # algorithme nul a chier, il faut trouver le bon
        score, counter = 0, 1
        lastPos = (0, 0)
        for x, y in self.cursor_positions:
            score += (x * x + lastPos[0]) * (y * y + lastPos[1]) * counter
            lastPos = lastPos[0], lastPos[1]
            counter += 1
        return score // len(self.cursor_positions)
