import pygame, sys
from constants import *
import numpy as np
import random
import copy

pygame.init()
WIDTH = 600
HEIGHT = 600
ROWS = 3
COLS = 3
SQSIZE = WIDTH // COLS
BG_COLOR= (255,255,255)
LINE_COLOR= (0, 128, 128)
CIRC_COLOR = (113,198,113)
CROSS_COLOR = (46,139,87)
LINE_WIDTH = 15
CIRC_WIDTH = 18
CROSS_WIDTH = 20
OFFSET = 50
RADIUS = SQSIZE // 4
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TESTCREATESALOME')
screen.fill( BG_COLOR )

class Board:
    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0
        
    def final_state(self):
        
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
            
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]
            
        if self.squares[0][0] == self.squares[1][1] == self.squares [2][2] != 0:
            return self.squares[1][1]
        
        if self.squares[2][0] == self.squares[1][1] == self.squares [0][2] != 0:
            return self.squares[1][1]
        
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
                if self.empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        return empty_sqrs
    
    def isfull(self):
        return self.marked_sqrs == 9
    
    def isfull(self):
        return self.marked_sqrs == 0

class AI:
    def __init__(self, level = 1, player=2):
        self.level = level
        self.player = player
    
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[idx]
    
    def minimax(self, board, maximizing):
        case = board.final_state()
        if case == 1:
            return 1, None
        if case == 2:
            return -1, None
        elif board.isfull():
            return 0, None
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()
            
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move
    
            
        elif not maximizing:
            min_eval =100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()
            
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move
    
    def eval(self, main_board):
        if self.level == 0:
            eval = 'random'
            move = self.rnd(main_board)
        else:
            eval, move = self.minimax(main_board, False)
        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        return move
            
        
class Game:
    def __init__(self):
        self.board= Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai'
        self.running = True
        self.show_lines()
        
    
    def show_lines(self):
        #vertical
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        #horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, WIDTH - SQSIZE,), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)
        
    def draw_fig(self, row, col):
     if self.player == 1:
        start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
        end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
        pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
        
        start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
        end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
        pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

     elif self.player == 2:
        center = ( col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2 )
        pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)
   
     
            
    def next_turn(self):
        self.player = self.player % 2 + 1
        
def main():
    game = Game()
    board = game.board
    ai = game.ai
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                if board.empty_sqr(row, col):
                    board.mark_sqr(row, col, game.player)
                    game.draw_fig(row, col)
                    game.next_turn()
         
        if game.gamemode == 'ai' and game.player == ai.player:
            pygame.display.update()
            
            row, col = ai.eval(board)
            board.mark_sqr(row, col, game.player)
            game.draw_fig(row, col)
            game.next_turn()
               
        pygame.display.update()
                
main()
    