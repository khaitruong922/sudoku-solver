from src.boards.technique import *


class TestTechnique:
    def test_sudoku_x_wing(self):
        s = sudoku_x_wing()
        s.solve()
        assert s.solved

    def test_sudoku_y_wing(self):
        s = sudoku_y_wing()
        s.solve()
        assert s.solved

    def test_sudoku_box_line_reduction(self):
        s = sudoku_box_line_reduction()
        s.solve()
        assert s.solved
