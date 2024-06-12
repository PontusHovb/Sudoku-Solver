# Sudoku
Testing different algorithms and code languages for solving the game Sudoku.

Algorithms are tested on 1 million Sudoku games accessible through Kaggle (https://www.kaggle.com/datasets/bryanpark/sudoku)

# Algorithms
## Bruteforce method
<p align=left>
<img width=250 src="https://github.com/PontusHovb/Sudoku/blob/master/GIFs/bruteforce.gif" />
</p>
In the bruteforcee method, a guess is performed for each empty cell until all cells are filled. If sudoku is not correctly solved a new guess for the last empty cell is performed. This is an algorithm which is easy to implement but computationally inefficient since it requires a maximum of $9^{\text{no. empty cells}}$ tries until the sudoku is solved.

## Bruteforce with look ahead (backtracking method)
<p align=left>
<img width=250 src="https://github.com/PontusHovb/Sudoku/blob/master/GIFs/bruteforce_lookahead.gif" />
</p>
An improvement to the bruteforce method can be done with the backtracking method where a guess (1-9) is performed for the first cell. If the guess is valid (does not violate sudoku-condition (same number is already in row, column and box)) then the function calls itself recursively with the remaining unsolved cells. This method can solve all solvable sudokus but often requires a lot of wrong tries before reaching the correct solution.

## Candidate-checking method
<p align=left>
<img width=250 src="https://github.com/PontusHovb/Sudoku/blob/master/GIFs/candidate_checking.gif" />
</p>
The candidate checking method for solving sudokus involve writing down all possible values for each empty cell. For each cell where there is only one possible value (naked single), that value must be the correct value and is inserted, and the rest of the empty cells are then updated. The advantage of this method is that it only inserts correct numbers but finding naked singles can be difficult and it is not guaranteed that it will reach a solution.

## Crook's algorithm
Crook's algorithm starts by using the candidate-checking and place-finding methods to solve these cells that can be solved with either of these methods. When no more cells can be sovled with these methods the backtracking method is used to solve the remaining cells.

### Preemtive sets
Preemtive sets are cells with m numbers (2 $\le$ m $\le$ 8) that fill up m cells. Since these number must fill up the m cells they can be ruled out as possible values for other cells in row/column/box. Preemtive sets are also refered to as Naked Pairs (m=2), Naked Triplets (m=3) etc.  

# Evaluation 
Algorithms and code languages are tested on a various of parameters:
- Speed (average time to solve a sudoku)
- Accuracy (average number of tries to solve an empty cell)
- Solving ability (% of sudoku's solved)
- Memory allocation (average memory allocation per sudoku)

## Speed
The average time to solve a sudoku with each of the algorithms were as followed:
| Algorithm               | Python | C       |
|-------------------------|--------|---------|
| Bruteforce w. lookahead | 14 ms  | 0.08 ms |
| Candidate-checking      | 25 ms  | 0.10 ms |

## Accuracy
The number of misses per algorithm:
| Algorithm               | Misses |
|-------------------------|--------|
| Bruteforce w. lookahead | 84     |
| Candidate-checking      | 0      |

## Solving ability
Percentage of sudokus solved:
| Algorithm               | Sudokus solved |
|-------------------------|----------------|
| Bruteforce w. lookahead | 100.00%        |
| Candidate-checking      | 99.96%         |

This is equivalent to candidate checking not being able to solve 337 out of the 1.000.000 sudokus in the Kaggle-dataset.

## Memory allocation
