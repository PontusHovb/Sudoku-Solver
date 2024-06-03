import numpy as np

class Sudoku:
    def __init__(self, puzzle, solution):
        self.puzzle = puzzle
        self.solution = solution
        self.unsolved_cells = self.get_all_unsolved(self.puzzle)

    def __str__(self):
        for r, row in enumerate(self.puzzle):
            if r in [3, 6]:
                print('------+-------+------')
            for c, value in enumerate(row):
                if c in [3, 6]:
                    print('|', end=' ')
                print(value, end=' ')

            print('\n', end='')
            
    def solve(self, method):
        match method:
            case "bruteforce":                               
                return self.bruteforce(self.puzzle, self.unsolved_cells, len(self.unsolved_cells))
            case "bruteforce_lookahead":
                return self.bruteforce_lookahead(self.puzzle, self.unsolved_cells)
            case "candidate_checking":
                return self.candidate_checking(self.puzzle, self.unsolved_cells)
            case _:
                print("Enter valid algorithm")
    
    def correct_solution(self):
        return np.array_equal(self.puzzle, self.solution)

    def get_all_unsolved(self, puzzle):
        unsolved_cells = list()
        for r, row in enumerate(puzzle):
            for c, cell in enumerate(row):
                if cell == 0:
                    unsolved_cells.append((r, c))
        
        return unsolved_cells
    
    def valid_guess(self, r, c, guess, puzzle):
        # Check if guess is in column
        if guess in puzzle[r] and c != np.where(puzzle[r] == guess):
            return False
        
        # Check if guess is in row
        if guess in [puzzle[i][c] for i in range(9)] and r != [puzzle[i][c] for i in range(9)].index(guess):
            return False

        # Check if guess is in square
        start_row, start_col = 3 * (r // 3), 3 * (c // 3)
        for check_row in range(start_row, start_row + 3):
            for check_col in range(start_col, start_col + 3):
                if puzzle[check_row][check_col] == guess and (check_row, check_col) != (r, c):
                    return False

        return True

    def get_candidates(self, puzzle, row, column):
        candidates = set(range(1, 10))
        candidates -= set(puzzle[row])                                          # Eliminate candidates in same row
        candidates -= set(puzzle[i][column] for i in range(9))                  # Eliminate candidates in same column

        block_row, block_col = 3 * (row // 3), 3 * (column // 3)                # Eliminate candidates in same box
        for i in range(3):
            for j in range(3):
                candidates.discard(puzzle[block_row + i][block_col + j])

        return candidates

    def bruteforce(self, puzzle, empty_cells):
        if len(empty_cells) == 0:
            return True if self.correct_solution() else False
               
        for guess in range(1,10):                                               # If empty cells left, make a guess for first empty cell
            puzzle[empty_cells[0][0]][empty_cells[0][1]] = guess

            if self.bruteforce(puzzle, empty_cells[1:], total_empty_cells):                        # Recursive solving
                return True
            
            puzzle[empty_cells[0][0]][empty_cells[0][1]] = 0                    # Backtrack if guess don't yield solution

        return False
    
    def bruteforce_lookahead(self, puzzle, empty_cells):
        if len(empty_cells) == 0:                                     
            return True if self.correct_solution() else False

        for guess in range(1, 10):                                              # If empty cells left, make a guess for first empty cell
            if self.valid_guess(empty_cells[0][0], empty_cells[0][1], guess, puzzle):
                puzzle[empty_cells[0][0]][empty_cells[0][1]] = guess

                if self.bruteforce_lookahead(puzzle, empty_cells[1:]):          # Recursive solving
                    return True
                    
                puzzle[empty_cells[0][0]][empty_cells[0][1]] = 0                # Backtrack if guess don't yield solution

        return False

    def candidate_checking(self, puzzle, empty_cells):
        if len(empty_cells) == 0:                                               # puzzle solved if there are no more empty cells left
            return True
        
        for empty_cell in empty_cells:                                          # Loop through all empty cells
            possible_values = 0
            for guess in range(1, 10):
                if self.valid_guess(empty_cell[0], empty_cell[1], guess, puzzle):
                    possible_guess = guess
                    possible_values += 1

            if possible_values == 1:                                            # If there is only one candidate for empty cell
                puzzle[empty_cell[0]][empty_cell[1]] = possible_guess
                empty_cells.remove(empty_cell)
                return self.candidate_checking(puzzle, empty_cells)

        return False                                                            # Correct value can't be determined for any empty cell        