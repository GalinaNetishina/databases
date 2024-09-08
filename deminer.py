import random


class Cell:
    __slots__ = ['around_mines', 'mine', 'fl_open']

    def __init__(self, around_mines: int, mine: bool):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False


class GamePole:
    def __init__(self, n: int, m: int):
        self.size = n
        self.pole = [[Cell(0, False) for _ in range(n)]
                     for _ in range(n)]
        self.init(m)

    def init(self, m):
        mined = random.sample(range(self.size**2), m)
        for i in mined:
            cell_cord = i // self.size, i % self.size
            self.mark(cell_cord)

    def get_neighbours(self, cell_cord: tuple[int, int]):
        i, j = cell_cord
        res = ((i - 1, j),
               (i + 1, j),
               (i + 1, j - 1),
               (i - 1, j - 1),
               (i - 1, j + 1),
               (i + 1, j + 1),
               (i, j + 1),
               (i, j - 1))
        yield from (self.pole[i][j] for i, j in res
                    if (0 <= i < self.size) and (0 <= j < self.size))

    def mark(self, cell_cord: tuple[int, int]):
        i, j = cell_cord
        self.pole[i][j].mine = True
        for cell in self.get_neighbours(cell_cord):
            cell.around_mines += 1

    def show(self):
        for row in self.pole:
            # print(*('#' if not cell.fl_open else '*' if cell.mine else cell.around_mines for cell in row))
            print(*('*' if cell.mine else cell.around_mines or "#" for cell in row))


if __name__ == "__main__":
    pole_game = GamePole(10, 12)
    pole_game.show()
