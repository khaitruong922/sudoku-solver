from src.difficulties import *
from src.sudoku import Sudoku


if __name__ == '__main__':
    # Sudoku.from_file('sudoku.txt').solve()
    print("Easy")
    s1 = sudoku_easy().solve()
    print("Medium")
    s2 = sudoku_medium().solve()
    print("Hard")
    s3 = sudoku_hard().solve()
    print("Expert")
    s4 = sudoku_expert().solve()
    s4.display_candidates()
    print("Evil")
    s5 = sudoku_evil().solve()
    s5.display_candidates()
