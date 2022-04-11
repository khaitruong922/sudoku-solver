# Sudoku Solver

An attempt to build a Sudoku algorithm with elimination techniques (without backtracking)

## Current progress

Techniques: Hidden Singles, Pointing Pair, Naked Subset, Hidden Subset

Can solve up to Expert in https://sudoku.com/

## Instructions

### Run project

python -m src.main

### Solve Sudoku

Create a Sudoku using 1D array of 81 digits.

```python
sudoku = Sudoku([
        6, 0, 0, 0, 0, 0, 0, 5, 0,
        9, 0, 0, 8, 3, 0, 0, 0, 0,
        0, 0, 1, 0, 0, 0, 0, 0, 3,
        0, 0, 0, 0, 0, 2, 0, 0, 0,
        0, 5, 0, 0, 0, 7, 0, 0, 6,
        0, 7, 2, 0, 1, 0, 0, 0, 0,
        0, 0, 0, 4, 0, 0, 1, 0, 0,
        0, 0, 0, 0, 0, 0, 7, 2, 5,
        0, 0, 0, 1, 0, 9, 6, 0, 0,
    ])
```

or load from a text file with 9 lines, each has 9 digits.

```{data-filename="sudoku.txt"}
003020600
900305001
001806400
008102900
700000008
006708200
002609500
800203009
005010300
```

```python
sudoku = Sudoku.from_file("sudoku.txt")
```

Then solve

```python
sudoku.solve()
```
