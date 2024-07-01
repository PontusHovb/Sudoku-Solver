# Algorithms

## Bruteforce method
<img align="left" width="250" src="https://github.com/PontusHovb/Sudoku/blob/master/GIFs%20%26%20Graphs/bruteforce.gif"/>
<img align="left" width="50" src="https://github.com/PontusHovb/Sudoku/assets/67122081/5818307d-976f-4cfc-9ad9-cf1ef711ceb1"/>
In the bruteforce method, a guess is performed for each empty cell until all cells are filled. If sudoku is not correctly solved a new guess for the last empty cell is performed. This is an algorithm which is easy to implement but computationally inefficient.
<br clear="all"/>

## Bruteforce with look ahead (backtracking method)
<img align="left" width="250" src="https://github.com/PontusHovb/Sudoku/blob/master/GIFs%20%26%20Graphs/bruteforce_lookahead.gif"/>
<img align="left" width="50" src="https://github.com/PontusHovb/Sudoku/assets/67122081/5818307d-976f-4cfc-9ad9-cf1ef711ceb1"/>
An improvement to the bruteforce method can be done with the backtracking method where a guess (1-9) is performed for the first cell. If the guess is valid (does not violate sudoku-condition (same number is already in row, column and box)) then the function calls itself recursively with the remaining unsolved cells. This method can solve all solvable sudokus but often requires a lot of wrong tries before reaching the correct solution.
<br clear="all"/>

## Candidate-checking method
<img align="left" width="250" src="https://github.com/PontusHovb/Sudoku/blob/master/GIFs%20%26%20Graphs/candidate_checking.gif"/>
<img align="left" width="50" src="https://github.com/PontusHovb/Sudoku/assets/67122081/5818307d-976f-4cfc-9ad9-cf1ef711ceb1"/>
The candidate checking method for solving sudokus involve writing down all possible values for each empty cell. For each cell where there is only one possible value (naked single), that value must be the correct value and is inserted, and the rest of the empty cells are then updated. The advantage of this method is that it only inserts correct numbers but finding naked singles can be difficult and it is not guaranteed that it will reach a solution.
<br clear="all"/>

## Place-finding method
<img align="left" width="250" src="https://github.com/PontusHovb/Sudoku/blob/master/GIFs%20%26%20Graphs/place_finding.gif"/>
<img align="left" width="50" src="https://github.com/PontusHovb/Sudoku/assets/67122081/5818307d-976f-4cfc-9ad9-cf1ef711ceb1"/>
The place finding method iterate through each unsolved cell and try to find cells where the guess can only occur in that cell (naked singles). This means that the guess only can occur in one place in the specific row, column or box. If the guess has only one possible location in its row, column or box that must be the correct position and the guess is inserted.
<br clear="all"/>

## Crook's algorithm
<img align="left" width="250" src="https://github.com/PontusHovb/Sudoku/blob/master/GIFs%20%26%20Graphs/crooks_algorithm.gif"/>
<img align="left" width="50" src="https://github.com/PontusHovb/Sudoku/assets/67122081/5818307d-976f-4cfc-9ad9-cf1ef711ceb1"/>
Crook's algorithm is a pen and paper algorithm for solving sudokus. Crook's algorithm is an extension of the place-finding method, not only looking for naked singles but preemtive sets with m>2. Preemtive sets are cells with m numbers (between 2 and 8) that fill up m cells. Since these number must fill up the m cells they can be ruled out as possible values for other cells in row/column/box. Preemtive sets are also refered to as Naked Pairs (m=2), Naked Triplets (m=3) etc.  
<br clear="all"/>

# Evaluation 
Algorithms and code languages are tested on a various of parameters:
- Speed (average time to solve a sudoku)
- Accuracy (average number of tries to solve an empty cell)
- Solving ability (% of sudoku's solved)

## Speed
The average time to solve a sudoku with each of the algorithms were as followed:
The algorithms are tested by solving 100 random sudokus each iteration and the times for python were as followed:
<br clear="all"/>
<img width="350" src="https://github.com/PontusHovb/Sudoku/blob/master/GIFs%20%26%20Graphs/average_time.png"/>

Exact times both in Python and C:
| Algorithm               | Python  | C        |
|-------------------------|---------|----------|
| Bruteforce              | -       | -        |
| Bruteforce w. lookahead | 14.9 ms | 0.033 ms |
| Candidate-checking      | 23.3 ms | 0.054 ms |
| Place-finding           | 82.3 ms | 0.071 ms |
| Crook's Algorithm       | 4.3 ms  | 0.149 ms |

Bruteforce is considerable slower than the other algorithms, and can't be tested in a reasonable time.

## Accuracy
Average number of tries per empty cell:
| Algorithm               | Avg. tries |
|-------------------------|------------|
| Bruteforce              | 8.9        |
| Bruteforce w. lookahead | 3.0        |
| Candidate-checking      | 1.0        |
| Place-finding           | 1.0        |
| Crook's Algorithm       | 1.0        |

## Solving ability
Percentage of sudokus solved:
| Algorithm               | Sudokus solved |
|-------------------------|----------------|
| Bruteforce              | 100.0000%      |
| Bruteforce w. lookahead | 100.0000%      |
| Candidate-checking      | 99.9663%       |
| Place-finding           | 58.8468%       |
| Crook's Algorithm       | 100.000%       |

This is equivalent to candidate checking not being able to solve 337 out of the 1.000.000 sudokus in the Kaggle-dataset.

# Source
Algorithms are tested on 1 million Sudoku games accessible on Kaggle (https://www.kaggle.com/datasets/bryanpark/sudoku)
