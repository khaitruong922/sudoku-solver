from src.difficulties import *


if __name__ == '__main__':
    # s1 = sudoku_easy().solve_and_display()
    # s2 = sudoku_medium().solve_and_display()
    # s3 = sudoku_hard().solve_and_display()
    s4 = sudoku_expert().solve_and_display()
    s5 = sudoku_evil().solve_and_display()
    s5.display_candidates()
