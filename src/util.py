
from typing import List


def valid_cell_value(n: int):
    return n >= 0 and n <= 9


def cell_index(r: int, c: int):
    return r * 9 + c


def position(i: int):
    r = i // 9
    c = i % 9
    b = r // 3 * 3 + c // 3
    return r, c, b


def row_indices(r: int):
    return [r * 9 + i for i in range(9)]


def column_indices(c: int):
    return [i * 9 + c for i in range(9)]


def box_indices(b: int):
    box_y = b // 3
    box_x = b % 3
    c_start = box_x * 3
    c_end = c_start + 3
    r_start = box_y * 3
    r_end = r_start + 3
    return [cell_index(r, c) for r in range(r_start, r_end) for c in range(c_start, c_end)]


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


def query_indices(r: int = None, c: int = None, b: int = None) -> List[int]:
    if r is None and c is None and b is None:
        return list(range(81))
    if r is not None and c is not None:
        return [cell_index(r, c)]
    if r is not None:
        if b is not None:
            r_start = b // 3 * 3
            r += r_start
            c_start = b % 3 * 3
            c_end = c_start + 3
            return row_indices(r)[c_start:c_end]
        return row_indices(r)
    if c is not None:
        if b is not None:
            c_start = b % 3 * 3
            c += c_start
            r_start = b // 3 * 3
            r_end = r_start + 3
            return column_indices(c)[r_start:r_end]
        return column_indices(c)
    if b is not None:
        return box_indices(b)
