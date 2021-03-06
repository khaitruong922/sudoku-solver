from src.boards.technique import *
from src.sudoku import Sudoku


def assert_solved(s: Sudoku):
    s.solve()
    assert s.solved


class TestTechnique:
    def test_sudoku_x_wing(self):
        assert_solved(sudoku_x_wing())

    def test_sudoku_y_wing(self):
        assert_solved(sudoku_y_wing())

    def test_sudoku_box_line_reduction(self):
        assert_solved(sudoku_box_line_reduction())

    def test_sudoku_box_box_reduction(self):
        assert_solved(sudoku_box_box_reduction())

    def test_sudoku_swordfish(self):
        assert_solved(sudoku_swordfish())

    def test_sudoku_jellyfish(self):
        assert_solved(sudoku_jellyfish())

    def test_sudoku_xyz_wing(self):
        assert_solved(sudoku_xyz_wing())
