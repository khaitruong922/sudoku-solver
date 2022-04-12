from src.sudoku import Sudoku

"""
    Sudoku boards classified by technique.
"""


def sudoku_x_wing():
    return Sudoku([
        6, 0, 0, 0, 9, 0, 0, 0, 7,
        0, 4, 0, 0, 0, 7, 1, 0, 0,
        0, 0, 2, 8, 0, 0, 0, 5, 0,
        8, 0, 0, 0, 0, 0, 0, 9, 0,
        0, 0, 0, 0, 7, 0, 0, 0, 0,
        0, 3, 0, 0, 0, 0, 0, 0, 8,
        0, 5, 0, 0, 0, 2, 3, 0, 0,
        0, 0, 4, 5, 0, 0, 0, 2, 0,
        9, 0, 0, 0, 3, 0, 0, 0, 4,
    ], name="Sudoku X-Wing")
