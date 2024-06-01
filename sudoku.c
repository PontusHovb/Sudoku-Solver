#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

#define FILENAME "hard_sudoku.csv"
#define NO_PUZZLES 1
#define SIZE 9

// Function declarations
int read_quizzes(const char* filename, int puzzles, int sudoku[NO_PUZZLES][SIZE][SIZE], int solution[NO_PUZZLES][SIZE][SIZE]);
void print_sudoku(int sudoku[SIZE][SIZE]);
int solve_sudoku(int sudoku[SIZE][SIZE], int row, int col);
int is_valid(int sudoku[SIZE][SIZE], int guess, int row, int col);
int find_unassigned_location(int sudoku[SIZE][SIZE], int *row, int *col);

int main() {
    int quizzes[NO_PUZZLES][SIZE][SIZE] = {0};
    int solutions[NO_PUZZLES][SIZE][SIZE] = {0};
    int solved_sudokus = 0;

    // Load all sudokus
    clock_t start_time = clock();
    int count = read_quizzes(FILENAME, NO_PUZZLES, quizzes, solutions);
    clock_t download_end_time = clock();
    printf("It took %f seconds to load %d puzzles.\n", (double)(download_end_time - start_time) / CLOCKS_PER_SEC, count);

    // Solve all sudokus
    for (int i = 0; i < count; i++) {
        print_sudoku(quizzes[i]);
        printf("\n\n");
        if (solve_sudoku(quizzes[i], 0, 0)) {
            solved_sudokus++;
            printf("Sudoku %d solved!\n", i + 1);
            print_sudoku(quizzes[i]);
        } else {
            printf("Sudoku %d not solved!\n", i + 1);
        }
    }

    clock_t solve_end_time = clock();
    printf("Method solved %f%% of %d sudokus in %f seconds.\n",
           (double)solved_sudokus / NO_PUZZLES * 100, NO_PUZZLES,
           (double)(solve_end_time - download_end_time) / CLOCKS_PER_SEC);

    return 0;
}

int read_quizzes(const char* filename, int puzzles, int sudoku[NO_PUZZLES][SIZE][SIZE], int solution[NO_PUZZLES][SIZE][SIZE]) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        printf("Error opening file\n");
        return 0;
    }

    char line[256];
    int puzzle_count = 0;
    while (fgets(line, sizeof(line), file) && puzzle_count < puzzles) {
        char* token = strtok(line, ",");
        if (token != NULL) {
            for (int row = 0; row < SIZE; row++) {
                for (int col = 0; col < SIZE; col++) {
                    int index = row * SIZE + col;
                    printf("%c", token[index]);
                    // Only process numeric input for the puzzle
                    if (isdigit(token[index])) {
                        sudoku[puzzle_count][row][col] = token[index] - '0';
                    } else {
                        sudoku[puzzle_count][row][col] = 0;  // Non-numeric input is handled as '0'
                    }
                    // Only process numeric input for the solution
                    int solution_index = SIZE * SIZE + 1 + index; // assuming there is exactly one character (comma) separator
                    if (isdigit(token[solution_index])) {
                        solution[puzzle_count][row][col] = token[solution_index] - '0';
                    } else {
                        solution[puzzle_count][row][col] = 0;  // Non-numeric input is handled as '0'
                    }
                }
            }
            puzzle_count++;
        }
    }

    fclose(file);
    return puzzle_count;
}

void print_sudoku(int sudoku[SIZE][SIZE]) {
    for (int row = 0; row < SIZE; row++) {
        for (int col = 0; col < SIZE; col++) {
            printf("%2d", sudoku[row][col]);
        }
        printf("\n");
    }
}

int solve_sudoku(int sudoku[SIZE][SIZE], int row, int col) {
    int r, c;

    if (!find_unassigned_location(sudoku, &r, &c)) {
        return 1;  // Success!
    }

    for (int num = 1; num <= 9; num++) {
        if (is_valid(sudoku, num, r, c)) {
            sudoku[r][c] = num;

            if (solve_sudoku(sudoku, r, c)) {
                return 1;
            }

            sudoku[r][c] = 0;  // Backtrack
        }
    }
    return 0;  // This triggers backtracking
}

int find_unassigned_location(int sudoku[SIZE][SIZE], int *row, int *col) {
    for (*row = 0; *row < SIZE; (*row)++) {
        for (*col = 0; *col < SIZE; (*col)++) {
            if (sudoku[*row][*col] == 0) {
                return 1;
            }
        }
    }
    return 0;
}

int is_valid(int sudoku[SIZE][SIZE], int guess, int row, int col) {
    for (int i = 0; i < SIZE; i++) {
        if (sudoku[row][i] == guess) return 0;  // Check row
        if (sudoku[i][col] == guess) return 0;  // Check column
        if (sudoku[3 * (row / 3) + i / 3][3 * (col / 3) + i % 3] == guess) return 0;  // Check box
    }
    return 1;
}
