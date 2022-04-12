from itertools import combinations, product
from typing import Dict, Iterable, List, Set
from timeit import default_timer as timer
from src.util import *
from src.exceptions import InvalidCellValue, InvalidSudoku


class Sudoku:
    def __init__(self, cells: List[int] = None, name: str = "Sudoku"):
        if cells is None:
            cells = [0] * 81
        self.set_cells(cells)
        self.candidates = [set() for _ in range(81)]
        self.name = name

    def get_cell(self, r: int, c: int) -> int:
        return self.cells[cell_index(r, c)]

    def set_cells(self, cells: List[int]):
        if len(cells) != 81:
            raise InvalidSudoku()

        for cell in cells:
            if not valid_cell_value(cell):
                raise InvalidCellValue()

        self.cells = cells

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

    def eliminate_candidates_of_indices(self, indices: Iterable[int], value: int):
        cnt = 0
        for i in indices:
            if value in self.candidates[i]:
                self.candidates[i].remove(value)
                cnt += 1
        return cnt

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

    def solve_hidden_singles(self):
        '''
            Solve hidden singles in row, column and box. Repeat until no more hidden singles are found.
        '''

        def solve_hidden_singles_of_indices(indices: List[str]):
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

        cnt = 0
        for i in range(9):
            cnt += solve_hidden_singles_of_indices(box_indices(i))
            cnt += solve_hidden_singles_of_indices(row_indices(i))
            cnt += solve_hidden_singles_of_indices(column_indices(i))

        if cnt > 0:
            cnt += self.solve_hidden_singles()
        return cnt

    def count_candidates(self, indices: Iterable[int]) -> Dict[int, int]:
        d = {}
        sets = [self.candidates[i] for i in indices]
        for s in sets:
            for n in s:
                d[n] = d.get(n, 0) + 1
        return d

    def eliminate_pointing_pair(self):
        """
            For each column in each box, check if they have numbers that does not belong to other columns in the box,
            then eliminate candidates of that number in that column of other boxes.

            Same applied for rows.
        """
        cnt = 0
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
                        cnt += self.eliminate_candidates_of_indices(other_rb_indices, k)

            # Scan columns in box
            for _c in range(3):
                cbi = query_indices(c=_c, b=b)
                c = b % 3 * 3 + _c
                ci = column_indices(c=c)
                cb_candidates_count = self.count_candidates(cbi)
                other_cb_indices = list(set(ci) - set(cbi))
                for k, v in cb_candidates_count.items():
                    if box_candidates_count[k] == v:
                        cnt += self.eliminate_candidates_of_indices(other_cb_indices, k)
        if cnt > 0:
            cnt += self.eliminate_pointing_pair()
        return cnt

    def eliminate_hidden_subsets(self):
        """
            For each area (box, column or row), check for each subset of size k from 2 to 4, if it has k candidates that do not belong other cells in the area, 
            eliminate all other candidates that are belong to other cells in the area.
        """
        def eliminate_hidden_subsets_of_indices(indices: List[str]):
            cnt = 0
            for size in range(2, min(4, len(indices))):
                indices_subsets = list(combinations(indices, size))
                for subset_indices in indices_subsets:
                    subset_candidates = set.union(*[self.candidates[i] for i in subset_indices])
                    other_indices = list(set(indices) - set(subset_indices))
                    other_candidates = set.union(*[self.candidates[i] for i in other_indices])
                    subset_unique_candidates = subset_candidates - other_candidates
                    # If the subset (size k) has k candidates that does not belong to other cells, eliminate other candidates in the subset that belong to other cells.
                    if len(subset_unique_candidates) == size:
                        for candidate in other_candidates:
                            cnt += self.eliminate_candidates_of_indices(subset_indices, candidate)
            return cnt

        cnt = 0
        for x in range(9):
            bi = [i for i in box_indices(x) if self.cells[i] == 0]
            ri = [i for i in row_indices(x) if self.cells[i] == 0]
            ci = [i for i in column_indices(x) if self.cells[i] == 0]
            cnt += eliminate_hidden_subsets_of_indices(bi)
            cnt += eliminate_hidden_subsets_of_indices(ri)
            cnt += eliminate_hidden_subsets_of_indices(ci)

        if cnt > 0:
            cnt += self.eliminate_hidden_subsets()
        return cnt

    def eliminate_naked_subsets(self):
        """
            For each area (box, column or row), check for naked subset of size k from 2 to 4. If it has k candidates, then eliminate those candidates from other cells in the area.
        """
        def eliminate_naked_subsets_of_indices(indices: List[str]):
            cnt = 0
            for size in range(2, min(4, len(indices))):
                indices_subsets = list(combinations(indices, size))
                for subset_indices in indices_subsets:
                    subset_candidates = set.union(*[self.candidates[i] for i in subset_indices])
                    if len(subset_candidates) == size:
                        other_indices = list(set(indices) - set(subset_indices))
                        for candidate in subset_candidates:
                            cnt += self.eliminate_candidates_of_indices(other_indices, candidate)
            return cnt

        cnt = 0
        for x in range(9):
            bi = [i for i in box_indices(x) if self.cells[i] == 0]
            ri = [i for i in row_indices(x) if self.cells[i] == 0]
            ci = [i for i in column_indices(x) if self.cells[i] == 0]
            cnt += eliminate_naked_subsets_of_indices(bi)
            cnt += eliminate_naked_subsets_of_indices(ri)
            cnt += eliminate_naked_subsets_of_indices(ci)

        if cnt > 0:
            cnt += self.eliminate_naked_subsets()
        return cnt

    def eliminate_x_wings(self):
        """
            Detect x-wing in row or column then eliminate that candidate from intersecting cells.
        """
        cnt = 0
        # Detect x-wing in rows
        for r1 in range(6):
            indices = [i for i in row_indices(r1) if self.cells[i] == 0]
            columns = [i % 9 for i in indices]
            candidates_count = self.count_candidates(indices)
            column_combs = list(combinations(columns, 2))
            for k, v in candidates_count.items():
                if v != 2:
                    continue
                for c1, c2 in column_combs:
                    # Skip if the two columns are in the same box
                    if c1 // 3 == c2 // 3:
                        continue
                    if k not in self.candidates[cell_index(r1, c1)] or k not in self.candidates[cell_index(r1, c2)]:
                        continue
                    for r2 in range(r1 // 3 * 3 + 3, 9):
                        if k not in self.candidates[cell_index(r2, c1)] or k not in self.candidates[cell_index(r2, c2)]:
                            continue
                        other_row_candidates_count = self.count_candidates(row_indices(r2))
                        if other_row_candidates_count.get(k, 0) == 2:
                            c1i = set(column_indices(c1)) - {cell_index(r1, c1), cell_index(r2, c1)}
                            c2i = set(column_indices(c2)) - {cell_index(r1, c2), cell_index(r2, c2)}
                            cnt += self.eliminate_candidates_of_indices(c1i | c2i, k)

        # Detect x-wing in columns
        for c1 in range(6):
            indices = [i for i in column_indices(c1) if self.cells[i] == 0]
            rows = [i // 9 for i in indices]
            candidates_count = self.count_candidates(indices)
            row_combs = list(combinations(rows, 2))
            for k, v in candidates_count.items():
                if v != 2:
                    continue
                for r1, r2 in row_combs:
                    # Skip if the two rows are in the same box
                    if r1 // 3 == r2 // 3:
                        continue
                    if k not in self.candidates[cell_index(r1, c1)] or k not in self.candidates[cell_index(r2, c1)]:
                        continue
                    for c2 in range(c1 // 3 * 3 + 3, 9):
                        if k not in self.candidates[cell_index(r1, c2)] or k not in self.candidates[cell_index(r2, c2)]:
                            continue
                        other_column_candidates_count = self.count_candidates(column_indices(c2))
                        if other_column_candidates_count.get(k, 0) == 2:
                            r1i = set(row_indices(r1)) - {cell_index(r1, c1), cell_index(r1, c2)}
                            r2i = set(row_indices(r2)) - {cell_index(r2, c1), cell_index(r2, c2)}
                            cnt += self.eliminate_candidates_of_indices(r1i | r2i, k)

        if cnt > 0:
            cnt += self.eliminate_x_wings()
        return cnt

    def eliminate_y_wings(self):
        cnt = 0
        for i in range(81):
            if self.cells[i] != 0:
                continue
            candidates = self.candidates[i]
            if len(candidates) != 2:
                continue
            # Assume that current cell is pivot of y-wing
            r, c, b = position(i)

            pincers_column = []
            pincers_row = []
            pincers_box = []

            # Check for pincers in column
            for _r in range(0, 9):
                _b = box_of(_r, c)
                # Skip if the two cells are in the same box
                if _b == b:
                    continue
                _i = cell_index(_r, c)
                other_candidates = self.candidates[_i]
                if len(other_candidates) != 2:
                    continue
                # Take if there is one candidate in common
                if len(other_candidates & candidates) == 1:
                    pincers_column.append(_i)

            # Check for pincers in row
            for _c in range(0, 9):
                _b = box_of(r, _c)
                # Skip if the two cells are in the same box
                if _b == b:
                    continue
                _i = cell_index(r, _c)
                other_candidates = self.candidates[_i]
                if len(other_candidates) != 2:
                    continue
                # Take if there is one candidate in common
                if len(other_candidates & candidates) == 1:
                    pincers_row.append(_i)

            # Check for pincers in box
            for _r in range(r // 3 * 3, r // 3 * 3 + 3):
                for _c in range(c // 3 * 3, c // 3 * 3 + 3):
                    # Skip if the two cells are in the same column or row
                    if _r == r and _c == c:
                        continue

                    _i = cell_index(_r, _c)
                    other_candidates = self.candidates[_i]
                    if len(other_candidates) != 2:
                        continue
                    # Take if there is one candidate in common
                    if len(other_candidates & candidates) == 1:
                        pincers_box.append(_i)

            pincers_rc = product(pincers_column, pincers_row)
            pincers_rb = product(pincers_row, pincers_box)
            pincers_cb = product(pincers_box, pincers_column)

            cnt = 0

            for i1, i2 in pincers_rc:
                if self.candidates[i1] ^ self.candidates[i2] == candidates:
                    candidate_to_eliminiate = (self.candidates[i1] & self.candidates[i2]).pop()
                    # Intersect positions of pincers
                    r1, c1, _ = position(i1)
                    r2, c2, _ = position(i2)
                    cnt += self.eliminate_candidates_of_indices(
                        [cell_index(r1, c2), cell_index(r2, c1)], candidate_to_eliminiate)

            for i1, i2 in pincers_rb:
                if self.candidates[i1] ^ self.candidates[i2] == candidates:
                    candidate_to_eliminiate = (self.candidates[i1] & self.candidates[i2]).pop()
                    r1, _, b1 = position(i1)
                    r2, _, b2 = position(i2)
                    # Remove candidates from the same row of the other pincer box.
                    cnt += self.eliminate_candidates_of_indices(
                        set(query_indices(r=r1 % 3, b=b2)) | set(query_indices(r=r2 % 3, b=b1)),
                        candidate_to_eliminiate
                    )

            for i1, i2 in pincers_cb:
                if self.candidates[i1] ^ self.candidates[i2] == candidates:
                    candidate_to_eliminiate = (self.candidates[i1] & self.candidates[i2]).pop()
                    _, c1, b1 = position(i1)
                    _, c2, b2 = position(i2)
                    # Remove candidates from the same column of the other pincer box.
                    cnt += self.eliminate_candidates_of_indices(
                        set(query_indices(c=c1 % 3, b=b2)) | set(query_indices(c=c2 % 3, b=b1)),
                        candidate_to_eliminiate
                    )

        if cnt > 0:
            cnt += self.eliminate_y_wings()
        return cnt

    def solve(self, compute_candidates=True):
        if compute_candidates:
            self.compute_candidates()
        self.eliminate_pointing_pair()
        self.eliminate_hidden_subsets()
        self.eliminate_naked_subsets()
        self.eliminate_x_wings()
        self.eliminate_y_wings()
        cnt = self.solve_hidden_singles()
        if cnt > 0:
            cnt += self.solve(compute_candidates=False)
        return cnt

    def solve_and_display(self):
        print(f"🔢 {self.name}")
        if not self.valid:
            print(f"❗ Invalid {self.name}!")
            return
        self.display()
        print(f"⌛ Solving {self.name}...")
        start = timer()
        cells_solved = self.solve()
        end = timer()
        self.display()
        print(f"{self.name}: {cells_solved} cells solved")
        if self.solved:
            print(f"✅ {self.name} solved in {end - start:.4f} seconds!")
        else:
            print(f"❌ Failed to solve {self.name}.")
        if not self.valid:
            print(f"❗ Invalid {self.name}!")
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
