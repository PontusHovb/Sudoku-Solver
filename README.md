# Algorithms

## Bruteforce method
<img align="left" width="250" src="https://github.com/PontusHovb/Sudoku/blob/master/GIFs/bruteforce.gif"/>
<img align="left" width="50" src="https://github.com/PontusHovb/Sudoku/assets/67122081/5818307d-976f-4cfc-9ad9-cf1ef711ceb1"/>
In the bruteforce method, a guess is performed for each empty cell until all cells are filled. If sudoku is not correctly solved a new guess for the last empty cell is performed. This is an algorithm which is easy to implement but computationally inefficient.
<br clear="all"/>

## Bruteforce with look ahead (backtracking method)
<img align="left" width="250" src="https://github.com/PontusHovb/Sudoku/blob/master/GIFs/bruteforce_lookahead.gif"/>
<img align="left" width="50" src="https://github.com/PontusHovb/Sudoku/assets/67122081/5818307d-976f-4cfc-9ad9-cf1ef711ceb1"/>
An improvement to the bruteforce method can be done with the backtracking method where a guess (1-9) is performed for the first cell. If the guess is valid (does not violate sudoku-condition (same number is already in row, column and box)) then the function calls itself recursively with the remaining unsolved cells. This method can solve all solvable sudokus but often requires a lot of wrong tries before reaching the correct solution.
<br clear="all"/>

## Candidate-checking method
<img align="left" width="250" src="https://github.com/PontusHovb/Sudoku/blob/master/GIFs/candidate_checking.gif"/>
<img align="left" width="50" src="https://github.com/PontusHovb/Sudoku/assets/67122081/5818307d-976f-4cfc-9ad9-cf1ef711ceb1"/>
The candidate checking method for solving sudokus involve writing down all possible values for each empty cell. For each cell where there is only one possible value (naked single), that value must be the correct value and is inserted, and the rest of the empty cells are then updated. The advantage of this method is that it only inserts correct numbers but finding naked singles can be difficult and it is not guaranteed that it will reach a solution.
<br clear="all"/>

## Place-finding method
<img align="left" width="250" src="https://github.com/PontusHovb/Sudoku/blob/master/GIFs/place_finding.gif"/>
<img align="left" width="50" src="https://github.com/PontusHovb/Sudoku/assets/67122081/5818307d-976f-4cfc-9ad9-cf1ef711ceb1"/>
The place finding method iterate through each unsolved cell and try to find cells where the guess can only occur in that cell (naked singles). This means that the guess only can occur in one place in the specific row, column or box. If the guess has only one possible location in its row, column or box that must be the correct position and the guess is inserted.
<br clear="all"/>

## Crook's algorithm
<img align="left" width="250" src="https://github.com/PontusHovb/Sudoku/blob/master/GIFs/crooks_algorithm.gif"/>
<img align="left" width="50" src="https://github.com/PontusHovb/Sudoku/assets/67122081/5818307d-976f-4cfc-9ad9-cf1ef711ceb1"/>
Crook's algorithm is a pen and paper algorithm for finding sudokus. Crook's algorithm is an extension of the place-finding method, not only looking for naked singles but preemtive sets with $m>2$.
### Preemtive sets
Preemtive sets are cells with m numbers (2 $\le$ m $\le$ 8) that fill up m cells. Since these number must fill up the m cells they can be ruled out as possible values for other cells in row/column/box. Preemtive sets are also refered to as Naked Pairs (m=2), Naked Triplets (m=3) etc.  
<br clear="all"/>

# Evaluation 
Algorithms and code languages are tested on a various of parameters:
- Speed (average time to solve a sudoku)
- Accuracy (average number of tries to solve an empty cell)
- Solving ability (% of sudoku's solved)
- Memory allocation (average memory allocation per sudoku)

## Speed
The average time to solve a sudoku with each of the algorithms were as followed:
| Algorithm               | Python  | C        |
|-------------------------|---------|----------|
| Bruteforce              | -       | -        |
| Bruteforce w. lookahead | 15 ms   | 0.034 ms |
| Candidate-checking      | 21 ms   | 0.050 ms |
| Place-finding           | 74 ms   | 0.067 ms |
| Crook's Algorithm       | 4.5 ms  |          |

Crook's Algorithm is not yet implemented in C.

## Accuracy
Average number of tries per empty cell:
| Algorithm               | Avg. tries |
|-------------------------|------------|
| Bruteforce              | 9.0        |
| Bruteforce w. lookahead | 2.7        |
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
| Crook's Algorithm       |                |

This is equivalent to candidate checking not being able to solve 337 out of the 1.000.000 sudokus in the Kaggle-dataset.

## Memory allocation


# Source
Algorithms are tested on 1 million Sudoku games accessible on Kaggle (https://www.kaggle.com/datasets/bryanpark/sudoku)