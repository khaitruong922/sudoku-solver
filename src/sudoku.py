from typing import List

from src.exceptions import InvalidCellValue, InvalidSudoku


class Sudoku:
    def __init__(self, cells: List[int] = None):
        if cells is None:
            cells = [0] * 81
        self.set_cells(cells)

    def set_cells(self, cells: List[int]):
        if len(cells) != 81:
            raise InvalidSudoku()

        for cell in cells:
            if not valid_cell_value(cell):
                raise InvalidCellValue()

        self.cells = cells

    def get_cell(self, y: int, x: int):
        return self.cells[cell_index(y, x)]

    def set_cell(self, y: int, x: int, value: int):
        if not valid_cell_value(value):
            raise InvalidCellValue()

        new_sudoku = Sudoku(self.cells.copy())
        new_sudoku.cells[cell_index(y, x)] = value
        if not new_sudoku.valid:
            return

        self.cells[cell_index(y, x)] = value

    def unset_cell(self, y: int, x: int):
        self.set_cell(y, x, 0)

    def row(self, y: int):
        return self.cells[y * 9:y * 9 + 9]

    def column(self, x: int):
        return self.cells[x::9]

    def box(self, n: int):
        block_y = n // 3
        block_x = n % 3
        x_start = block_x * 3
        x_end = x_start + 3
        cells = []
        for y in range(block_y * 3, block_y * 3 + 3):
            cells.extend(self.row(y)[x_start:x_end])
        return cells

    def display(self):
        for y1 in range(3):
            for y2 in range(3):
                y = y1 * 3 + y2
                self.display_row(y)
            if y1 < 2:
                print("------+-------+------")
        print()

    def display_row(self, y: int):
        row = self.row(y)
        for i in range(3):
            for j in range(3):
                s = str(row[i * 3 + j])
                s = s.replace("0", "_")
                print(s, end=" ")
            if i < 2:
                print("|", end=" ")
        print()

    def candidates(self, i: int):
        y, x, b = position(i)
        row = set(self.row(y))
        column = set(self.column(x))
        box = set(self.box(b))
        candidates = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        candidates = candidates - row - column - box
        return candidates

    def solve_unique_candidates(self):
        i = 0
        cnt = 0
        while i < 81:
            if self.cells[i] == 0:
                candidates = self.candidates(i)
                if len(candidates) == 1:
                    cnt += 1
                    self.cells[i] = candidates.pop()
                    i = 0
                    continue
            i += 1
        print("Solved unique candidates:", cnt)

    def solve(self):
        print("Sudoku:")
        self.display_state()
        self.solve_unique_candidates()
        self.display_state()

    def display_state(self):
        self.display()
        if not self.valid:
            print("Sudoku invalid!")
        if self.solved:
            print("Sudoku solved!")

    @property
    def valid(self):
        for i in range(9):
            column = [v for v in self.column(i) if v != 0]
            box = [v for v in self.box(i) if v != 0]
            row = [v for v in self.row(i) if v != 0]

            if len(set(column)) != len(column):
                return False
            if len(set(box)) != len(box):
                return False
            if len(set(row)) != len(row):
                return False
        return True

    @property
    def solved(self):
        return self.valid and all(v != 0 for v in self.cells)

    @classmethod
    def from_file(cls, filename: str):
        sudoku = cls()
        sudoku.set_cells(load_cells_from_file(filename))
        return sudoku


def valid_cell_value(n: int):
    return n >= 0 and n <= 9


def cell_index(y: int, x: int):
    return y * 9 + x


def position(i: int):
    y = i // 9
    x = i % 9
    box = y // 3 * 3 + x // 3
    return y, x, box


def load_cells_from_file(filename: str):
    cells = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        if len(lines) != 9:
            raise ValueError('File must contain exactly 9 lines')
        for line in lines:
            line = line.replace(" ", "").strip()
            if len(line) != 9:
                raise ValueError('Each line must contain exactly 9 numbers')
            for c in line:
                if not c.isdigit():
                    raise ValueError('Each cell must be a number')
                cells.append(int(c))
    return cells