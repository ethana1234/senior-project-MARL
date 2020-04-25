import numpy as np
import gym
from gym import spaces

BOARD_ROWS,BOARD_COLS = 3,3
TOTAL_BOARD_SPACES = BOARD_ROWS*BOARD_COLS
COORD_TO_INDEX = lambda x : (x[0] * BOARD_ROWS) + x[1]


# Class that implements the Gym Environment Interface
class TicTacToeEnv(gym.Env):
    '''Class that implements the Gym Environment Interface'''
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        super(TicTacToeEnv, self).__init__()
        
        # Board is always 3x3 for tic tac toe
        self.action_space = spaces.Discrete(TOTAL_BOARD_SPACES)
        self.observation_space = spaces.Discrete(TOTAL_BOARD_SPACES)
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.gameOver = False
        self.playerTurn = 1
    
    def reset(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.gameOver = False
        self.playerTurn = 1
        
    def step(self, action):
        self.board[action[0],action[1]] = self.playerTurn
        reward = self.winner()
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
        
    def availablePositions(self):
        '''Update vacant positions after a turn is made'''
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i,j] == 0:
                    # Coordinates need to be in tuple form
                    positions.append((i,j))
        return positions
        
    def getHash(self):
        '''Get a unique hash value that corresponds with the current board state.
        This is used to store the board state in a state-value dictionary'''
        return str(self.board.reshape(BOARD_ROWS * BOARD_COLS))
        
    def winner(self):
        ''' After each move, check if there's a winner and give out rewards'''
        # Player 1 win
        mask = (self.board == 1)
        if mask.all(0).any() or mask.all(1).any() or mask.diagonal().all() or np.fliplr(mask).diagonal().all():
            return (1,0)

        # Player 2 win
        mask = (self.board == -1)
        if mask.all(0).any() or mask.all(1).any() or mask.diagonal().all() or np.fliplr(mask).diagonal().all():
            return (0,1)

        # Tie
        if not len(self.availablePositions()):
            self.gameOver = True
            return (0.1, 0.5)
        
        # Game not over
        self.gameOver = False
        return None
