from src.data import sudoku_easy, sudoku_hard, sudoku_medium
from src.sudoku import Sudoku


if __name__ == '__main__':
    # Sudoku.from_file('sudoku.txt').solve()
    print("Easy")
    sudoku_easy().solve()
    print("Medium")
    sudoku_medium().solve()
    print("Hard")
    sudoku_hard().solve()
