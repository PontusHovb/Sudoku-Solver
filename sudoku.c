#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

#define FILENAME "sudoku.csv"
#define NO_PUZZLES 1
#define SIZE 9

// Function declarations
int read_quizzes(const char* filename, int puzzles, int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE]);
void print_sudoku(int sudoku[SIZE][SIZE]);
int correct_solution(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE]);
int get_all_unsolved(int (*sudoku)[SIZE][SIZE], int (*unsolved_cells)[SIZE*SIZE][2]);
int solve_sudoku(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE]);
int bruteforce(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolved_cells)[SIZE*SIZE][2], int unsolved_index, int no_unsolved_cells);
int bruteforce_lookahead(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolved_cells)[SIZE*SIZE][2], int unsolved_index, int no_unsolved_cells);
int validGuess(int r, int c, int guess, int (*sudoku)[SIZE][SIZE]);

int main() {
    int (*quizzes)[SIZE][SIZE] = malloc(NO_PUZZLES * sizeof(*quizzes));
    int (*solutions)[SIZE][SIZE] = malloc(NO_PUZZLES * sizeof(*solutions));
    int solved_sudokus = 0;

    // Load all sudokus
    clock_t start_time = clock();
    int count = read_quizzes(FILENAME, NO_PUZZLES, quizzes, solutions);
    clock_t download_end_time = clock();
    printf("It took %f seconds to load %d puzzles.\n", (double)(download_end_time - start_time) / CLOCKS_PER_SEC, count);

    // Solve all sudokus
    for (int i = 0; i < count; i++) {
        if (solve_sudoku(&quizzes[i], &solutions[i]) == 1) {
            solved_sudokus++;
        } 
    }  

    clock_t solve_end_time = clock();
    printf("Method solved %f%% of %d sudokus in %f seconds.\n",
           (double)solved_sudokus / NO_PUZZLES * 100, NO_PUZZLES,
           (double)(solve_end_time - download_end_time) / CLOCKS_PER_SEC);

    free(quizzes);
    free(solutions);
    return 1;
}

int read_quizzes(const char* filename, int puzzles, int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE]) {
    // Handle missing / corrupted file
    FILE *file = fopen(filename, "r");
    if (!file) {
        printf("Error opening file\n");
        return 0;
    }

    char line[1024];
    int puzzleCount = 0;
    int first_line = 1;

    // Read all sudokus
    while (fgets(line, sizeof(line), file) && puzzleCount < puzzles) {
        if (first_line) {
            first_line = 0;
            continue;
        }

        char *input_sudoku = strtok(line, ",");
        char *input_solution = strtok(NULL, "\n");

        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                sudoku[puzzleCount][i][j] = input_sudoku[i * SIZE + j] - '0';
                solution[puzzleCount][i][j] = input_solution[i * SIZE + j] - '0';
            }
        }
        puzzleCount++;
    }

    fclose(file);
    return puzzleCount;
}

void print_sudoku(int sudoku[SIZE][SIZE]) {
    for (int row = 0; row < SIZE; row++) {
        for (int col = 0; col < SIZE; col++) {
            printf("%2d", sudoku[row][col]);
        }
        printf("\n");
    }
}

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
        if (correct_solution(sudoku, solution) == 1) {
            return 1;
        }
        else {
            return 0;
        }
    }

    for (int num = 1; num <= 9; num++) {                                                                    // If empty cells left, make a guess for first empty cell
        (*sudoku)[(*unsolved_cells)[unsolved_index][0]][(*unsolved_cells)[unsolved_index][1]] = num;

        if (bruteforce(sudoku, solution, unsolved_cells, unsolved_index+1, no_unsolved_cells) == 1) {       // Recursive solving
            return 1;
        }

        (*sudoku)[(*unsolved_cells)[unsolved_index][0]][(*unsolved_cells)[unsolved_index][1]] = 0;          // Backtrack if guess don't yield solution
    }

    return 0;
}

int bruteforce_lookahead(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolved_cells)[SIZE*SIZE][2], int unsolved_index, int no_unsolved_cells) {
    if (unsolved_index == no_unsolved_cells) {
        if (correct_solution(sudoku, solution) == 1) {
            return 1;
        }
        else {
            return 0;
        }
    }

    for (int guess = 1; guess <= 9; guess++) {                                                                    // If empty cells left, make a guess for first empty cell
        if (validGuess((*unsolved_cells)[unsolved_index][0], (*unsolved_cells)[unsolved_index][1], guess, sudoku)) {
            (*sudoku)[(*unsolved_cells)[unsolved_index][0]][(*unsolved_cells)[unsolved_index][1]] = guess;

            if (bruteforce_lookahead(sudoku, solution, unsolved_cells, unsolved_index+1, no_unsolved_cells) == 1) {       // Recursive solving
                return 1;
            }
            
            (*sudoku)[(*unsolved_cells)[unsolved_index][0]][(*unsolved_cells)[unsolved_index][1]] = 0;          // Backtrack if guess don't yield solution
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
    int unsolved_cells[SIZE*SIZE][2] = {{0}};;
    int unsolved_index = 0;
    int no_unsolved_cells = get_all_unsolved(sudoku, &unsolved_cells);
    return bruteforce(sudoku, solution, &unsolved_cells, unsolved_index, no_unsolved_cells);
}
