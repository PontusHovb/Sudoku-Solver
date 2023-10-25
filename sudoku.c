#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 9
#define NUM_SUDOKUS 10
#define NUM_FIELDS 2
#define FILENAME "sudoku.csv"

//bool correct_sudoku();
//bool bruteforce_solve();
//bool backtrack_solve();

int main() {
    FILE *file;
    char line[SIZE*SIZE];
    int sudoku[NUM_SUDOKUS][SIZE][SIZE];
    char *token;
    char *fields[NUM_FIELDS];
    const char *delimiter = ","; // CSV delimiter

    // Open the CSV file
    file = fopen(FILENAME, "r");
    if (file == NULL) {
        fprintf(stderr, "Error opening file.\n");
        return 1;
    }

    int n = 0; // Count number of sudokus

    // Read and process each line
    while (fgets(line, sizeof(line), file) && n < NUM_SUDOKUS) {
        int field_count = 0;

        // Tokenize the line
        token = strtok(line, delimiter);
        
        while (token != NULL && field_count < NUM_FIELDS) {
            if (field_count == 0 && n != 0) {
                int i = 0;
                while (token[i] != '\0') {
                    sudoku[n][i/SIZE][i%SIZE] = atoi(&token[i]);
                    i++;
                }
            }
            
            token = strtok(NULL, delimiter);
            field_count++;
        }
        
        n++;
    }
    // Printing the sudoku array
    for (int i = 0; i < NUM_SUDOKUS; i++) {
        printf("Sudoku %d:\n", i + 1);
        for (int j = 0; j < SIZE; j++) {
            for (int k = 0; k < SIZE; k++) {
                printf("%d ", sudoku[i][j][k]);
            }
            printf("\n");
        }
        printf("\n");
    }
    // Close the file
    fclose(file);

    return 0;
}