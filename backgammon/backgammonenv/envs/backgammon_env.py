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
        self.board = np.array([[0, None]] * (TOT_BOARD_PTS + 3)) # add location for bar and homes
        self.board[1] = [2, WHITE]
        self.board[12] = [5, WHITE]
        self.board[17] = [3, WHITE]
        self.board[19] = [5, WHITE]
        self.board[6] = [5, BLACK]
        self.board[8] = [3, BLACK]
        self.board[13] = [5, BLACK]
        self.board[24] = [2, BLACK]
        self.board[BAR_IND] = [0,0]
        self.gameOver = False
        self.homePts = { BLACK: [18,19,20,21,22,23], WHITE: [0,1,2,3,4,5] }
        self.playerTurn = None
    
    def reset(self):
        self.board = np.array([[0, None]] * (TOT_BOARD_PTS + 3))
        self.board[1] = [2, WHITE]
        self.board[12] = [5, WHITE]
        self.board[17] = [3, WHITE]
        self.board[19] = [5, WHITE]
        self.board[6] = [5, BLACK]
        self.board[8] = [3, BLACK]
        self.board[13] = [5, BLACK]
        self.board[24] = [2, BLACK]
        self.board[BAR_IND] = [0,0]
        self.gameOver = False
        self.playerTurn = None
        
    def step(self, action):
        self.board = self.updateBoard(action,self.board)
        reward = self.winner()
        if reward is not None:
            self.gameOver = True
        return reward, self.gameOver, self.getHash()

    def updateBoard(self, action, board):
        '''Given a move, update board. This function can be used to update the actual or by QAgentPlayer that's attempting to choose an action'''
        # Action in this case is a checker to move, and the location to move it to
        move_from_i,move_to_i = action # indices of board
        move_from,move_to = board[move_from_i],board[move_to_i] # actual location objects
        if move_to_i == BLACK_HOME or move_to_i == WHITE_HOME:
            # Sending a checker home
            move_from[0] -= 1
        else:
            if move_to[1] is not None and move_to[1] != self.playerTurn:
                # Remove other player's checker to bar first
                board[BAR_IND][WHITE if self.playerTurn == BLACK else WHITE] += 1
                move_to[0] = 0
            if move_from_i == 0:
                # Moving from bar case
                board[BAR_IND][self.playerTurn] -= 1
            else:
                move_from[0] -= 1
        if move_from_i != 0 and move_from[0] == 0:
            # if leaving a board spot makes the spot empty
            move_from[1] = None
        else:
            move_to[1] = self.playerTurn
        move_to[0] += 1
        return board
    
    def render(self):
        board_string = []
        # Find max checker stack
        maxlen = 0
        for spot in self.board[BAR_IND + 1:WHITE_HOME]:
            maxlen = spot[0] if spot[0] > maxlen else maxlen
        # Left side of board
        for t,b in zip(range(13,19),range(12,6,-1)):
            top,bottom = self.board[t],self.board[b]
            board_column = [f'{t:2}','--']
            checker = 'B' if top[1] == BLACK else 'W'
            board_column += [f'{checker} ' for i in range(top[0])]
            board_column += [f'  ' for i in range(maxlen - top[0])]
            board_column.append(f'--')
            checker = 'B' if bottom[1] == BLACK else 'W'
            board_column += [f'  ' for i in range(maxlen - bottom[0])]
            board_column += [f'{checker} ' for i in range(bottom[0])]
            board_column += ['--',f'{b:2}']
            board_string.append(np.array(board_column))
        # Bar
        bar_string = ['   ','---'] + ['   ' for i in range(maxlen*2+1)] + ['---','   ']
        for i in range(self.board[BAR_IND][0]):
            bar_string[-(i+3)] = ' W '
        for i in range(self.board[BAR_IND][1]):
            bar_string[i+2] = ' B '
        board_string.append(np.array(bar_string))
        # Right side of board
        for t,b in zip(range(19,25),range(6,0,-1)):
            top,bottom = self.board[t],self.board[b]
            board_column = [f'{t:2}','--']
            checker = 'B' if top[1] == BLACK else 'W'
            board_column += [f'{checker} ' for i in range(top[0])]
            board_column += [f'  ' for i in range(maxlen - top[0])]
            board_column.append(f'--')
            checker = 'B' if bottom[1] == BLACK else 'W'
            board_column += [f'  ' for i in range(maxlen - bottom[0])]
            board_column += [f'{checker} ' for i in range(bottom[0])]
            board_column += ['--',f'{b:2}']
            board_string.append(np.array(board_column))
        # Joining columns together
        board_string = np.stack(board_string).T
        print('\n'.join('|'.join(x for x in row) for row in board_string))

    def getHash(self):
        '''Get a unique hash value that corresponds with the current board state
        This is used to store the board state in a state-value dictionary'''
        return str(self.board.reshape(2 * (TOT_BOARD_PTS + 3)))
        
    def winner(self):
        '''After each move, check if there's a winner and give out rewards'''
        if self.board[WHITE_HOME][0] == ALL_CHECKERS:
            return (1,0)
        if self.board[BLACK_HOME][0] == ALL_CHECKERS:
            return (0,1)
        # Game not over
        return None

    def availablePositions(self,roll):
        '''Get a list valid moves based on a dice roll. DOESN'T INCLUDE RULE FOR DOUBLES ROLL'''
        possibleMoves = []
        board_copy = self.board.copy()
        # First get all moves using roll[0] first
        first_die_move = self.useRoll(roll[0],board_copy) # this is an array of possible from/to moves for roll[0]
        if first_die_move:
            for move in first_die_move:
                board_copy = self.updateBoard(move,board_copy)
                second_die_move = self.useRoll(roll[1],board_copy) # array of possible from/to moves for roll[1]
                possibleMoves += [(move,next_move) for next_move in second_die_move] # add every combination of move with values from move2
                board_copy = self.board.copy()

        if roll[0] == roll[1]:
            # Even though the rules for doubles isn't implemented, check for doubles in order to not waste time with a second loop
            return possibleMoves
            
        # Get all moves using the roll[1] first
        second_die_move = self.useRoll(roll[1],board_copy)
        if second_die_move:
            for move in second_die_move:
                board_copy = self.updateBoard(move,board_copy)
                first_die_move = self.useRoll(roll[0],board_copy)
                possibleMoves += [(move,next_move) for next_move in first_die_move]
                board_copy = self.board.copy()

        return possibleMoves

    def useRoll(self, die, board):
        '''Returns all actions for a single die roll on the given board'''
        all_home_board = True
        possibleMoves = []
        if board[BAR_IND][self.playerTurn] > 0:
            # Have to move off the bar first
            move_to = die if self.playerTurn == WHITE else (25 - die)
            return [(BAR_IND,move_to)]

        if self.playerTurn == WHITE:
            # White checkers move forward
            for i,loc in zip(range(1,WHITE_HOME),board[1:WHITE_HOME]):
                # Normal moves
                if loc[1] == WHITE:
                    if i < 19:
                        all_home_board = False
                    if i + die < WHITE_HOME and (board[i+die][1] != BLACK or board[i+die][0] < 2):
                        possibleMoves.append((i,i+die))
            if all_home_board:
                # Sending checker home
                for i,loc in zip(range(19,WHITE_HOME),board[19:WHITE_HOME]):
                    if i + die >= WHITE_HOME and loc[1] == WHITE:
                        possibleMoves.append((i,WHITE_HOME))
        else:
            # Black checkers move backward
            for i,loc in zip(range(WHITE_HOME-1,0,-1),board[WHITE_HOME-1:0:-1]):
                #print(i,':',loc)
                if loc[1] == BLACK:
                    if i > 6:
                        all_home_board = False
                    if i - die > 1 and (board[i-die][1] != WHITE or board[i-die][0] < 2):
                        possibleMoves.append((i,i-die))
            if all_home_board:
                for i,loc in zip(range(6,0,-1),board[6:0:-1]):
                    if i - die <= 0 and loc[1] == BLACK:
                        possibleMoves.append((i,BLACK_HOME))

        return possibleMoves


        
'''env = BackgammonEnv()
env.playerTurn = BLACK
some_moves = env.availablePositions((3,2))
for _ in range(5):
    some_moves = env.availablePositions((np.random.randint(1,7), np.random.randint(1,7)))
    print(len(some_moves))
    a_move = some_moves[np.random.randint(0,len(some_moves))]
    print(a_move)
    env.step(a_move[0])
    env.step(a_move[1])
    env.render()
    print('\n\n')
    env.playerTurn = WHITE if env.playerTurn == BLACK else BLACK'''