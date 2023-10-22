#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 9
#define NUM_SUDOKUS 10
#define NUM_FIELDS 2
#define FILENAME "sudoku.csv"

int main() {
    FILE *file;
    char line[SIZE*SIZE];
    int sudoku[NUM_SUDOKUS];
    char *token;
    char *fields[NUM_FIELDS];
    const char *delimiter = ","; // CSV delimiter

    // Open the CSV file
    file = fopen(FILENAME, "r");
    if (file == NULL) {
        fprintf(stderr, "Error opening file.\n");
        return 1;
    }

    int i = 0; // Count number of sudokus

    // Read and process each line
    while (fgets(line, sizeof(line), file) && i < NUM_SUDOKUS) {
        int field_count = 0;

        // Tokenize the line
        token = strtok(line, delimiter);
        
        while (token != NULL && field_count < NUM_FIELDS) {
            sudoku[i] = token;
            token = strtok(NULL, delimiter);
            field_count++;
        }
        
        i++;
    }

    printf("%i ", sudoku);
    printf("\n");

    // Close the file
    fclose(file);

    return 0;
}