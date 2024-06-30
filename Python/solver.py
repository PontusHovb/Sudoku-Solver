import numpy as np
from gui import GUI

class Sudoku:
    def __init__(self, puzzle, solution):
        self.puzzle = puzzle
        self.solution = solution
        self.unsolved_cells = self.get_all_unsolved(self.puzzle)
        self.no_unsolved_cells = len(self.unsolved_cells)
        self.tries = 0

    def __str__(self):
        for r, row in enumerate(self.puzzle):
            if r in [3, 6]:
                print('------+-------+------')
            for c, value in enumerate(row):
                if c in [3, 6]:
                    print('|', end=' ')
                print(value, end=' ')

            print('\n', end='')
            
    def solve(self, method, show_gui):
        if show_gui:
            self.gui = GUI(self.puzzle, method)
        else:
            self.gui = False

        match method:
            case "bruteforce":                               
                self.bruteforce(self.puzzle, self.unsolved_cells, self.gui)
            case "bruteforce_lookahead":
                self.bruteforce_lookahead(self.puzzle, self.unsolved_cells, self.gui)
            case "candidate_checking":
                self.candidate_checking(self.puzzle, self.unsolved_cells, self.gui)
            case "place_finding":
                self.place_finding(self.puzzle, self.unsolved_cells, self.gui)
            case "crooks_algorithm":
                self.crooks_algorithm(self.puzzle, self.unsolved_cells, self.gui)
            case _:
                print("Enter valid algorithm")

        return self.tries, self.no_unsolved_cells
    
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

    def is_only_possible_location(self, puzzle, empty_cell, guess, check_type):
        if check_type == "row":
            for c in range(9):
                if puzzle[empty_cell[0]][c] == 0 and c != empty_cell[1] and self.valid_guess(empty_cell[0], c, guess, puzzle):
                    return False
        elif check_type == "column":
            for r in range(9):
                if puzzle[r][empty_cell[1]] == 0 and r != empty_cell[0] and self.valid_guess(r, empty_cell[1], guess, puzzle):
                    return False
        elif check_type == "box":
            start_row, start_col = 3 * (empty_cell[0] // 3), 3 * (empty_cell[1] // 3)
            for r in range(start_row, start_row + 3):
                for c in range(start_col, start_col + 3):
                    if puzzle[r][c] == 0 and not (r == empty_cell[0] and c == empty_cell[1]) and self.valid_guess(r, c, guess, puzzle):
                        return False
        else:
            return False
        return True

    def find_preemtive_sets(self, cell, sudoku_markup, gui):
        cell_markup = sudoku_markup[cell[0]][cell[1]]
        changes_made = 0

        # Row
        row = sudoku_markup[cell[0]].tolist()
        if row.count(cell_markup) == len(cell_markup):
            for value in cell_markup:
                for c, markup in enumerate(row):
                    if markup != cell_markup:
                        try:
                            sudoku_markup[cell[0]][c].remove(value)
                            changes_made += 1
                            if gui: gui.draw_markup_cell(cell[0], c, markup)
                        except:
                            pass

        # Column
        col = [sudoku_markup[i][cell[1]] for i in range(9)]
        if col.count(cell_markup) == len(cell_markup):
            for value in cell_markup:
                for r, markup in enumerate(col):
                    if markup != cell_markup:
                        try:
                            sudoku_markup[r][cell[1]].remove(value)
                            changes_made += 1
                            if gui: gui.draw_markup_cell(r, cell[1], markup)
                        except:
                            pass

        # Box
        box_indecies = list()
        box = list()
        for r, row in enumerate(sudoku_markup):
            for c, markup in enumerate(row):
                if r // 3 == cell[0] // 3 and c // 3 == cell[1] // 3:
                    box.append(markup)
                    box_indecies.append([r, c])

        if box.count(   cell_markup) == len(cell_markup):
            for value in cell_markup:
                for i, markup in enumerate(box):
                    if markup != cell_markup:
                        try:
                            sudoku_markup[box_indecies[i][0]][box_indecies[i][1]].remove(value)
                            changes_made += 1
                            if gui: gui.draw_markup_cell(box_indecies[i][0], box_indecies[i][1], markup)
                        except:
                            pass

        return sudoku_markup, changes_made

    def get_candidates(self, puzzle, row, column):
        candidates = set(range(1, 10))
        candidates -= set(puzzle[row])                                          # Eliminate candidates in same row
        candidates -= set(puzzle[i][column] for i in range(9))                  # Eliminate candidates in same column

        block_row, block_col = 3 * (row // 3), 3 * (column // 3)                # Eliminate candidates in same box
        for i in range(3):
            for j in range(3):
                candidates.discard(puzzle[block_row + i][block_col + j])

        return candidates

    def bruteforce(self, puzzle, empty_cells, gui):
        if len(empty_cells) == 0:
            return True if self.correct_solution() else False
               
        for guess in range(1,10):                                               # If empty cells left, make a guess for first empty cell
            if gui:
                gui.show_number(empty_cells[0][0], empty_cells[0][1], guess)
                gui.add_number(empty_cells[0][0], empty_cells[0][1], guess)
            puzzle[empty_cells[0][0]][empty_cells[0][1]] = guess
            self.tries += 1

            if self.bruteforce(puzzle, empty_cells[1:], gui):                   # Recursive solving
                return True
            
            if gui: gui.erase_number(empty_cells[0][0],empty_cells[0][1]) 
            puzzle[empty_cells[0][0]][empty_cells[0][1]] = 0                    # Backtrack if guess don't yield solution

        return False
    
    def bruteforce_lookahead(self, puzzle, empty_cells, gui):
        if len(empty_cells) == 0:                                     
            return True if self.correct_solution() else False

        for guess in range(1, 10):                                              # If empty cells left, make a guess for first empty cell
            if gui: gui.show_number(empty_cells[0][0], empty_cells[0][1], guess)
            if self.valid_guess(empty_cells[0][0], empty_cells[0][1], guess, puzzle):
                if gui: gui.add_number(empty_cells[0][0], empty_cells[0][1], guess)
                puzzle[empty_cells[0][0]][empty_cells[0][1]] = guess
                self.tries += 1

                if self.bruteforce_lookahead(puzzle, empty_cells[1:], gui):     # Recursive solving
                    return True

                if gui: gui.erase_number(empty_cells[0][0],empty_cells[0][1]) 
                puzzle[empty_cells[0][0]][empty_cells[0][1]] = 0                # Backtrack if guess don't yield solution

        return False

    def candidate_checking(self, puzzle, empty_cells, gui):
        if len(empty_cells) == 0:                                               # puzzle solved if there are no more empty cells left
            return True
        
        for empty_cell in empty_cells:                                          # Loop through all empty cells
            possible_values = 0
            for guess in range(1, 10):
                if gui: gui.show_number(empty_cell[0], empty_cell[1], guess)
                if self.valid_guess(empty_cell[0], empty_cell[1], guess, puzzle):
                    possible_guess = guess
                    possible_values += 1

            if possible_values == 1:                                            # If there is only one candidate for empty cell
                if gui: gui.add_number(empty_cell[0], empty_cell[1], possible_guess)
                puzzle[empty_cell[0]][empty_cell[1]] = possible_guess
                self.tries += 1
                empty_cells.remove(empty_cell)
                return self.candidate_checking(puzzle, empty_cells, gui)

        return False                                                            # Correct value can't be determined for any empty cell
    
    def place_finding(self, puzzle, empty_cells, gui):
        if len(empty_cells) == 0:                                               # puzzle solved if there are no more empty cells left
            return True
    
        for guess in range(1, 10):
            for empty_cell in empty_cells:
                if gui: gui.show_number(empty_cell[0], empty_cell[1], guess)
                if self.valid_guess(empty_cell[0], empty_cell[1], guess, puzzle):
                    if (self.is_only_possible_location(puzzle, empty_cell, guess, "row") or
                        self.is_only_possible_location(puzzle, empty_cell, guess, "column") or
                        self.is_only_possible_location(puzzle, empty_cell, guess, "box")):
                        
                        if gui: gui.add_number(empty_cell[0], empty_cell[1], guess)
                        puzzle[empty_cell[0]][empty_cell[1]] = guess
                        self.tries += 1
                        empty_cells.remove(empty_cell)
                        self.place_finding(puzzle, empty_cells, gui)

    def crooks_algorithm(self, puzzle, empty_cells, gui):
        sudoku_markup = np.empty((9, 9), dtype=set)

        # Mark sudoku with all possible values for every empty cell
        for empty_cell in empty_cells:
            sudoku_markup[empty_cell[0]][empty_cell[1]] = self.get_candidates(puzzle, empty_cell[0], empty_cell[1])
        gui.draw_markup_grid(puzzle, sudoku_markup)
        
        return self.crooks_algorithm_solve(puzzle, sudoku_markup, gui)

    def crooks_algorithm_solve(self, puzzle, sudoku_markup, gui, i=0):
        if np.count_nonzero(sudoku_markup == None) == 9*9:
            return True
        
        changes_made = 0
        
        for r, row in enumerate(sudoku_markup):
            for c, markup in enumerate(row):
                if markup != None:
                    sudoku_markup, updates = self.find_preemtive_sets([r, c], sudoku_markup, gui)
                    changes_made += updates

                    if len(markup) == 1:
                        puzzle[r, c] = list(markup)[0]
                        sudoku_markup[r][c] = None
                        changes_made += 1
                        if gui: 
                            gui.show_number(r, c, list(markup)[0])
                            gui.add_number(r, c, list(markup)[0])

        if changes_made>0:
            return self.crooks_algorithm_solve(puzzle, sudoku_markup, gui, i+1)
        else:
            return False