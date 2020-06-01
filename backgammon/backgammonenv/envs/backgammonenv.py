import numpy as np
import gym
from gym import spaces

TOT_BOARD_PTS = 24
P1 = 0
P2 = 1
ALL_CHECKERS = 15

class BackgammonEnv(gym.Env):
    '''Class that implements the Gym Environment Interface'''
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        super(BackgammonEnv, self).__init__()
        
        self.action_space = spaces.Discrete(TOT_BOARD_PTS)
        self.observation_space = spaces.Discrete(TOT_BOARD_PTS)
        self.homePts = {P1: [i for i in range(18,24)], P2: [i for i in range(6)]}
        self.board = np.array([(0, None)] * TOT_BOARD_PTS)
        self.board[0] = (2, P1)
        self.board[11] = (5, P1)
        self.board[16] = (3, P1)
        self.board[18] = (5, P1)
        self.board[5] = (5, P2)
        self.board[7] = (3, P2)
        self.board[12] = (5, P2)
        self.board[23] = (2, P2)
        self.out = [0,0]
        self.gameOver = False
        self.homePts = { P2: [18,19,20,21,22,23], P1: [0,1,2,3,4,5] }
        self.playerTurn = P1
        self.roll = (np.random.randint(1,7), np.random.randint(1,7))
    
    def reset(self):
        self.board = np.array([(0, None)] * TOT_BOARD_PTS)
        self.board[0] = (2, P1)
        self.board[11] = (5, P1)
        self.board[16] = (3, P1)
        self.board[18] = (5, P1)
        self.board[5] = (5, P2)
        self.board[7] = (3, P2)
        self.board[12] = (5, P2)
        self.board[23] = (2, P2)
        self.out = [0,0]
        self.gameOver = False
        self.playerTurn = P1
        self.roll = (np.random.randint(1,7), np.random.randint(1,7))
        
    def step(self, action):
        reward = self.winner(action)
        if reward is not None:
            self.gameOver = True
        self.playerTurn = P2 if self.playerTurn == P1 else P1
        return self.board, reward, self.gameOver, self.getHash()
    
    def render(self):
        print(self.board)
        

    def bearOff(self, board):
        tot = sum(np.array([self.board[position][0] for position in self.homePts[self.playerTurn] if self.playerTurn == self.board[position][1]]))
        return tot == (ALL_CHECKERS - self.out[self.playerTurn])

'''
    def bearOffOneRoll(self, roll):
        # use one roll to move the only checkers outside home board to home board, bear off with other roll(s)
        tot = sum(np.array([self.board[position][0] for position in self.homePts[self.playerTurn] if self.playerTurn == self.board[position][1]]))
        threshold = ALL_CHECKERS - (len(roll)-1)
        return tot >= (threshold - self.out[self.playerTurn])

    def canMoveTo(self, target):
        if target < 0 or target > 23:
            return self.bearOff()
        return self.board[target][0] < 2 or (self.board[target][0] > 1 and self.board[target][1] == self.playerTurn)

    def isValid(self, target):
        if 0 <= target < TOT_BOARD_PTS:
            return self.board[target][0] < 2 or (self.board[target][0] > 1 and self.board[target][1] == self.playerTurn)
        return False
'''

    def availablePositions(self, board, roll):
        opponent = 1 - self.playerTurn
        possibleMoves = np.array([])
        for i in range(TOT_BOARD_PTS):
            if board[i][0] > 0 and board[i][1] == self.playerTurn:
                target = roll + i
                if target < 0 or target > 23:
                    return self.bearOff(board)
                if board[target][0] < 2 or self.board[target][1] != opponent:
                    #validMove
                    possibleMoves.append((i,target))
        return possibleMoves

        
    def getHash(self):
        '''Get a unique hash value that corresponds with the current board state
        This is used to store the board state in a state-value dictionary'''
        return str(self.board.reshape(TOT_BOARD_PTS))
        
    def winner(self):
        '''After each move, check if there's a winner and give out rewards'''
        if self.board[P1_HOME][P1_CHECKERS] == ALL_CHECKERS return (1,0)
        if self.board[P2_HOME][P2_CHECKERS] == ALL_CHECKERS return (0,1)
        # Game not over
        return None
