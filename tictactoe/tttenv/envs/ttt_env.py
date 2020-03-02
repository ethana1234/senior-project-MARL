import numpy as np
import gym
from gym import spaces

BOARD_ROWS,BOARD_COLS = 3,3
TOTAL_BOARD_SPACES = BOARD_ROWS*BOARD_COLS
COORD_TO_INDEX = lambda x : (x[0] * BOARD_ROWS) + x[1]


# Class that implements the Gym Environment Interface
class TicTacToeEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        super(TicTacToeEnv, self).__init__()
        
        # Board is always 3x3 for tic tac toe
        self.action_space = spaces.Discrete(TOTAL_BOARD_SPACES)
        self.observation_space = spaces.Discrete(TOTAL_BOARD_SPACES)
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.gameOver = False
        self.playerTurn = 0
    
    def reset(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.gameOver = False
        self.playerTurn = 0
        
    def step(self, action):
        self.board[action[0],action[1]] = self.playerTurn
        reward = self.winner()
        if reward is not None:
            self.gameOver = True
        # Switch to other player
        self.playerTurn = 0 if self.playerTurn == 1 else 1
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
    def winner(self):
        # Row win
        for i in range(BOARD_ROWS):
            # p1 wins
            if sum(self.board[i, :]) == 3:
                self.gameOver = True
                return (1, 0)
            # p2 wins
            elif sum(self.board[i, :]) == -3:
                self.gameOver = True
                return (0, 1)
            
        # Column win 
        for i in range(BOARD_COLS):
            if sum(self.board[:, i]) == 3:
                self.gameOver = True
                return (1, 0)
            elif sum(self.board[:, i]) == -3:
                self.gameOver = True
                return (0, 1)
            
        # Diagonal win
        diag1 = sum([self.board[i, i] for i in range(BOARD_COLS)])
        diag2 = sum([self.board[i, BOARD_COLS - i - 1] for i in range(BOARD_COLS)])
        if diag1 == 3 or diag2 == 3:
            self.gameOver = True
            return (1, 0)
        elif diag1 == -3 or diag2 == -3:
            self.gameOver = True
            return (0, 1)
        
        # Tie
        if not len(self.availablePositions()):
            self.gameOver = True
            return (0.1, 0.5)
        
        # Game not over
        self.gameOver = False
        return None
    
    