import numpy as np
import time

FILENAME = "sudoku.csv"
NO_PUZZLES = 1000

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

# Find first unsolved cell
def find_unsolved(sudoku):
    for r, row in enumerate(sudoku):
        for c, cell in enumerate(row):
            if cell == 0:
                return (r, c)
    
    return None                                 

def get_all_unsolved(sudoku):
    unsolved_cells = list()
    for r, row in enumerate(sudoku):
        for c, cell in enumerate(row):
            if cell == 0:
                unsolved_cells.append((r, c))
    
    return unsolved_cells    

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

# Backtrack solve
def backtrack_solve(sudoku, empty_cells):
    # Sudoku solved if there are no empty cells left
    if len(empty_cells) == 0:
        return True

    empty = empty_cells[0]

    for guess in range(1,10):                    
        if valid_guess(empty[0], empty[1], guess, sudoku):              # Check if guess is valid
            sudoku[empty[0]][empty[1]] = guess

            if backtrack_solve(sudoku, empty_cells[1:]):                # Recursive solving
                return True
            
            sudoku[empty[0]][empty[1]] = 0                              # Backtrack if guess don't yield solution

    return False

# Candidate-checking method
def candidate_checking_method(sudoku, empty_cells):
    # Sudoku solved if there are no empty cells left
    if len(empty_cells) == 0:
        return True
    
    # Loop through all empty cells
    for empty_cell in empty_cells:
        possible_values = 0
        for guess in range(1, 10):
            if valid_guess(empty_cell[0], empty_cell[1], guess, sudoku):
                possible_guess = guess
                possible_values += 1

        # If there is only one candidate for empty cell
        if possible_values == 1:
            sudoku[empty_cell[0]][empty_cell[1]] = possible_guess
            empty_cells.remove(empty_cell)
            return candidate_checking_method(sudoku, empty_cells)

    # Correct value can't be determined for any empty cell
    return False


def solve_sudoku(sudoku):
    empty_cells = get_all_unsolved(sudoku)
    return candidate_checking_method(sudoku, empty_cells)

def main():
    start_time = time.time()

    quizzes, solutions = read_quizzes(FILENAME, NO_PUZZLES)                 # Get sudokus
    download_end_time = time.time()
    print(f"It took {download_end_time - start_time} seconds to download {NO_PUZZLES} sudokus")

    # Solve each sudoku
    solved_sudokus = 0
    for sudoku in quizzes:
        if solve_sudoku(sudoku):
            solved_sudokus += 1

    solve_end_time = time.time()
    print(f"Method solved {round(solved_sudokus / NO_PUZZLES, 2)*100}% of {NO_PUZZLES} sudokus in {solve_end_time - download_end_time} seconds")
    
if __name__ == '__main__':
    main()