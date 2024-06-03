# Sudoku
Testing different algorithms and code languages for solving the game Sudoku.

Algorithms are tested on 1 million Sudoku games accessible through Kaggle (https://www.kaggle.com/datasets/bryanpark/sudoku)

# Evaluation 
Algorithms are tested on a various of parameters:
- Time (average time to solve a sudoku)
- Misses (number of times solver guessed on a wrong value)
- Percentage of sudokus solved (how many of total sudokus where algorithm able to solve)

## Average time
The average time to solve a sudoku with each of the algorithms were as followed:
| Algorithm               | Python | C       | C vs. Python |
|-------------------------|--------|---------|--------------|
| Bruteforce w. lookahead | 14 ms  | 0.03 ms | -99.8%       |
| Candidate-checking      | 25 ms  | 0.05 ms | -99.8%       |

# Algorithms
## Brute-force method
In the backtracking method, a guess (1-9) is performed for the first cell. If the guess is valid (does not violate sudoku-condition (same number is already in row, column and box)) then the function calls itself recursively with the remaining unsolved cells. This is done until sudoku is solved or there are no possible value for remaining empty cell.

This is the simpliest method for solving sudokus numerically and is therefore set as the base-case for which improved methods are compared. This algorithm is simple to implement but often causes a lot of misses and can therefore be computationally inefficient.

## Candidate-checking method
The candidate checking method for solving sudokus involve writing down all possible values for each empty cell.
For each cell where there is only one possible value, that value must be the correct value and is inserted, and the rest of the empty cells are then updated.
Naked single

## Crook's algorithm
Crook's algorithm starts by using the candidate-checking and place-finding methods to solve these cells that can be solved with either of these methods. When no more cells can be sovled with these methods the backtracking method is used to solve the remaining cells.

### Preemtive sets
Preemtive sets are cells with m numbers (2 $\le$ m $\le$ 8) that fill up m cells. Since these number must fill up the m cells they can be ruled out as possible values for other cells in row/column/box. Preemtive sets are also refered to as Naked Pairs (m=2), Naked Triplets (m=3) etc.  
