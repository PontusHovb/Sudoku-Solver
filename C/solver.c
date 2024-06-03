#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include "functions.h"

// Check if solution is correct
int CorrectSolution(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE]) {
    for (int row = 0; row < SIZE; row++) {
        for (int col = 0; col < SIZE; col++) {
            if ((*sudoku)[row][col] != (*solution)[row][col]) {
                return 0;
            }
        }
    }
    return 1;
}

int Bruteforce(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolvedCells)[SIZE*SIZE][2], int unsolvedIndex, int noUnsolvedCells) {
    if (unsolvedIndex == noUnsolvedCells) {
        return CorrectSolution(sudoku, solution);
    }

    for (int num = 1; num <= 9; num++) {                                                                    // If empty cells left, make a guess for first empty cell
        (*sudoku)[(*unsolvedCells)[unsolvedIndex][0]][(*unsolvedCells)[unsolvedIndex][1]] = num;

        if (Bruteforce(sudoku, solution, unsolvedCells, unsolvedIndex+1, noUnsolvedCells) == 1) {       // Recursive solving
            return 1;
        }
        else {
            (*sudoku)[(*unsolvedCells)[unsolvedIndex][0]][(*unsolvedCells)[unsolvedIndex][1]] = 0;      // Backtrack if guess don't yield solution
        }
    }

    return 0;
}

int BruteforceLookAhead(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolvedCells)[SIZE*SIZE][2], int unsolvedIndex, int noUnsolvedCells) {
    if (unsolvedIndex == noUnsolvedCells) {
        return CorrectSolution(sudoku, solution);
    }

    for (int guess = 1; guess <= 9; guess++) {                                                                    // If empty cells left, make a guess for first empty cell
        if (ValidGuess((*unsolvedCells)[unsolvedIndex][0], (*unsolvedCells)[unsolvedIndex][1], guess, sudoku)) {
            (*sudoku)[(*unsolvedCells)[unsolvedIndex][0]][(*unsolvedCells)[unsolvedIndex][1]] = guess;

            if (BruteforceLookAhead(sudoku, solution, unsolvedCells, unsolvedIndex+1, noUnsolvedCells) == 1) {       // Recursive solving
                return 1;
            }
            else {
                (*sudoku)[(*unsolvedCells)[unsolvedIndex][0]][(*unsolvedCells)[unsolvedIndex][1]] = 0;          // Backtrack if guess don't yield solution
            }
        }
    }

    return 0;
}

int CandidateChecking(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolvedCells)[SIZE*SIZE][2], int unsolvedIndex, int noUnsolvedCells) {
    // Loop through unsolved cells until no more cell can be solved
    int solvedIter = 1;             // Used for initialization
    int solvedPrevIter = 0;        

    while (solvedIter > solvedPrevIter) {
        solvedPrevIter = solvedIter;
        solvedIter = 0;

        // Test all unsolved cells
        for (int i = 0; i < noUnsolvedCells; i++) {
            int possibleValues = 0;
            int possibleGuess;
            for (int guess = 1; guess <= 9; guess++) {
                if (ValidGuess((*unsolvedCells)[i][0], (*unsolvedCells)[i][1], guess, sudoku)) {
                    possibleGuess = guess;
                    possibleValues++;
                }
            }

            if (possibleValues == 1) {
                (*sudoku)[(*unsolvedCells)[i][0]][(*unsolvedCells)[i][1]] = possibleGuess;
                solvedIter++;
            }
        }

        if (CorrectSolution(sudoku, solution)) {
            return 1;
        }
    }
    return 0;
}

int get_all_unsolved(int (*sudoku)[SIZE][SIZE], int (*unsolvedCells)[SIZE*SIZE][2]) {
    int noUnsolvedCells = 0;  // Initialize the count of unsolved cells
    for (int row = 0; row < SIZE; row++) {
        for (int col = 0; col < SIZE; col++) {
            if ((*sudoku)[row][col] == 0) {
                (*unsolvedCells)[noUnsolvedCells][0] = row;
                (*unsolvedCells)[noUnsolvedCells][1] = col;
                noUnsolvedCells++;
            }
        }
    }
    return noUnsolvedCells;
}

int ValidGuess(int row, int col, int guess, int (*sudoku)[SIZE][SIZE]) {
    // Check if guess is in row
    for (int i = 0; i < SIZE; i++) {
        if ((*sudoku)[row][i] == guess && i != col) {
            return 0;
        }
    }

    // Check if guess is in column
    for (int i = 0; i < SIZE; i++) {
        if ((*sudoku)[i][col] == guess && i != row) {
            return 0;
        }
    }

    // Check if guess is in the 3x3 square
    int startRow = 3 * (row / 3);
    int startCol = 3 * (col / 3);
    for (int r = startRow; r < startRow + 3; r++) {
        for (int c = startCol; c < startCol + 3; c++) {
            if ((*sudoku)[r][c] == guess && r != row && c != col) {
                return 0;
            }
        }
    }

    return 1;
}

// Choose which algorithm to use
int SolveSudoku(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE]) {
    int unsolvedCells[SIZE*SIZE][2] = {{0}};
    int unsolvedIndex = 0;
    int noUnsolvedCells = get_all_unsolved(sudoku, &unsolvedCells);

    if (strcmp(ALGORITHM, "Bruteforce") == 0) {
        return Bruteforce(sudoku, solution, &unsolvedCells, unsolvedIndex, noUnsolvedCells);
    }
    else if (strcmp(ALGORITHM, "BruteforceLookAhead") == 0) {
        return BruteforceLookAhead(sudoku, solution, &unsolvedCells, unsolvedIndex, noUnsolvedCells);
    }
    else if (strcmp(ALGORITHM, "CandidateChecking") == 0) {
        return CandidateChecking(sudoku, solution, &unsolvedCells, unsolvedIndex, noUnsolvedCells);
    }
    else {
        printf("Choose valid algorithm\n");
        return 0;
    }
}