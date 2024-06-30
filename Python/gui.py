import pygame
import math
import time

SIZE = 9
SCREEN_SIZE = 450
DURATION = 0.02
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 139)
LIGHT_BLUE = (173, 216, 230)

class GUI():
    def __init__(self, puzzle, title):
        pygame.init()
        self.font = pygame.font.Font(None, 36)
        self.markup_font = pygame.font.Font(None, 18)
        self.block_size = SCREEN_SIZE // SIZE

        # Initialize window
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
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
        for x in range(0, SCREEN_SIZE, self.block_size):
            line_width = 3 if x % (self.block_size * 3) == 0 else 1
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, SCREEN_SIZE), line_width)
            pygame.draw.line(self.screen, BLACK, (0, x), (SCREEN_SIZE, x), line_width)

        for r in range(SIZE):
            for c in range(SIZE):
                if puzzle[r][c] != 0:  
                    text = self.font.render(str(puzzle[r][c]), True, BLACK)
                    text_x = c * self.block_size + (self.block_size - text.get_width()) // 2
                    text_y = r * self.block_size + (self.block_size - text.get_height()) // 2
                    self.screen.blit(text, (text_x, text_y))

    def draw_markup_grid(self, puzzle, sudoku_markup):
        for r in range(SIZE):
            for c in range(SIZE):
                if puzzle[r][c] == 0:  
                    self.draw_markup_cell(r, c, sudoku_markup[r][c])      

    def draw_markup_cell(self, row, col, markup, duration=DURATION):
        self.show_number(row, col, "", duration)

        text_rows = math.ceil(len(markup) / 3)
        for text_row in range(text_rows):
            markup_string = ', '.join(map(str, list(markup)[3*text_row:3*(text_row+1)]))
            text = self.markup_font.render(markup_string, True, BLACK)
            text_x = col * self.block_size + 2
            text_y = row * self.block_size + 2 + self.block_size // 3 * text_row
            self.screen.blit(text, (text_x, text_y))

        self.run(duration)

    def show_number(self, row, col, number, duration=DURATION):
        self.screen.fill(LIGHT_BLUE, rect=[col * self.block_size + 2, row * self.block_size + 2, self.block_size  - 4, self.block_size - 4])
        text = self.font.render(str(number), True, DARK_BLUE)
        text_x = col * self.block_size + (self.block_size - text.get_width()) // 2
        text_y = row * self.block_size + (self.block_size - text.get_height()) // 2
        self.screen.blit(text, (text_x, text_y))
        self.run(duration)
        self.erase_number(row, col)

    def add_number(self, row, col, number):
        text = self.font.render(str(number), True, DARK_BLUE)
        text_x = col * self.block_size + (self.block_size - text.get_width()) // 2
        text_y = row * self.block_size + (self.block_size - text.get_height()) // 2
        self.screen.blit(text, (text_x, text_y))
       
    def erase_number(self, row, col):
        self.screen.fill(WHITE, rect=[col * self.block_size + 2, row * self.block_size + 2, self.block_size  - 4, self.block_size - 4])

def main():
    puzzle = [[0, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 9, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    sudoku = GUI(puzzle, "Sudoku")
    markup = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    sudoku.run(0.5)
    sudoku.draw_markup_cell(0, 0, markup, 1)

if __name__ == '__main__':
    main()