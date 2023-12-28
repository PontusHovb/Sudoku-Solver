% define the puzzle to be solved
board = [0,0,6, 0,0,8, 5,0,0 ; ...
         0,0,0, 0,7,0, 6,1,3 ; ...
         0,0,0, 0,0,0, 0,0,9 ; ...
         0,0,0, 0,9,0, 0,0,1 ; ...
         0,0,1, 0,0,0, 8,0,0 ; ...
         4,0,0, 5,3,0, 0,0,0 ; ...
         1,0,7, 0,5,3, 0,0,0 ; ...
         0,5,0, 0,6,4, 0,0,0 ; ...
         3,0,0, 1,0,0, 0,6,0 ]

% The following code solves the Sudoku puzzle from above, in which zeros 
% denote empty cells of the Sudoku board. 
% The code returns a completed Sudoku puzzle if there is at
% least one solution, otherwise it returns a matrix with at least one zero
% entry.

% initialize some variables
cell_ctr = 1;       % cell-counter
ini_board = board;  % make a copy of the untouched Sudoku board
updown = 1;         % variable to keep track of direction (forward-backward on board)
 
% main solving loop: the counter cell_ctr moves back and forth between 1
% and 81. The algorithm stops when 0 is reached (the puzzle has no
% solution), or when 82 is reached (a solution has been found)
while (cell_ctr>0) && (cell_ctr<82)
    
    % case: current cell was originally empty, and entry 9 was not tested yet
    if (ini_board(1+floor((cell_ctr-1)/9),1+mod(cell_ctr-1,9))==0) ...
        && ...
       (board(1+floor((cell_ctr-1)/9),1+mod(cell_ctr-1,9))<9) 
        updown = 1;
        board(1+floor((cell_ctr-1)/9),1+mod(cell_ctr-1,9)) ...
            = board(1+floor((cell_ctr-1)/9),1+mod(cell_ctr-1,9)) + 1;
        anydouble
        if ~double % case there are no doubles
            cell_ctr = cell_ctr + 1; % proceed to next cell
        end
        
    % case: current cell was originally empty, but we have tried all
    % possible entries
    elseif ini_board(1+floor((cell_ctr-1)/9),1+mod(cell_ctr-1,9))==0 
        board(1+floor((cell_ctr-1)/9),1+mod(cell_ctr-1,9)) = 0;
        cell_ctr = cell_ctr -1;
        updown = -1; 
    
    % case: current cell was filled at the beginning. Jump to next cell. 
    else 
        if updown==1 
            cell_ctr = cell_ctr +1; % if you were going forward, keep doing it
        else
            cell_ctr = cell_ctr -1; % if you were going backward, keep doing it
        end
    end
    
end

% display the solved Sudoku
board