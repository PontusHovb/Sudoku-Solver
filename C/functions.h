#define FILENAME "../Data/sudoku.csv"
#define NO_PUZZLES 1000000
#define SIZE 9
#define ALGORITHM "BruteforceLookAhead"

#ifndef solver_h
#define solver_h

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

int ReadQuizzes(const char* filename, int puzzles, int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE]);
void PrintSudoku(int (*sudoku)[SIZE][SIZE]);

int CorrectSolution(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE]);
int GetCandidates(int (*sudoku)[SIZE][SIZE], int row, int col);
int GetAllUnsolved(int (*sudoku)[SIZE][SIZE], int (*unsolvedCells)[SIZE*SIZE][2]);
int IsOnlyPossibleLocation(int (*sudoku)[SIZE][SIZE], int row, int col, int guess, char checkType[3]);
int SolveSudoku(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE]);
int Bruteforce(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolvedCells)[SIZE*SIZE][2], int unsolvedIndex, int noUnsolvedCells);
int BruteforceLookAhead(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolvedCells)[SIZE*SIZE][2], int unsolvedIndex, int noUnsolvedCells);
int CandidateChecking(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolvedCells)[SIZE*SIZE][2], int noUnsolvedCells);
int PlaceFinding(int (*sudoku)[SIZE][SIZE], int (*solution)[SIZE][SIZE], int (*unsolvedCells)[SIZE*SIZE][2], int noUnsolvedCells);
int ValidGuess(int row, int col, int guess, int (*sudoku)[SIZE][SIZE]);

#endif