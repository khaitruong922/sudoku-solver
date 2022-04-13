from src.boards.difficulty import *


class TestDifficulty:
    def test_sudoku_easy(self):
        s = sudoku_easy()
        s.solve()
        assert s.solved

    def test_sudoku_medium(self):
        s = sudoku_medium()
        s.solve()
        assert s.solved

    def test_sudoku_hard(self):
        s = sudoku_hard()
        s.solve()
        assert s.solved

    def test_sudoku_expert(self):
        s = sudoku_expert()
        s.solve()
        assert s.solved

    def test_sudoku_evil(self):
        s = sudoku_evil()
        s.solve()
        assert s.solved
