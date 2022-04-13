
from typing import List, Tuple


def valid_cell_value(n: int) -> bool:
    return n >= 0 and n <= 9


def cell_index(r: int, c: int) -> int:
    return r * 9 + c


def position(i: int) -> Tuple[int, int, int]:
    r = row_of(i)
    c = column_of(i)
    b = box_of_rc(r, c)
    return r, c, b


def box_of_i(i: int) -> int:
    return box_of_rc(row_of(i), column_of(i))


def column_of(i: int) -> int:
    return i % 9


def row_of(i: int) -> int:
    return i // 9


def box_of_rc(r: int, c: int) -> int:
    return r // 3 * 3 + c // 3


def row_indices(r: int) -> List[int]:
    return [r * 9 + i for i in range(9)]


def column_indices(c: int) -> List[int]:
    return [i * 9 + c for i in range(9)]


def box_indices(b: int) -> List[int]:
    box_r = b // 3
    box_c = b % 3
    c_start = box_c * 3
    c_end = c_start + 3
    r_start = box_r * 3
    r_end = r_start + 3
    return [cell_index(r, c) for r in range(r_start, r_end) for c in range(c_start, c_end)]


def rows_of_box(b: int) -> List[int]:
    box_start_r = b // 3 * 3
    return [box_start_r + i for i in range(3)]


def columns_of_box(b: int) -> List[int]:
    box_start_c = b % 3 * 3
    return [box_start_c + i for i in range(3)]


def load_cells_from_file(filename: str) -> List[int]:
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
            if c is not None:
                c += c_start
                return [cell_index(r, c)]
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
