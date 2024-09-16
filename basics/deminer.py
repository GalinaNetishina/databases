import random
from collections import namedtuple

cell_cord = namedtuple('cord', ['i', 'j'])


class Cell:
    __slots__ = ['around_mines', 'mine', 'fl_open', 'cords']

    def __init__(self, around_mines: int, mine: bool, cords: cell_cord):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False
        self.cords = cords

    def __repr__(self):
        if not self.fl_open:
            return '#'
        if self.mine:
            return '*'
        return str(self.around_mines)


class GameOver(Exception):
    pass


class GamePole:
    def __init__(self, n: int, m: int):
        self.size = n
        self.pole = [[Cell(0, False, cell_cord(i, j))
                     for i in range(n)]
                     for j in range(n)]
        self.init(m)

    def init(self, m: int):
        for cord in random.sample(range(self.size**2), m):
            i, j = cord // self.size, cord % self.size
            self.set_mine(self.pole[i][j])

    def set_mine(self, cell):
        cell.mine = True
        for cell in self.get_neighbours(cell.cords):
            cell.around_mines += 1

    def get_neighbours(self, cord: cell_cord):
        i, j = cord
        res = ((i - 1, j),
               (i + 1, j),
               (i + 1, j - 1),
               (i - 1, j - 1),
               (i - 1, j + 1),
               (i + 1, j + 1),
               (i, j + 1),
               (i, j - 1))
        yield from (self.pole[i][j]
                    for i, j in res
                    if (0 <= i < self.size)
                    and (0 <= j < self.size)
                    )

    def open(self, cord: cell_cord):
        i, j = cord
        cell = self.pole[i][j]
        if cell.mine:
            raise GameOver('GameOver! You exploded')
        cell.fl_open = True
        if cell.around_mines == 0:
            for cell in self.get_neighbours(cell.cords):
                if not cell.around_mines:
                    cell.fl_open = True
        self.show()

    def show(self):
        for row in self.pole:
            print(*row)


if __name__ == "__main__":
    pole_game = GamePole(10, 12)
    while input('Play? Enter anything to agree or be silent\n'):
        try:
            while True:
                cord = map(lambda x: int(x) - 1, input('enter cords for checking(i, j from 1 to 10)\n').split(' '))
                pole_game.open(cord)
        except Exception:
                print(Exception)

