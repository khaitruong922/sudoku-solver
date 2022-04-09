import pytest
from src.exceptions import InvalidSudoku, InvalidCellValue
from src.sudoku import Sudoku, position


@pytest.fixture
def sudoku():
    return Sudoku([
        0, 6, 0, 4, 0, 1, 3, 7, 0,
        1, 0, 0, 0, 0, 0, 4, 2, 0,
        3, 0, 0, 0, 0, 2, 0, 6, 1,
        4, 9, 6, 0, 0, 0, 0, 3, 2,
        0, 0, 8, 3, 6, 9, 0, 0, 0,
        0, 5, 3, 0, 0, 8, 1, 9, 6,
        6, 4, 0, 8, 1, 3, 2, 0, 0,
        0, 0, 0, 6, 0, 7, 0, 0, 0,
        0, 0, 0, 5, 9, 0, 0, 0, 3,
    ])


class TestSudoku:

    def test_get_cell(self, sudoku: Sudoku):
        assert sudoku.get_cell(0, 0) == 0
        assert sudoku.get_cell(8, 8) == 3

    def test_set_cell(self, sudoku: Sudoku):
        with pytest.raises(InvalidCellValue):
            sudoku.set_cell(0, 0, 10)
        with pytest.raises(InvalidCellValue):
            sudoku.set_cell(0, 0, -1)

        sudoku.set_cell(0, 0, 1)
        assert sudoku.get_cell(0, 0) == 0

        sudoku.set_cell(0, 0, 2)
        assert sudoku.get_cell(0, 0) == 2

    def test_set_cells(self, sudoku: Sudoku):
        with pytest.raises(InvalidSudoku):
            sudoku.set_cells([0] * 80)
        with pytest.raises(InvalidSudoku):
            sudoku.set_cells([0] * 82)
        with pytest.raises(InvalidCellValue):
            sudoku.set_cells([-1] * 81)

    def test_row(self, sudoku: Sudoku):
        assert sudoku.row(0) == [0, 6, 0, 4, 0, 1, 3, 7, 0]
        assert sudoku.row(8) == [0, 0, 0, 5, 9, 0, 0, 0, 3]

    def test_column(self, sudoku: Sudoku):
        assert sudoku.column(0) == [0, 1, 3, 4, 0, 0, 6, 0, 0]
        assert sudoku.column(8) == [0, 0, 1, 2, 0, 6, 0, 0, 3]

    def test_box(self, sudoku: Sudoku):
        assert sudoku.box(0) == [0, 6, 0, 1, 0, 0, 3, 0, 0]
        assert sudoku.box(1) == [4, 0, 1, 0, 0, 0, 0, 0, 2]
        assert sudoku.box(3) == [4, 9, 6, 0, 0, 8, 0, 5, 3]
        assert sudoku.box(4) == [0, 0, 0, 3, 6, 9, 0, 0, 8]
        assert sudoku.box(8) == [2, 0, 0, 0, 0, 0, 0, 0, 3]

    def test_candidates(self, sudoku: Sudoku):
        assert sudoku.candidates(0) == {2, 5, 8, 9}
        assert sudoku.candidates(8) == {5, 8, 9}

        blank_sudoku = Sudoku()
        assert blank_sudoku.candidates(0) == {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def test_valid(self, sudoku: Sudoku):
        assert sudoku.valid

        invalid_row_sudoku = Sudoku([
            0, 1, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
        ])
        assert not invalid_row_sudoku.valid

        invalid_column_sudoku = Sudoku([
            0, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
        ])
        assert not invalid_column_sudoku.valid

        invalid_box_sudoku = Sudoku([
            0, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0,
        ])

        assert not invalid_box_sudoku.valid


def test_position():
    assert position(0) == (0, 0, 0)
    assert position(4) == (0, 4, 1)
    assert position(28) == (3, 1, 3)
    assert position(80) == (8, 8, 8)
