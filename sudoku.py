import numpy as np

sudoku = np.array(
    [[5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]]    )       # Start array

r = c = 0
while sudoku[r][c] != 0:            # Loop through to sudoku until unsolved cell is found
    if c == 8:                      # Skip to next row if end of row
        c = 0
        r += 1
    else:
        c += 1

def guess(r, c):
    for guess in range(1,9):
        if valid_guess(r, c, guess):
            print(guess)

def valid_guess(r, c, guess):
    for check_row in range(0,8):                                        # Check if guess is in colummn
        if sudoku[check_row][c] == guess and check_row != r:
            return False
    
    for check_column in range(0,8):                                     # Check if guess is in row
        if sudoku[r][check_column] == guess and check_column != c:
            return False

    square_row = r // 3
    square_column = c // 3
    print(square_row, square_column)
    
    return True

print(sudoku)