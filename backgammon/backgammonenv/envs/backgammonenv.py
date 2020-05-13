import numpy as np
import gym
from gym import spaces

TOTAL_BOARD_PTS = 26 #first and last are home (end states)
P1_HOME = 0
P2_HOME = 25
P1_CHECKERS = 0
P2_CHECKERS = 1
ALL_CHECKERS = 15


class BackgammonEnv(gym.Env):
    '''Class that implements the Gym Environment Interface'''
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        super(BackgammonEnv, self).__init__()
        
        self.action_space = spaces.Discrete(TOTAL_BOARD_PTS)
        self.observation_space = spaces.Discrete(TOTAL_BOARD_PTS)
        self.board = np.array([ [0,0],
                                [0,2], [0,0], [0,0], [0,0], [0,0], [5,0],
                                [0,0], [3,0], [0,0], [0,0], [0,0], [0,5],
                                [5,0], [0,0], [0,0], [0,0], [0,3], [0,0],
                                [0,5], [0,0], [0,0], [0,0], [0,0], [2,0],
                                [0,0]] )
        self.gameOver = False
        self.playerTurn = 0
        self.roll = (np.random.randint(1,7), np.random.randint(1,7))
    
    def reset(self):
        self.board = np.array([ [0,0],
                                [0,2], [0,0], [0,0], [0,0], [0,0], [5,0],
                                [0,0], [3,0], [0,0], [0,0], [0,0], [0,5],
                                [5,0], [0,0], [0,0], [0,0], [0,3], [0,0],
                                [0,5], [0,0], [0,0], [0,0], [0,0], [2,0],
                                [0,0]] )
        self.gameOver = False
        self.playerTurn = 0
        self.roll = (np.random.randint(1,7), np.random.randint(1,7))
        
    def step(self, action):
        reward = self.winner(action)
        if reward is not None:
            self.gameOver = True
        self.playerTurn = 1 if self.playerTurn == 0 else 0
        return self.board, reward, self.gameOver, self.getHash()
    
    def render(self):
        print(self.board)
   '''     
   to be done outside of env
    def useRoll(self, roll):
        possibleMoves = np.array([])
        opponent = 1 - self.playerTurn
        for i in range(1, TOTAL_BOARD_PTS - 1):
            if board[i][self.playerTurn] > 0:
                if board[roll+i][opponent] < 2:
                    #validMove
                    move1 = (i,roll+i)
                    #find any possible next moves
                    for i in range (1, TOTAL_BOARD_PTS - 1):

        
    def getValidMoves(self):
        '''roll and get valid moves from board'''
        self.roll = (np.random.randint(1,7), np.random.randint(1,7))
        move1 = useRoll(self.roll[0])
        move2 = useRoll(self.roll[1])
        if self.roll[0]==self.roll[1]
            move3 = useRoll(self.roll[0])
            move4 = useRoll(self.roll[1])
'''

        
    def getHash(self):
        '''Get a unique hash value that corresponds with the current board state
        This is used to store the board state in a state-value dictionary'''
        return str(self.board.reshape(TOTAL_BOARD_PTS))
        
    def winner(self):
        '''After each move, check if there's a winner and give out rewards'''
        if self.board[P1_HOME][P1_CHECKERS] == ALL_CHECKERS return (1,0)
        if self.board[P2_HOME][P2_CHECKERS] == ALL_CHECKERS return (0,1)
        # Game not over
        return None
