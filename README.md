# Sudoku
Testing different algorithms for solving Sudoku.

Algorithms are tested on 1 million Sudoku games accessible through Kaggle (https://www.kaggle.com/datasets/bryanpark/sudoku)

### Backtracking method
In the backtracking method, a guess (1-9) is performed for the first cell. If the guess is valid (does not violate sudoku-condition (same number is already in row, column and box)) then the function calls itself recursively with the remaining unsolved cells. This is done until sudoku is solved or there are no possible value for remaining empty cell.

### Candidate-checking method
The candidate checking method for solving sudokus involve writing down all possible values for each empty cell.
For each cell where there is only one possible value, that value must be the correct value and is inserted, and the rest of the empty cells are then updated.

### Place-finding method
The place-finding method iterates through 1 to 9 and tries finding rows, columns or boxes where there is only one possible position for one value.

### Crook's algorithm
Crook's algorithm starts by using the candidate-checking and place-finding methods to solve these cells that can be solved with either of these methods. When no more cells can be sovled with these methods the backtracking method is used to solve the remaining cells.