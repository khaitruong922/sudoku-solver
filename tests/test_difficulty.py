from src.boards.difficulty import *
from src.sudoku import Sudoku


def assert_solved(s: Sudoku):
    s.solve()
    assert s.solved


class TestDifficulty:

    def test_sudoku_easy(self):
        assert_solved(sudoku_easy())

    def test_sudoku_medium(self):
        assert_solved(sudoku_medium())

    def test_sudoku_hard(self):
        assert_solved(sudoku_hard())

    def test_sudoku_expert(self):
        assert_solved(sudoku_expert())

    def test_sudoku_expert_2(self):
        assert_solved(sudoku_expert_2())

    def test_sudoku_evil(self):
        assert_solved(sudoku_evil())

    def test_sudoku_evil_2(self):
        assert_solved(sudoku_evil_2())
