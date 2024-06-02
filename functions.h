#define FILENAME "sudoku.csv"
#define NO_PUZZLES 100
#define SIZE 9
#define ALGORITHM "bruteforce_lookahead"

#ifndef solver_h
#define solver_h

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

int read_quizzes(const char* filename, int puzzles, int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE]);
void print_sudoku(int (*sudoku)[SIZE][SIZE]);

int correct_solution(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE]);
int get_candidates(int (*sudoku)[SIZE][SIZE], int row, int col);
int get_all_unsolved(int (*sudoku)[SIZE][SIZE], int (*unsolved_cells)[SIZE*SIZE][2]);
int solve_sudoku(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE]);
int bruteforce(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolved_cells)[SIZE*SIZE][2], int unsolved_index, int no_unsolved_cells);
int bruteforce_lookahead(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolved_cells)[SIZE*SIZE][2], int unsolved_index, int no_unsolved_cells);
int candidate_checking(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolved_cells)[SIZE*SIZE][2], int unsolved_index, int no_unsolved_cells);
int place_finding(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolved_cells)[SIZE*SIZE][2], int unsolved_index, int no_unsolved_cells);
int validGuess(int r, int c, int guess, int (*sudoku)[SIZE][SIZE]);

#endif