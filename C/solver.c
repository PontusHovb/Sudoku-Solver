#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include "functions.h"

// Check if solution is correct
int correct_solution(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE]) {
    for (int row = 0; row < SIZE; row++) {
        for (int col = 0; col < SIZE; col++) {
            if ((*sudoku)[row][col] != (*solution)[row][col]) {
                return 0;
            }
        }
    }
    return 1;
}

int bruteforce(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolved_cells)[SIZE*SIZE][2], int unsolved_index, int no_unsolved_cells) {
    if (unsolved_index == no_unsolved_cells) {
        return correct_solution(sudoku, solution);
    }

    for (int num = 1; num <= 9; num++) {                                                                    // If empty cells left, make a guess for first empty cell
        (*sudoku)[(*unsolved_cells)[unsolved_index][0]][(*unsolved_cells)[unsolved_index][1]] = num;

        if (bruteforce(sudoku, solution, unsolved_cells, unsolved_index+1, no_unsolved_cells) == 1) {       // Recursive solving
            return 1;
        }
        else {
            (*sudoku)[(*unsolved_cells)[unsolved_index][0]][(*unsolved_cells)[unsolved_index][1]] = 0;      // Backtrack if guess don't yield solution
        }
    }

    return 0;
}

int bruteforce_lookahead(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolved_cells)[SIZE*SIZE][2], int unsolved_index, int no_unsolved_cells) {
    if (unsolved_index == no_unsolved_cells) {
        return correct_solution(sudoku, solution);
    }

    for (int guess = 1; guess <= 9; guess++) {                                                                    // If empty cells left, make a guess for first empty cell
        if (validGuess((*unsolved_cells)[unsolved_index][0], (*unsolved_cells)[unsolved_index][1], guess, sudoku)) {
            (*sudoku)[(*unsolved_cells)[unsolved_index][0]][(*unsolved_cells)[unsolved_index][1]] = guess;

            if (bruteforce_lookahead(sudoku, solution, unsolved_cells, unsolved_index+1, no_unsolved_cells) == 1) {       // Recursive solving
                return 1;
            }
            else {
                (*sudoku)[(*unsolved_cells)[unsolved_index][0]][(*unsolved_cells)[unsolved_index][1]] = 0;          // Backtrack if guess don't yield solution
            }
        }
    }

    return 0;
}

int candidate_checking(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolved_cells)[SIZE*SIZE][2], int unsolved_index, int no_unsolved_cells) {
    // Loop through unsolved cells until no more cell can be solved
    int solvedIter = 1;             // Used for initialization
    int solvedPrevIter = 0;        

    while (solvedIter > solvedPrevIter) {
        solvedPrevIter = solvedIter;
        solvedIter = 0;

        // Test all unsolved cells
        for (int i = 0; i < no_unsolved_cells; i++) {
            int possible_values = 0;
            int possible_guess;
            for (int guess = 1; guess <= 9; guess++) {
                if (validGuess((*unsolved_cells)[i][0], (*unsolved_cells)[i][1], guess, sudoku)) {
                    possible_guess = guess;
                    possible_values++;
                }
            }

            if (possible_values == 1) {
                (*sudoku)[(*unsolved_cells)[i][0]][(*unsolved_cells)[i][1]] = possible_guess;
                solvedIter++;
            }
        }

        if (correct_solution(sudoku, solution)) {
            return 1;
        }
    }
    return 0;
}

int get_all_unsolved(int (*sudoku)[SIZE][SIZE], int (*unsolved_cells)[SIZE*SIZE][2]) {
    int no_unsolved_cells = 0;  // Initialize the count of unsolved cells
    for (int row = 0; row < SIZE; row++) {
        for (int col = 0; col < SIZE; col++) {
            if ((*sudoku)[row][col] == 0) {
                (*unsolved_cells)[no_unsolved_cells][0] = row;
                (*unsolved_cells)[no_unsolved_cells][1] = col;
                no_unsolved_cells++;
            }
        }
    }
    return no_unsolved_cells;
}

int validGuess(int r, int c, int guess, int (*sudoku)[SIZE][SIZE]) {
    // Check if guess is in row
    for (int i = 0; i < SIZE; i++) {
        if ((*sudoku)[r][i] == guess && i != c) {
            return 0;
        }
    }

    // Check if guess is in column
    for (int i = 0; i < SIZE; i++) {
        if ((*sudoku)[i][c] == guess && i != r) {
            return 0;
        }
    }

    // Check if guess is in the 3x3 square
    int start_row = 3 * (r / 3);
    int start_col = 3 * (c / 3);
    for (int row = start_row; row < start_row + 3; row++) {
        for (int col = start_col; col < start_col + 3; col++) {
            if ((*sudoku)[row][col] == guess && row != r && col != c) {
                return 0;
            }
        }
    }

    return 1;
}

// Choose which algorithm to use
int solve_sudoku(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE]) {
    int unsolved_cells[SIZE*SIZE][2] = {{0}};
    int unsolved_index = 0;
    int no_unsolved_cells = get_all_unsolved(sudoku, &unsolved_cells);

    if (strcmp(ALGORITHM, "bruteforce") == 0) {
        return bruteforce(sudoku, solution, &unsolved_cells, unsolved_index, no_unsolved_cells);
    }
    else if (strcmp(ALGORITHM, "bruteforce_lookahead") == 0) {
        return bruteforce_lookahead(sudoku, solution, &unsolved_cells, unsolved_index, no_unsolved_cells);
    }
    else if (strcmp(ALGORITHM, "candidate_checking") == 0) {
        return candidate_checking(sudoku, solution, &unsolved_cells, unsolved_index, no_unsolved_cells);
    }
    else {
        printf("Choose valid algorithm");
        return 0;
    }
}