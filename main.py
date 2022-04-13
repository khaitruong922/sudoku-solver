from src.boards import *

if __name__ == '__main__':
    # s1 = sudoku_easy().solve_and_display()
    # s2 = sudoku_medium().solve_and_display()
    # s3 = sudoku_hard().solve_and_display()
    # s4 = sudoku_expert().solve_and_display()
    # x_wing = sudoku_x_wing().solve_and_display()
    # y_wing = sudoku_y_wing().solve_and_display()
    blr = sudoku_box_line_reduction().solve_and_display()
    blr.display_candidates()
    # s5 = sudoku_evil().solve_and_display()
    # s5.display_candidates()
