class InvalidSudoku(Exception):
    """
    Raised when try to initialize an invalid sudoku.
    """
    pass


class InvalidCellValue(Exception):
    """
    Raised when try to set a cell not in the range of 0-9. 
    """
    pass
