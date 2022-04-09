from src.data import sudoku_easy, sudoku_medium
from src.sudoku import Sudoku


if __name__ == '__main__':
    Sudoku.from_file('sudoku.txt').solve()
    sudoku_easy().solve()
    sudoku_medium().solve()
