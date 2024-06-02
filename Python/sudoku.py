import numpy as np
import time
import random
import os
from solver import Sudoku

FILENAME = "../Data/sudoku.csv"
ALGORITHM = "bruteforce_lookahead"
NO_PUZZLES = 1000
SIZE = 9
 
# Read puzzles from csv-file
def read_puzzles(filename, no_puzzles):
    puzzles = np.zeros((no_puzzles, SIZE*SIZE), np.int32)
    solutions = np.zeros((no_puzzles, SIZE*SIZE), np.int32)

    with open(filename, 'r') as csv_file:
        all_sudokus = csv_file.read().splitlines()
        if len(all_sudokus) + 1 < NO_PUZZLES:
            raise ValueError("There are not enough puzzles in file")
    
    sudokus = random.sample(all_sudokus[1:], k=no_puzzles)
    for i, line in enumerate(sudokus):
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