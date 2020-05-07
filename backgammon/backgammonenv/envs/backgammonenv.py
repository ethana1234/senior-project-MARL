import numpy as np
import gym
from gym import spaces


class BackgammonEnv(gym.Env):
    '''Class that implements the Gym Environment Interface'''
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        super(BackgammonEnv, self).__init__()
        
        self.action_space = spaces.Discrete(TOTAL_BOARD_SPACES)
        self.observation_space = spaces.Discrete(TOTAL_BOARD_SPACES)
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.gameOver = False
        self.playerTurn = 1
    
    def reset(self):
        pass
        
    def step(self, action):
        pass
    
    def render(self):
        pass
        
    def availablePositions(self):
        '''Update vacant positions after a turn is made'''
        pass
        
    def getHash(self):
        '''Get a unique hash value that corresponds with the current board state
        This is used to store the board state in a state-value dictionary'''
        pass

        
    def winner(self, row, col):
        '''After each move, check if there's a winner and give out rewards'''
        
                    
        
        # Tie
        if not len(self.availablePositions()):
            return (0.1, 0.5)
        
        # Game not over
        return None