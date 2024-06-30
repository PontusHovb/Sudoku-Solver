CC = gcc
CFLAGS = -Wall -Wextra -std=c11
TARGET = sudoku

all: $(TARGET)

$(TARGET): sudoku.o solver.o
	$(CC) $(CFLAGS) -o $(TARGET) sudoku.o solver.o

sudoku.o: sudoku.c functions.h
	$(CC) $(CFLAGS) -c sudoku.c

solver.o: solver.c functions.h
	$(CC) $(CFLAGS) -c solver.c

clean:
	rm -f *.o $(TARGET)