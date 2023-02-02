import sys
import pygame
import numpy as np

from constants import *

#PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)

class Board:

    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares # [squares]
        self.marked_sqrs = 0

    def final_state(self):
        '''
            @return 0 if there is not win yet
            @return 1 if player 1 wins
            @retunr 2 if player 2 wins
        '''

        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]

        # descending diagonal win
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]

        # ascending diagonal win
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]

        # no win yet
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqrs(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs

    def isFull(self):
        return self.marked_sqrs == 9

    def isEmpty(self):
        return self.marked_sqrs == 0

class Game:

    def __init__(self):
        self.board = Board()
        #self.ai = AI()
        self.player = 1 # 1-cross # 2-circles
        self.gamemode = 'pvp' # pvp or AI
        self.running = True
        self.show_lines()

    def show_lines(self):
        # vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQUARE_SIZE, 0), (WIDTH - SQUARE_SIZE, HEIGHT), LINE_WIDTH)

        # horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQUARE_SIZE), (WIDTH, HEIGHT - SQUARE_SIZE), LINE_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1

    def draw_fig(self, row, col):
        if self.player == 1:
            #draw cross
            # descending line
            start_desc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET)
            end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            # ascending line
            start_asc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            # draw circle
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

def main():

    # game object
    game = Game()
    board = game.board

    # mainloop
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE

                if board.empty_sqr(row, col):
                    board.mark_sqr(row, col, game.player)
                    game.draw_fig(row, col)
                    game.next_turn()

        pygame.display.update()

main()
