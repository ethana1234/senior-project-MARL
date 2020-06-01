import numpy as np
import gym
from gym import spaces

BOARD_ROWS,BOARD_COLS = 6,7
TOTAL_BOARD_SPACES = BOARD_ROWS*BOARD_COLS
COORD_TO_INDEX = lambda x : (x[0] * BOARD_ROWS) + x[1]


class Connect4Env(gym.Env):
    '''Class that implements the Gym Environment Interface'''
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
        '''Get a unique hash value that corresponds with the current board state
        This is used to store the board state in a state-value dictionary'''
        return str(self.board.reshape(BOARD_ROWS * BOARD_COLS))

    def find_runs(self, x):
        """Find runs of consecutive items in an array.
        Credit to Github user alimanfoo for this function"""

        # ensure array
        x = np.asanyarray(x)
        if x.ndim != 1:
            raise ValueError('only 1D array supported')
        n = x.shape[0]

        # handle empty array
        if n == 0:
            return np.array([]), np.array([]), np.array([])

        else:
            # find run starts
            loc_run_start = np.empty(n, dtype=bool)
            loc_run_start[0] = True
            np.not_equal(x[:-1], x[1:], out=loc_run_start[1:])
            run_starts = np.nonzero(loc_run_start)[0]

            # find run values
            run_values = x[loc_run_start]

            # find run lengths
            run_lengths = np.diff(np.append(run_starts, n))

            # Now find if a winner exists
            for ind,val in enumerate(run_values):
                if val == 1 and run_lengths[ind] >= 4:
                    return (1,0)
                elif val == -1 and run_lengths[ind] >= 4:
                    return (0,1)

            return None
        
    def winner(self, row, col):
        '''After each move, check if there's a winner and give out rewards'''
        row_win = self.find_runs(self.board[row,:])
        if row_win is not None:
            return row_win

        col_win = self.find_runs(self.board[:,col])
        if col_win is not None:
            return col_win

        diag_win = self.find_runs(self.board.diagonal(offset=row-col+3))
        if diag_win is not None:
            return diag_win
        diag_win = self.find_runs(np.fliplr(self.board).diagonal(offset=row+col-4))
        if diag_win is not None:
            return diag_win
                    
        
        # Tie
        if not len(self.availablePositions()):
            return (0.1, 0.5)
        
        # Game not over
        return None
