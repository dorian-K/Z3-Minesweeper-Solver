import random

class Minesweeper:

    def __init__(self) -> None:
        self.field_size = 20 # square
        self.field_mines = [] # 1 = mine, 0 = empty
        self.field_mask = [] # 1 = hidden, 0 = visible
        self.field_values = [] # number of mine neighbours, 'values'

    def generate_mines(self):
        # initialize minefield
        for x in range(self.field_size):
            col = []
            for y in range(self.field_size):
                has_mine = random.uniform(0, 1) > 0.8
                if x == 0 and y == 0:
                    has_mine = False # always keep the upper left corner free for the initial move
                if has_mine:
                    col.append(1)
                else:
                    col.append(0)
            self.field_mines.append(col)

            # fill mask with 1s
            self.field_mask.append([1 for i in range(self.field_size)])

        # now compute the neighbouring values
        for x in range(self.field_size):
            col = []
            for y in range(self.field_size):
                neighbours = self.get_neighbours(x, y)
                if self.is_mine(x, y):
                    col.append(0)
                else:
                    col.append(sum([self.is_mine(pos[0], pos[1]) for pos in neighbours]))
            self.field_values.append(col)
    
    def coord_to_hash(self, x, y):
        return x * self.field_size + y

    def hash_to_coord(self, hash):
        return (hash // self.field_size, hash % self.field_size)

    def is_mine(self, x, y):
        return self.field_mines[x][y] == 1

    def is_masked(self, x, y):
        return self.field_mask[x][y] == 1

    def get_neighbours(self, x, y, only_masked=False):
        n = []
        for rel_x in range(-1, 2):
            for rel_y in range(-1, 2):
                if rel_x == 0 and rel_y == 0:
                    continue
                if not (0 <= x + rel_x < self.field_size) or not (0 <= y + rel_y < self.field_size):
                    continue # outside the field
                if only_masked and self.field_mask[x + rel_x][y + rel_y] == 0:
                    continue # do not add unmasked neighbours
                n.append((x + rel_x, y + rel_y))
        return n

    def print_field(self, non_masked_only=False):
        for y in range(self.field_size):
            line = ""
            for x in range(self.field_size):
                if non_masked_only and self.is_masked(x, y) == 1:
                    line += ' '
                elif self.is_mine(x, y):
                    line += 'M'
                else:
                    line += str(self.field_values[x][y]) 
                line += ' '
            print(line)

    def unmask_pos(self, x, y): 
        if not self.is_masked(x, y):
            raise Exception("Pos already unmasked!")
        self.field_mask[x][y] = 0
        if self.is_mine(x, y):
            raise Exception("Unmasked a mine!!, at "+str(x)+" "+str(y))

    def is_game_done(self):
        for x in range(self.field_size):
            for y in range(self.field_size):
                if self.is_mine(x, y):
                    continue
                if self.is_masked(x, y):
                    return False
        return True