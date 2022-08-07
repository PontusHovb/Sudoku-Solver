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


def find_unsolved_cell(sudoku):
    r = c = 0
    while sudoku[r][c] != 0:            # Loop through to sudoku until unsolved cell is found
        if c == 8:                      # Skip to next row if end of row
            c = 0
            r += 1
        else:
            c += 1
    
    return r, c

def guess(r, c, sudoku, last_guess_r, last_guess_c):
    for guess_number in range(1,10):
        if valid_guess(r, c, guess_number, sudoku):
            sudoku[r][c] = guess_number
            last_guess_r = r
            last_guess_c = c
            print("------------------------------------------------")
            print(sudoku)
            r, c = find_unsolved_cell(sudoku)
            guess(r, c, sudoku, last_guess_r, last_guess_c)
    
    if sudoku[r][c] == 0:                                               # If no guess is possible
        sudoku[last_guess_r][last_guess_c] = 0
        return
        

def valid_guess(r, c, guess, sudoku):
    for check_row in range(0,9):                                        # Check if guess is in colummn
        if sudoku[check_row][c] == guess and check_row != r:
            return False
    
    for check_column in range(0,9):                                     # Check if guess is in row
        if sudoku[r][check_column] == guess and check_column != c:
            return False

    for check_row in range(0, 3):                                       # Check if guess is in square
        for check_column in range(0, 3):
            if (r // 3)*3 + check_row != r and (c // 3)*3 + check_column != c:
                if sudoku[(r // 3)*3 + check_row][(c // 3)*3 + check_column] == guess:
                    return False

    return True

def main():
    r, c = find_unsolved_cell(sudoku)
    print("cell", r, c)
    guess(r, c, sudoku, '', '')

if __name__ == '__main__':
    main()
