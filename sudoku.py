import numpy as np
import time

FILENAME = "sudoku.csv"
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

def first_unsolved_cell(sudoku):
    for r, row in enumerate(sudoku):
        for c, cell in enumerate(row):
            if cell == 0:
                return [r, c]
    
    return None                                 
    
def brute_force_solve(sudoku):
    r, c = first_unsolved_cell(sudoku)
    
    if not first_unsolved_cell(sudoku):         # No empty cells, sudoku is solved
        return True, sudoku

    for guess in range(0,9):                    
        if valid_guess(r, c, guess, sudoku):    # Check if guess is valid
            sudoku[r][c] = guess
            print("----------------------------")
            print(r,c,"->",guess)
            print(sudoku)
            time.sleep(3)
            if brute_force_solve(sudoku)[0]:    # Recursive solving
                return True, sudoku
            
            sudoku[r][c] = 0                    # Backtrack if guess don't yield solution

    return False, sudoku



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
    start_time = time.time()

    quizzes, solutions = read_quizzes(FILENAME, NO_PUZZLES)             # Get sudokus
    download_end_time = time.time()
    print(f"It took {download_end_time - start_time} seconds to download {NO_PUZZLES} sudokus")

    # Solve each sudoku
    for i, sudoku in enumerate(quizzes):
        if brute_force_solve(sudoku)[0]:
            print(brute_force_solve(sudoku)[1])
        else:
            print("No solution")

    solve_end_time = time.time()
    print(f"It took {solve_end_time - download_end_time} seconds to solve {NO_PUZZLES} sudokus")
    

if __name__ == '__main__':
    main()