from typing import List, Set

from src.exceptions import InvalidCellValue, InvalidSudoku


class Sudoku:
    def __init__(self, cells: List[int] = None):
        if cells is None:
            cells = [0] * 81
        self.set_cells(cells)
        self.candidates = [set() for _ in range(81)]

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

    def place_cell(self, i: int, value: int):
        self.cells[i] = value
        self.candidates[i] = set()
        self.eliminate_candidates(value, i)

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

    def eliminate_candidates(self, value: int, i: int = None, y: int = None, x: int = None, b: int = None):
        if value == 0:
            return
        if i is not None:
            y, x, b = position(i)
        for k in box_indices(b):
            self.candidates[k].discard(value)
        for k in row_indices(y):
            self.candidates[k].discard(value)
        for k in column_indices(x):
            self.candidates[k].discard(value)

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

    def compute_candidates(self, i: int = None):
        if i is None:
            for i in range(81):
                self.compute_candidates(i)
            return
        y, x, b = position(i)
        if self.cells[i] != 0:
            return
        row = set(self.row(y))
        column = set(self.column(x))
        box = set(self.box(b))
        candidates = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        candidates = candidates - row - column - box
        self.candidates[i] = candidates
        return candidates

    def solve_naked_singles(self):
        '''
            Solve naked singles in all cells.   
            Can solve: Easy
        '''
        i = 0
        cnt = 0
        for i in range(81):
            if self.cells[i] == 0:
                candidates = list(self.candidates[i])
                if len(candidates) == 1:
                    cnt += 1
                    self.place_cell(i, candidates[0])
        if cnt > 0:
            self.solve_naked_singles()

    def solve_hidden_singles(self):
        '''
            Solve hidden singles in row, column and box.
            Superior to solve_naked_singles()
            Can solve: Medium
        '''
        cnt = 0
        for i in range(9):
            cnt += self.solve_hidden_singles_of_indices(box_indices(i))
            cnt += self.solve_hidden_singles_of_indices(row_indices(i))
            cnt += self.solve_hidden_singles_of_indices(column_indices(i))
        if cnt > 0:
            self.solve_hidden_singles()

    def solve_hidden_singles_of_indices(self, indices: List[str]):
        '''
            Find a cell with unique candidate in a list of cells.
        '''
        candidates_sets: List[Set[int]] = [self.candidates[i] for i in indices if len(self.candidates[i]) >= 1]

        if len(candidates_sets) == 0:
            return 0

        cnt = 0
        for i in indices:
            other_sets = [s for s in candidates_sets if s is not self.candidates[i]] or [set()]
            other_candidates = set.union(*other_sets)
            unique_candidates = self.candidates[i] - other_candidates
            if len(unique_candidates) == 1:
                cnt += 1
                self.place_cell(i, unique_candidates.pop())
        return cnt

    def solve(self):
        self.display_state()
        self.compute_candidates()
        # self.solve_naked_single()
        # self.display_state()
        self.solve_hidden_singles()
        self.display_state()

    def display_state(self):
        self.display()
        if not self.valid:
            print("Invalid!")
        if self.solved:
            print("Solved!")

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


def row_indices(y: int):
    return [y * 9 + i for i in range(9)]


def column_indices(x: int):
    return [i * 9 + x for i in range(9)]


def box_indices(n: int):
    block_y = n // 3
    block_x = n % 3
    x_start = block_x * 3
    x_end = x_start + 3
    y_start = block_y * 3
    y_end = y_start + 3
    return [cell_index(y, x) for y in range(y_start, y_end) for x in range(x_start, x_end)]


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
