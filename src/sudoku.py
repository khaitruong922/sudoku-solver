from typing import Dict, Iterable, List, Set


from src.util import *
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

    def get_cell(self, r: int, c: int):
        return self.cells[cell_index(r, c)]

    def set_cell(self, r: int, c: int, value: int):
        if not valid_cell_value(value):
            raise InvalidCellValue()

        new_sudoku = Sudoku(self.cells.copy())
        new_sudoku.cells[cell_index(r, c)] = value
        if not new_sudoku.valid:
            return

        self.cells[cell_index(r, c)] = value

    def place_cell(self, i: int, value: int):
        self.cells[i] = value
        self.candidates[i] = set()
        self.eliminate_candidates(value, i)

    def unset_cell(self, r: int, c: int):
        self.set_cell(r, c, 0)

    def row(self, r: int):
        return self.cells[r * 9:r * 9 + 9]

    def column(self, c: int):
        return self.cells[c::9]

    def box(self, n: int):
        block_r = n // 3
        block_c = n % 3
        c_start = block_c * 3
        c_end = c_start + 3
        cells = []
        for r in range(block_r * 3, block_r * 3 + 3):
            cells.extend(self.row(r)[c_start:c_end])
        return cells

    def eliminate_candidates(self, value: int, i: int = None, r: int = None, c: int = None, b: int = None):
        if value == 0:
            return
        if i is not None:
            r, c, b = position(i)
        if r is not None:
            self.eliminate_candidates_of_indices(row_indices(r), value)
        if c is not None:
            self.eliminate_candidates_of_indices(column_indices(c), value)
        if b is not None:
            self.eliminate_candidates_of_indices(box_indices(b), value)

    def eliminate_candidates_of_indices(self, indices: List[str], value: int):
        for i in indices:
            self.candidates[i].discard(value)

    def compute_candidates(self, i: int = None):
        if i is None:
            for i in range(81):
                self.compute_candidates(i)
            return
        r, c, b = position(i)
        if self.cells[i] != 0:
            return
        row = set(self.row(r))
        column = set(self.column(c))
        box = set(self.box(b))
        candidates = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        candidates = candidates - row - column - box
        self.candidates[i] = candidates
        return candidates

    def solve_naked_singles(self):
        '''
            Solve naked singles in all cells. Repeat until no more naked singles are found.

            Can solve up to `Easy`
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
            Solve hidden singles in row, column and box. Repeat until no more hidden singles are found.

            Superior to `solve_naked_singles`

            Can solve up to `Medium`
        '''
        cnt = 0
        for i in range(9):
            cnt += self.solve_hidden_singles_of_indices(box_indices(i))
            cnt += self.solve_hidden_singles_of_indices(row_indices(i))
            cnt += self.solve_hidden_singles_of_indices(column_indices(i))

        if cnt > 0:
            self.solve_hidden_singles()
        return cnt

    def solve_hidden_singles_of_indices(self, indices: List[str]):
        '''
            Find a cell with unique candidate in a list of cells.
        '''
        candidates_sets: List[Set[int]] = [self.candidates[i] for i in indices if len(self.candidates[i]) >= 1]

        if len(candidates_sets) == 0:
            return 0

        cnt = 0
        for i in indices:
            if self.cells[i] != 0:
                continue
            candidates = set(self.candidates[i])

            # Check if it has a unique candidate in the box
            if len(candidates) > 1:
                other_sets = [s for s in candidates_sets if s is not self.candidates[i]] or [set()]
                other_candidates = set.union(*other_sets)
                candidates -= other_candidates

            # If it has a unique candidate, place it
            if len(candidates) == 1:
                cnt += 1
                self.place_cell(i, candidates.pop())
        return cnt

    def count_candidates(self, indices: Iterable[int]) -> Dict[int, int]:
        d = {}
        sets = [self.candidates[i] for i in indices]
        for s in sets:
            for n in s:
                d[n] = d.get(n, 0) + 1
        return d

    def eliminate_hidden_directions(self):
        """
            For each column in each box, check if they have numbers that does not belong to other columns in the box, 
            then eliminate candidates of that number in that column of other boxes.

            Same applied for rows.
        """
        for b in range(9):
            bi = box_indices(b)
            box_candidates_count = self.count_candidates(bi)

            # Scan rows in box
            for _r in range(3):
                rbi = query_indices(r=_r, b=b)
                r = b // 3 * 3 + _r
                ri = row_indices(r=r)
                rb_candidates_count = self.count_candidates(rbi)
                other_rb_indices = list(set(ri) - set(rbi))
                for k, v in rb_candidates_count.items():
                    if box_candidates_count[k] == v:
                        self.eliminate_candidates_of_indices(other_rb_indices, k)

            # Scan columns in box
            for _c in range(3):
                cbi = query_indices(c=_c, b=b)
                c = b % 3 * 3 + _c
                ci = column_indices(c=c)
                cb_candidates_count = self.count_candidates(cbi)
                other_cb_indices = list(set(ci) - set(cbi))
                for k, v in cb_candidates_count.items():
                    if box_candidates_count[k] == v:
                        self.eliminate_candidates_of_indices(other_cb_indices, k)

    def solve_hidden_directions(self):
        """
            Use eliminate_hidden_directions to eliminate candidates in each row and column, then use solve_hidden_singles. 
            Repeat until no more squares can be solved.

            Superior to `solve_hidden_singles`

            Can solve up to `Hard`
        """
        self.eliminate_hidden_directions()
        cnt = self.solve_hidden_singles()
        if cnt > 0:
            self.solve_hidden_directions()
        return cnt

    def solve(self):
        self.display_state()
        self.compute_candidates()
        print("Solving...")
        self.solve_hidden_directions()
        self.display_state()
        print()
        return self

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

    def display(self):
        for r1 in range(3):
            for r2 in range(3):
                r = r1 * 3 + r2
                self.display_row(r)
            if r1 < 2:
                print("------+-------+------")
        print()

    def display_row(self, r: int):
        row = self.row(r)
        for i in range(3):
            for j in range(3):
                s = str(row[i * 3 + j])
                s = s.replace("0", "_")
                print(s, end=" ")
            if i < 2:
                print("|", end=" ")
        print()

    def display_candidates(self):
        def display_set(i: int):
            print("".join(str(n) for n in self.candidates[i]).center(10), end=" ")
        for r1 in range(3):
            for r2 in range(3):
                r = r1 * 3 + r2
                for c1 in range(3):
                    for c2 in range(3):
                        c = c1 * 3 + c2
                        i = cell_index(r, c)
                        display_set(i)
                    if c1 < 2:
                        print("|", end=" ")
                print()
            if r1 < 2:
                print("-" * 33 + "+" + "-" * 34 + "+" + "-" * 33)

    def display_state(self):
        self.display()
        if not self.valid:
            print("Invalid!")
        if self.solved:
            print("Solved!")
