import numpy as np
import gym
from gym import spaces

BOARD_ROWS,BOARD_COLS = 6,7
TOTAL_BOARD_SPACES = BOARD_ROWS*BOARD_COLS
COORD_TO_INDEX = lambda x : (x[0] * BOARD_ROWS) + x[1]


# Class that implements the Gym Environment Interface
class Connect4Env(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        super(Connect4Env, self).__init__()
        
        # Board is always 6x7 for connect4
        self.action_space = spaces.Discrete(TOTAL_BOARD_SPACES)
        self.observation_space = spaces.Discrete(TOTAL_BOARD_SPACES)
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.gameOver = False
        self.playerTurn = 1
        self.curRows = {curRow: BOARD_ROWS for curRow in range(BOARD_COLS)}
    
    def reset(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.gameOver = False
        self.playerTurn = 1
        
    def step(self, action):
        row,col = action[0],action[1]
        self.board[row,col] = self.playerTurn
        self.curRows[col] -= 1
        reward = self.winner(row,col)
        if reward is not None:
            self.gameOver = True
        # Switch to other player
        self.playerTurn = -1 if self.playerTurn == 1 else 1
        return self.board, reward, self.gameOver, self.getHash()
    
    def render(self):
        # p1: x  p2: o
        for i in range(0, BOARD_ROWS):
            print('-------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')
        
    # Update vacant positions after a turn is made
    def availablePositions(self):
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i,j] == 0:
                    # Coordinates need to be in tuple form
                    positions.append((i,j))
        return positions
        
    # Get a unique hash value that corresponds with the current board state
    # This is used to store the board state in a state-value dictionary
    def getHash(self):
        return str(self.board.reshape(BOARD_ROWS * BOARD_COLS))
        
    # After each move, check if there's a winner and give out rewards
    def winner(self, row, column):
        # Col win
        # p1 wins
        if sum(self.board[row:min(BOARD_COLS,row+4),column]) == 4:
            return (1, 0)
        # p2 wins
        elif sum(self.board[row:min(BOARD_COLS,row+4), column]) == -4:
            return (0, 1)

        for i in range(4):
        # Row win 
            if sum(self.board[row, max(0,column-i):min(BOARD_ROWS,column+4-i)]) == 4:
                return (1, 0)
            elif sum(self.board[row, max(0,column-i):min(BOARD_ROWS, column+4-i)]) == -4:
                return (0, 1)

        diag = self.board.diagonal(offset = column-row)

        if len(diag) >= 4:
            for i in range(len(diag)-3):
                if sum(diag[i:i+4]) == 4:
                    return (1, 0)
                if sum(diag[i:i+4]) == -4:
                    return (0, 1)
                if sum(diag[i-4:i]) == 4:
                    return (1, 0)
                if sum(diag[i-4:i]) == -4:
                    return (0, 1)

#TODO
#failure example test case
#a=np.array([0,0,0,0,0,0,0]*6)
#a[4][0]=1
#a[3][1]=1
#a[2][2]=1
#a[1][3]=1
#winner(a, 4,0)

        diag2 = np.fliplr(self.board).diagonal(offset = row-column)
        if len(diag2) >= 4:
            for i in range(len(diag2)-3):
                if sum(diag2[i:i+4]) == 4:
                    return (1, 0)
                if sum(diag2[i:i+4]) == -4:
                    return (0, 1)
                if sum(diag2[i-4:i]) == 4:
                    return (1, 0)
                if sum(diag2[i-4:i]) == -4:
                    return (0, 1)
                    
        
        # Tie
        if not len(self.availablePositions()):
            self.gameOver = True
            return (0.1, 0.5)
        
        # Game not over
        return None
    
