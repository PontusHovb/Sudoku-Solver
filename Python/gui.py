import math
import time
import sys
import os
import contextlib

# Import pygame without welcome message
with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
    import pygame

SIZE = 9
PUZZLE_SIZE = 450
MARGINS = 0
DURATION = 0.002
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 139)
LIGHT_BLUE = (173, 216, 230)
LIGHT_YELLOW = (255, 255, 144)
LIGHT_GREEN = (144, 230, 201)

class GUI():
    def __init__(self, puzzle, title):
        pygame.init()
        self.font = pygame.font.Font(None, 36)
        self.markup_font = pygame.font.Font(None, 16)
        self.block_size = PUZZLE_SIZE // SIZE

        # Initialize window
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((PUZZLE_SIZE+2*MARGINS, PUZZLE_SIZE+2*MARGINS))
        self.screen.fill(WHITE)
        self.draw_grid(puzzle)
        pygame.display.flip()

    def run(self, duration=DURATION):
        start_time = time.time()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = False
            if time.time() - start_time > duration:
                running = False
            pygame.display.flip()

    def draw_grid(self, puzzle):
        for x in range(0, PUZZLE_SIZE+1, self.block_size):
            line_width = 3 if x % (self.block_size * 3) == 0 else 1
            
            pygame.draw.line(self.screen, BLACK, (x+MARGINS, MARGINS), (x+MARGINS, PUZZLE_SIZE+MARGINS), line_width)
            pygame.draw.line(self.screen, BLACK, (MARGINS, x+MARGINS), (PUZZLE_SIZE+MARGINS, x+MARGINS), line_width)

        for r in range(SIZE):
            for c in range(SIZE):
                if puzzle[r][c] != None:
                    text = self.font.render(str(puzzle[r][c]), True, BLACK)
                    text_x = MARGINS + c * self.block_size + (self.block_size - text.get_width()) // 2
                    text_y = MARGINS + r * self.block_size + (self.block_size - text.get_height()) // 2
                    self.screen.blit(text, (text_x, text_y))

    def draw_markup_grid(self, puzzle, markup):
        for r in range(SIZE):
            for c in range(SIZE):
                if markup[r][c] != None:  
                    self.draw_markup_cell(r, c, markup[r][c])      

    def draw_markup_cell(self, row, col, cell_markup, duration=DURATION):
        self.show_number(row, col, "", duration)

        text_rows = math.ceil(len(cell_markup) / 3)
        for text_row in range(text_rows):
            markup_string = ', '.join(map(str, list(cell_markup)[3*text_row:3*(text_row+1)]))
            text = self.markup_font.render(markup_string, True, BLACK)
            text_x = MARGINS + col * self.block_size + 2
            text_y = MARGINS + row * self.block_size + 2 + self.block_size // 3 * text_row
            self.screen.blit(text, (text_x, text_y))

        self.run(duration)

    def show_number(self, row, col, number, duration=DURATION):
        self.screen.fill(LIGHT_BLUE, rect=[MARGINS + col * self.block_size + 2, MARGINS + row * self.block_size + 2, self.block_size - 4, self.block_size - 4])
        text = self.font.render(str(number), True, DARK_BLUE)
        text_x = MARGINS + col * self.block_size + (self.block_size - text.get_width()) // 2
        text_y = MARGINS + row * self.block_size + (self.block_size - text.get_height()) // 2
        self.screen.blit(text, (text_x, text_y))
        self.run(duration)
        self.erase_number(row, col)

    def add_number(self, row, col, number, certain=False):
        if certain:
            self.screen.fill(LIGHT_GREEN, rect=[MARGINS + col * self.block_size + 2, MARGINS + row * self.block_size + 2, self.block_size  - 4, self.block_size - 4])
        else:
            self.screen.fill(LIGHT_YELLOW, rect=[MARGINS + col * self.block_size + 2, MARGINS + row * self.block_size + 2, self.block_size  - 4, self.block_size - 4])
        if number != 0:
            text = self.font.render(str(number), True, DARK_BLUE)
            text_x = MARGINS + col * self.block_size + (self.block_size - text.get_width()) // 2
            text_y = MARGINS + row * self.block_size + (self.block_size - text.get_height()) // 2
            self.screen.blit(text, (text_x, text_y))
       
    def erase_number(self, row, col):
        self.screen.fill(WHITE, rect=[MARGINS + col * self.block_size + 2, MARGINS + row * self.block_size + 2, self.block_size - 4, self.block_size - 4])

    def display_correct_solution(self, cells_to_solve, puzzle, duration=DURATION):
        self.draw_grid(puzzle)
        for cell in cells_to_solve:
            self.add_number(cell[0], cell[1], puzzle[cell[0]][cell[1]], certain=True)
        
        pygame.display.set_caption('Sudoku solved!')
        self.run(duration)

def main():
    puzzle = [[None, 1, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, 9, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None],
              [None, None, None, None, None, None, None, None, None]]

    sudoku = GUI(puzzle, "Sudoku")
    markup = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    sudoku.run(0.5)
    sudoku.draw_markup_cell(0, 0, markup, 1)

if __name__ == '__main__':
    main()