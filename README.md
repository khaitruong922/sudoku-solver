# Sudoku Solver

An attempt to build a Sudoku algorithm with elimination techniques (without backtracking)

# Techniques

- Hidden Single
- Pointing Pair
- Naked Subset
- Hidden Subset

More techniques will be implemented in the future.

Can solve up to Expert in https://sudoku.com/

# Instructions

## Run project

python -m src.main

## Solve Sudoku

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

#### **`sudoku.txt`**

```
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

# Sample output

```
🔢 Sudoku Expert
6 _ _ | _ _ _ | _ 5 _
9 _ _ | 8 3 _ | _ _ _
_ _ 1 | _ _ _ | _ _ 3
------+-------+------
_ _ _ | _ _ 2 | _ _ _
_ 5 _ | _ _ 7 | _ _ 6
_ 7 2 | _ 1 _ | _ _ _
------+-------+------
_ _ _ | 4 _ _ | 1 _ _
_ _ _ | _ _ _ | 7 2 5
_ _ _ | 1 _ 9 | 6 _ _

⌛ Solving Sudoku Expert...
6 4 3 | 7 9 1 | 8 5 2
9 2 5 | 8 3 6 | 4 7 1
7 8 1 | 2 5 4 | 9 6 3
------+-------+------
1 9 6 | 5 4 2 | 3 8 7
3 5 4 | 9 8 7 | 2 1 6
8 7 2 | 6 1 3 | 5 9 4
------+-------+------
2 6 8 | 4 7 5 | 1 3 9
4 1 9 | 3 6 8 | 7 2 5
5 3 7 | 1 2 9 | 6 4 8

✅ Sudoku Expert solved!
```

```
🔢 Sudoku Evil
_ _ _ | _ _ 3 | _ _ 8
2 _ 4 | _ 6 _ | _ 9 _
_ 1 _ | _ _ _ | _ _ _
------+-------+------
_ 7 _ | _ _ _ | _ 5 _
5 _ 1 | _ _ 6 | 3 _ _
_ 9 _ | _ 1 _ | _ _ _
------+-------+------
_ _ _ | 2 _ _ | 9 _ _
7 _ _ | _ _ _ | _ _ _
6 _ 5 | _ 4 _ | _ 2 _

⌛ Solving Sudoku Evil...
9 6 7 | _ _ 3 | _ _ 8
2 5 4 | _ 6 _ | _ 9 3
8 1 3 | _ _ _ | _ _ _
------+-------+------
_ 7 _ | _ _ _ | _ 5 _
5 8 1 | _ _ 6 | 3 _ _
_ 9 _ | _ 1 _ | _ _ _
------+-------+------
1 4 8 | 2 _ _ | 9 _ _
7 2 9 | 6 _ _ | _ _ _
6 3 5 | _ 4 _ | _ 2 _

❌ Failed to solve Sudoku Evil.
```
