from src.data import sudoku_easy, sudoku_hard, sudoku_medium
from src.sudoku import Sudoku


if __name__ == '__main__':
    # Sudoku.from_file('sudoku.txt').solve()
    print("Easy")
    s1 = sudoku_easy().solve()
    print("Medium")
    s2 = sudoku_medium().solve()
    print("Hard")
    s3 = sudoku_hard().solve()
    s3.display_candidates()
