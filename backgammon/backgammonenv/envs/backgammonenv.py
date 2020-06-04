import numpy as np
import gym
from gym import spaces

TOT_BOARD_PTS = 24
WHITE,BLACK = 0,1
ALL_CHECKERS = 15
WHITE_HOME,BLACK_HOME,BAR_IND = 25,26,0 # for self.board array

class BackgammonEnv(gym.Env):
    '''Class that implements the Gym Environment Interface'''
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        super(BackgammonEnv, self).__init__()
        
        self.action_space = spaces.Discrete(TOT_BOARD_PTS)
        self.observation_space = spaces.Discrete(TOT_BOARD_PTS)
        self.homePts = {WHITE: [i for i in range(18,24)], BLACK: [i for i in range(6)]}
        self.board = np.array([[0, None]] * TOT_BOARD_PTS + 3) # add 3 extra locations for homes and bar
        self.board[1] = [2, WHITE]
        self.board[12] = [5, WHITE]
        self.board[17] = [3, WHITE]
        self.board[19] = [5, WHITE]
        self.board[6] = [5, BLACK]
        self.board[8] = [3, BLACK]
        self.board[13] = [5, BLACK]
        self.board[24] = [2, BLACK]
        self.board[BAR_IND] = [0,0]
        self.board[WHITE_HOME] = 0
        self.board[BLACK_HOME] = 0
        self.gameOver = False
        self.homePts = { BLACK: [18,19,20,21,22,23], WHITE: [0,1,2,3,4,5] }
        self.playerTurn = WHITE
        self.roll = (np.random.randint(1,7), np.random.randint(1,7))
    
    def reset(self):
        self.board = np.array([[0, None]] * TOT_BOARD_PTS + 3)
        self.board[1] = [2, WHITE]
        self.board[12] = [5, WHITE]
        self.board[17] = [3, WHITE]
        self.board[19] = [5, WHITE]
        self.board[6] = [5, BLACK]
        self.board[8] = [3, BLACK]
        self.board[13] = [5, BLACK]
        self.board[24] = [2, BLACK]
        self.board[0] = [0,0]
        self.board[WHITE_HOME] = 0
        self.board[BLACK_HOME] = 0
        self.gameOver = False
        self.playerTurn = WHITE
        self.roll = (np.random.randint(1,7), np.random.randint(1,7))
        
    def step(self, action):
        # Action in this case is a checker to move, and the location to move it to
        move_from,move_to = action
        if move_to == BLACK_HOME or move_to == WHITE_HOME:
            # Sending a checker home
            self.board[move_from][0] -= 1
            self.board[move_to] += 1
        else:
            if self.board[move_to][1] is not None:
                # Remove other player's checker to bar first
                self.board[BAR_IND][WHITE if self.playerTurn == BLACK else WHITE] += 1
                self.board[move_to][0] = 0
            if move_from == 0:
                # Moving from bar case
                self.board[BAR_IND][self.playerTurn] -= 1
            else:
                self.board[move_from][0] -= 1
            self.board[move_to][0] += 1
            self.board[move_to][1] = self.playerTurn
        reward = self.winner()
        if reward is not None:
            self.gameOver = True
        self.playerTurn = BLACK if self.playerTurn == WHITE else WHITE
        return self.board, reward, self.gameOver, self.getHash()
    
    def render(self):
        print(self.board)
        
    def getValidMoves(self):
        '''roll and get valid moves from board'''
        
        possibleMoves = np.array([])
        self.roll = (np.random.randint(1,7), np.random.randint(1,7))
        move1 = useRoll(self.roll[0]) #this is an array of possible from/to moves for roll 0
        move2 = useRoll(self.roll[1]) #array of possible from/to moves for roll 1
        moveComb = useRoll(self.roll[0] + self.roll[1]) #array of possible from/to moves using both rolls at once
        if self.roll[0]==self.roll[1]:
            move3 = useRoll(self.roll[0])
            move4 = useRoll(self.roll[1])
            possibleMoves.append(np.array([move1,move2,move3,move4]))
        else:
            possibleMoves.append(np.array([move1,move2]))
        return possibleMoves


    def bearOff(self):
        tot = sum(np.array([self.board[position][0] for position in self.homePts[self.playerTurn] if self.playerTurn == self.board[position][1]]))
        return tot == (ALL_CHECKERS - self.out[self.playerTurn])

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

    def useRoll(self, roll):
        opponent = 1 - self.playerTurn
        possibleMove = np.array([])
        for i in range(TOT_BOARD_PTS):
            if board[i][0] > 0 and board[i][1] == self.playerTurn:
                target = roll + i
                if target < 0 or target > 23:
                    return self.bearOff()
                if board[target][0] < 2 or self.board[target][1] != opponent:
                    #validMove
                    possibleMove.append((i,target))
        return possibleMove

        
    def getHash(self):
        '''Get a unique hash value that corresponds with the current board state
        This is used to store the board state in a state-value dictionary'''
        return str(self.board.reshape(TOT_BOARD_PTS))
        
    def winner(self):
        '''After each move, check if there's a winner and give out rewards'''
        if self.board[WHITE_HOME][WHITE_CHECKERS] == ALL_CHECKERS:
            return (1,0)
        if self.board[BLACK_HOME][BLACK_CHECKERS] == ALL_CHECKERS:
            return (0,1)
        # Game not over
        return None
