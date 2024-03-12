import numpy as np
import time
from itertools import combinations

FILENAME = "hard_sudoku.csv"
NO_PUZZLES = 1

# Read quizzes from csv-file
def read_quizzes(filename, size):
    quizzes = np.zeros((size, 81), np.int32)
    solutions = np.zeros((size, 81), np.int32)

    for i, line in enumerate(open(filename, 'r').read().splitlines()[1:size+1]):
        quiz, solution = line.split(",")
        for j, q_s in enumerate(zip(quiz, solution)):
            q, s = q_s
            quizzes[i, j] = q
            solutions[i, j] = s

    quizzes = quizzes.reshape((-1, 9, 9))
    solutions = solutions.reshape((-1, 9, 9))

    return quizzes, solutions               


# Find all unsolved cells in sudoku
def get_all_unsolved(sudoku):
    unsolved_cells = list()
    for r, row in enumerate(sudoku):
        for c, cell in enumerate(row):
            if cell == 0:
                unsolved_cells.append((r, c))
    
    return unsolved_cells    

# Check if a guess is valid
def valid_guess(r, c, guess, sudoku):
    # Check if guess is in column
    if guess in sudoku[r] and c != sudoku[r].index(guess):
        return False
    
    # Check if guess is in row
    if guess in [sudoku[i][c] for i in range(9)] and r != [sudoku[i][c] for i in range(9)].index(guess):
        return False

    # Check if guess is in square
    start_row, start_col = 3 * (r // 3), 3 * (c // 3)
    for check_row in range(start_row, start_row + 3):
        for check_col in range(start_col, start_col + 3):
            if sudoku[check_row][check_col] == guess and (check_row, check_col) != (r, c):
                return False

    return True

def get_candidates(sudoku, row, column):
    candidates = set(range(1, 10))

    # Eliminate candidates in same row
    candidates -= set(sudoku[row])

    # Eliminate candidates in same column
    candidates -= set(sudoku[i][column] for i in range(9))

    # Eliminate candidates in same box
    block_row, block_col = 3 * (row // 3), 3 * (column // 3)
    for i in range(3):
        for j in range(3):
            candidates.discard(sudoku[block_row + i][block_col + j])

    return candidates


###############################################################################################################################
########################################                  Algorithms                   ########################################
###############################################################################################################################
# Brute-force algorithm
def bruteforce(sudoku, solution, empty_cells):
    if np.array_equal(sudoku, solution):                                    # Check if sudoku is solved
        return True
                                                                  
    for guess in range(1,10):                                               # If empty cells left, make a guess for first empty cell
        sudoku[empty_cells[0][0]][empty_cells[0][1]] = guess

        if bruteforce(sudoku, solution, empty_cells[1:]):                   # Recursive solving
            return True
            
        sudoku[empty_cells[0][0]][empty_cells[0][1]] = 0                    # Backtrack if guess don't yield solution

# Brute-force algorithm with look ahead
def bruteforce_lookahead(sudoku, solution, empty_cells):
    if len(empty_cells) == 0:                                               # Sudoku solved if there are no more empty cells left
        return True

    for guess in range(1, 10):
        if valid_guess(empty_cells[0][0], empty_cells[0][1], guess, sudoku):
            sudoku[empty_cells[0][0]][empty_cells[0][1]] = guess

            if bruteforce_lookahead(sudoku, solution, empty_cells[1:]):     # Recursive solving
                return True
                
            sudoku[empty_cells[0][0]][empty_cells[0][1]] = 0                # Backtrack if guess don't yield solution

# Candidate-checking method
def candidate_checking(sudoku, solution, empty_cells):
    if len(empty_cells) == 0:                                               # Sudoku solved if there are no more empty cells left
        return True
    
    for empty_cell in empty_cells:                                          # Loop through all empty cells
        possible_values = 0
        for guess in range(1, 10):
            if valid_guess(empty_cell[0], empty_cell[1], guess, sudoku):
                possible_guess = guess
                possible_values += 1

        if possible_values == 1:                                            # If there is only one candidate for empty cell
            sudoku[empty_cell[0]][empty_cell[1]] = possible_guess
            empty_cells.remove(empty_cell)
            return candidate_checking(sudoku, solution, empty_cells)

    return False                                                            # Correct value can't be determined for any empty cell

# Place-finding method
def place_finding(sudoku, solution, empty_cells):
    if len(empty_cells) == 0:                                               # Sudoku solved if there are no more empty cells left
        return True
    
    for empty_cell in empty_cells:                                          # Loop through all empty cells
        candidates = get_candidates(sudoku, empty_cell[0, empty_cell[1]])

        if len(candidates) == 1:                                            # Hidden single if there is only one candidate left
            sudoku[empty_cell[0]][empty_cell[1]] = candidates.pop()
            empty_cells.remove(empty_cell)   
            return candidate_checking(sudoku, solution, empty_cells)
    
    return False

# Choose which algorithm to use
def solve_sudoku(sudoku, solution):                                         
    empty_cells = get_all_unsolved(sudoku)
    return place_finding(sudoku, solution, empty_cells)              

def main():
    start_time = time.time()

    quizzes, solutions = read_quizzes(FILENAME, NO_PUZZLES)                 # Get sudokus
    download_end_time = time.time()
    print(f"It took {download_end_time - start_time} seconds to download {NO_PUZZLES} sudokus")

    # Solve each sudoku
    solved_sudokus = 0
    for sudoku, solution in zip(quizzes, solutions):
        if solve_sudoku(sudoku, solution):
            solved_sudokus += 1

    solve_end_time = time.time()
    print(f"Method solved {round(solved_sudokus / NO_PUZZLES, 2)*100}% of {NO_PUZZLES} sudokus in {solve_end_time - download_end_time} seconds")
    
if __name__ == '__main__':
    main()