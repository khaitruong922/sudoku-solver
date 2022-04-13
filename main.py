from src.boards import *

if __name__ == '__main__':
    s5 = sudoku_evil().solve_and_display()
    s5.display_candidates()
