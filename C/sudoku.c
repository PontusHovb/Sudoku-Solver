#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include "functions.h"

int main() {
    int (*quizzes)[SIZE][SIZE] = malloc(NO_PUZZLES * sizeof(*quizzes));
    int (*solutions)[SIZE][SIZE] = malloc(NO_PUZZLES * sizeof(*solutions));
    int solvedSudokus = 0;

    // Load all sudokus
    clock_t startTime = clock();
    int count = ReadQuizzes(FILENAME, NO_PUZZLES, quizzes, solutions);
    clock_t downloadEndTime = clock();
    printf("It took %f seconds to load %d puzzles.\n", (double)(downloadEndTime - startTime) / CLOCKS_PER_SEC, count);

    // Solve all sudokus
    for (int i = 0; i < count; i++) {
        if (SolveSudoku(&quizzes[i], &solutions[i]) == 1) {
            solvedSudokus++;
        } 
    }  

    clock_t solve_end_time = clock();
    printf("Method solved %f%% of %d sudokus in %f seconds.\n",
           (double)solvedSudokus / NO_PUZZLES * 100, NO_PUZZLES,
           (double)(solve_end_time - downloadEndTime) / CLOCKS_PER_SEC);

    free(quizzes);
    free(solutions);
    return 1;
}

int ReadQuizzes(const char* filename, int puzzles, int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE]) {
    // Handle missing / corrupted file
    FILE *file = fopen(filename, "r");
    if (!file) {
        printf("Error opening file\n");
        return 0;
    }

    char line[1024];
    int puzzleCount = 0;
    int firstLine = 1;

    // Read all sudokus
    while (fgets(line, sizeof(line), file) && puzzleCount < puzzles) {
        if (firstLine) {
            firstLine = 0;
            continue;
        }

        char *inputSudoku = strtok(line, ",");
        char *inputSolution = strtok(NULL, "\n");

        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                sudoku[puzzleCount][i][j] = inputSudoku[i * SIZE + j] - '0';
                solution[puzzleCount][i][j] = inputSolution[i * SIZE + j] - '0';
            }
        }
        puzzleCount++;
    }

    fclose(file);
    return puzzleCount;
}

void PrintSudoku(int (*sudoku)[SIZE][SIZE]) {
    for (int row = 0; row < SIZE; row++) {
        for (int col = 0; col < SIZE; col++) {
            printf("%2d", (*sudoku)[row][col]);
        }
        printf("\n");
    }
}