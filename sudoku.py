import numpy as np
import time
from solver import Sudoku

FILENAME = "easy_sudoku.csv"
ALGORITHM = "candidate_checking"
NO_PUZZLES = 1
SIZE = 9
 
# Read puzzles from csv-file
def read_puzzles(filename, no_puzzles):
    puzzles = np.zeros((no_puzzles, SIZE*SIZE), np.int32)
    solutions = np.zeros((no_puzzles, SIZE*SIZE), np.int32)

    for i, line in enumerate(open(filename, 'r').read().splitlines()[1:no_puzzles+1]):
        puzzle, solution = line.split(",")
        for j, q_s in enumerate(zip(puzzle, solution)):
            q, s = q_s
            puzzles[i, j] = q
            solutions[i, j] = s

    puzzles = puzzles.reshape((-1, SIZE, SIZE))
    solutions = solutions.reshape((-1, SIZE, SIZE))

    return puzzles, solutions    

def main():
    start_time = time.time()
    puzzles, solutions = read_puzzles(FILENAME, NO_PUZZLES)                 # Get sudokus
    download_end_time = time.time()
    print(f"It took {round(download_end_time - start_time, 4)} seconds to download {NO_PUZZLES} sudokus")

    # Solve each sudoku
    solved_sudokus = 0
    for puzzle, solution in zip(puzzles, solutions):
        sudoku = Sudoku(puzzle, solution)

        sudoku.solve(ALGORITHM)
        if sudoku.correct_solution():
            solved_sudokus += 1

    solve_end_time = time.time()
    print(f"Method solved {round(solved_sudokus / NO_PUZZLES, 2)*100}% of {NO_PUZZLES} sudokus in {round(solve_end_time - download_end_time, 4)} seconds")

if __name__ == '__main__':
    main()