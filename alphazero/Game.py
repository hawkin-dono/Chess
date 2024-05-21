import chess 
import numpy as np
import random
import re

reward_dict = {'p': 0.04, 'n': 0.12, 'b': 0.12, 'r': 0.2, 'q': 0.36}

class Game():
    """
    This class specifies the base Game class. To define your own game, subclass
    this class and implement the functions below. This works when the game is
    two-player, adversarial and turn-based.

    Use 1 for player1 and -1 for player2.

    See othello/OthelloGame.py for an example implementation.
    """
    def __init__(self):
        pass

    def getInitBoard(self)->chess.Board:
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        return chess.Board()

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return (8,8)

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        
        Explain:
            Each of the 8×8 positions identifies the square from which to “pick up” a piece.
            The first 64 plane represent the to-square.
            The last 12 planes represnet the promotion:
                4: capture left diagonal to r, n, b, q
                4: capture right diagonal to r, n, b, q
                4: no capture, step straight to r, n, b, q
                
                
        We represent the policy π(ajs) by a 8 × 8 × 73
        stack of planes encoding a probability distribution over 4,672 possible moves. Each of the 8×8
        positions identifies the square from which to “pick up” a piece. The first 56 planes encode
        possible ‘queen moves’ for any piece: a number of squares [1::7] in which the piece will be
        moved, along one of eight relative compass directions fN; NE; E; SE; S; SW; W; NWg. The
        next 8 planes encode possible knight moves for that piece. The final 9 planes encode possible
        underpromotions for pawn moves or captures in two possible diagonals, to knight, bishop or
        rook respectively. Other pawn moves or captures from the seventh rank are promoted to a
        queen.
        """
        # return 8 * 8 * 76 
        return 8 * 8 * 73   # 8x8 for the board, 73 for the possible moves (56 for queen moves, 8 for knight moves, 9 for underpromotions)
    
    def index_to_position(self, index):
        '''
        Convert index of board to position square (x, y)'''
        row = index // 8
        col = index % 8
        return (row, col)
    
    def position_to_index(self, position):
        ''' 
        Convert position square (x, y) of board to index'''
        return position[0] * 8 + position[1]
    
    def positon_to_string(self, position):
        ''' 
        Convert position square (x, y) of board to string'''
        return chr(position[1] + 97) + str(position[0] + 1)
    
    def string_to_position(self, string):
        '''
        Convert string to position square (x, y)'''
        return (int(string[1]) - 1, ord(string[0]) - 97)
    
    def action_to_policy_idx(self, board: chess.Board, action: str):
        """
        Input:
            action: a string of action in type uci
            'a2a3' or 'a7a8q'
        
        Returns:
            policy: a list of probabilities of length self.getActionSize()
        """
        # policy = np.array([0] * self.getActionSize())
        if action is None: return None
        
        from_square = self.string_to_position(action[:2])
        to_square = self.string_to_position(action[2:4])
        promote_piece = action[4:]
        
        # direction_map = {'N': 0, 'NE': 1, 'E': 2, 'SE': 3, 'S': 4, 'SW': 5, 'W': 6, 'NW': 7}
        direction_map = {(1,0): 0, (1,1): 1, (0,1): 2, (-1,1): 3, (-1,0): 4, (-1,-1): 5, (0,-1): 6, (1,-1): 7}
        # knight_move_map = {'NNE': 0, 'ENE': 1, 'ESE': 2, 'SSE': 3, 'SSW': 4, 'WSW': 5, 'WNW': 6, 'NNW': 7}
        knight_move_map = {(2, 1): 0, (1, 2): 1, (-1, 2): 2, (-2, 1): 3, (-2, -1): 4, (-1, -2): 5, (1, -2): 6, (2, -1): 7}
        
        # pawn_promotion_map = {'left': 0, 'right': 1, 'straight': 2}
        pawn_promotion_map = {(1, -1): 0, (1, 1): 1, (1, 0): 2}

        check_piece = self.get_piece_at(board, from_square)
        
        if check_piece is None: return None 
            
        if promote_piece != 'q' and promote_piece != '':  #under promotion of pawn
            direction = np.array(to_square) - np.array(from_square)
            direction = pawn_promotion_map[tuple(direction / np.max(np.abs(direction)))]
            promote_piece = ['n', 'b', 'r'].index(promote_piece)
            to_square = 64 + promote_piece * 3 + direction
            
        elif check_piece.piece_type == chess.KNIGHT:           #knight move
            direction = np.array(to_square) - np.array(from_square)
            direction = knight_move_map[tuple(direction)]
            to_square = 56 + direction
            
        else: #normal move
            # distance = np.array(to_square) - np.array(from_square)
            # direction = direction_map[tuple(distance / np.max(np.abs(distance)))]
            distance = np.array(to_square) - np.array(from_square)
            # direction = direction_map[tuple(distance / np.max(np.abs(distance)))]
            direction = direction_map[tuple(np.sign(distance))]
            distance = np.max(np.abs(distance))
            to_square = direction + (distance - 1)*8
            
        idx = self.position_to_index(from_square) * 73 + to_square
        # print(idx)
        
        # policy[idx] = 1
        return idx
    
    def action_to_policy(self, board: chess.Board, action: str):
        policy = np.array([0] * self.getActionSize())
        idx = self.action_to_policy_idx(board, action)
        policy[idx] = 1
        return policy
    
    def policy_idx_to_action(self, idx: int, board: chess.Board, policy: np.array= None, require_legal=True):
        """
        Input:
            policy: a list of probabilities of length self.getActionSize()
        
        Returns:
            action: 
        """
        # idx = np.argmax(policy)
        
        from_square = self.index_to_position(idx // 73)
        to_square = idx % 73
        promote_piece = ''
        
        # direction_map = {0: 'N', 1: 'NE', 2: 'E', 3: 'SE', 4: 'S', 5: 'SW', 6: 'W', 7: 'NW'}
        direction_map = {0: [1, 0], 1: [1, 1], 2: [0, 1], 3: [-1, 1], 4: [-1, 0], 5: [-1, -1], 6: [0, -1], 7: [1, -1]}
        # knight_move_map = {0: 'NNE', 1: 'ENE', 2: 'ESE', 3: 'SSE', 4: 'SSW', 5: 'WSW', 6: 'WNW', 7: 'NNW'}
        knight_move_map = {0: [2, 1], 1: [1, 2], 2: [-1, 2], 3: [-2, 1], 4: [-2, -1], 5: [-1, -2], 6: [1, -2], 7: [2, -1]}
        
        
        if to_square < 56:        #normal move
            direction = to_square % 8
            distance = to_square // 8 + 1
            
            to_square = np.array(from_square) + np.array(direction_map[direction]) * distance
        
        elif to_square < 64:             #knight move
            direction = to_square % 8
            to_square = np.array(from_square) + np.array(knight_move_map[direction])
            
            
        else:
            promotion = (to_square - 64) // 3            # k, b , r
            direction = (to_square - 64) % 3          # left, right, straight
            if direction == 0:
                to_square = np.array(from_square) + np.array([1, -1])
            elif direction == 1:
                to_square = np.array(from_square) + np.array([1, 1])
            else:
                to_square = np.array(from_square) + np.array([1, 0])

            promote_to = ['n', 'b', 'r']
            promote_piece = promote_to[promotion]
        
        try:
            if promote_piece == '' and self.get_piece_at(board, from_square).piece_type == chess.PAWN and to_square[0] == 7:
                promote_piece = 'q'
        except:
            pass
            
        
        move_uci = self.positon_to_string(from_square) + self.positon_to_string(to_square) + promote_piece
        # print(move_uci)
        if not require_legal:
            return move_uci
        try: 
            if board.is_legal(chess.Move.from_uci(move_uci)):
                return move_uci
        except:
            return None
    
    def policy_to_action(self, board: chess.Board, policy: np.array):
        idx = np.argmax(policy)
        return self.policy_idx_to_action(idx, board, policy)

    def get_piece_at(self, board, position):
        return board.piece_at(chess.square(position[1], position[0]))  #file , rank
    
    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        b = board.copy()
        move = chess.Move.from_uci(str(action))
        if b.is_legal(move):
            b.push(move)
        return b, -player
        
    def getAllEnemysMoves(self, state):
        moves = [] 
        for move in state.legal_moves:
            from_squre = move.from_square
            to_square = move.to_square
            
            using_piece = state.piece_at(from_squre)
            if using_piece.symbol() in ['p', 'n', 'b', 'r', 'q', 'k']:
                moves.append(str(move))
        return moves
        

    def getAllPlayerMoves(self, state):
        moves = [] 
        for move in state.legal_moves:
            from_squre = move.from_square
            to_square = move.to_square
            
            using_piece = state.piece_at(from_squre)
            if using_piece.symbol() in ['P', 'N', 'B', 'R', 'Q', 'K']:
                moves.append(str(move))
        return moves 

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        # valids = [0] * self.getActionSize()
        # for move in board.legal_moves:
        #     valids[self.action_to_policy_idx(board, move.uci())] = 1
        # return valids
        valids = [0] * self.getActionSize()
        if player == 1:
            moves = self.getAllPlayerMoves(board)
            for move in moves:
                valids[self.action_to_policy_idx(board, move)] = 1
        else:
            moves = self.getAllEnemysMoves(board)
            for move in moves:
                valids[self.action_to_policy_idx(board, move)] = 1
        
        return valids

    def getGameEnded(self, board: chess.Board, player: int):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
               
        """
        if board.is_checkmate():
            if board.turn == player:
                return -1
            else:
                return 1
        
        if len(board.move_stack) > 100:
            return 1e-4
        
        if board.is_seventyfive_moves():
            return 1e-4
        
        # if board.is_fifty_moves():
        #     return 1e-4
        
        if board.is_stalemate():
            return 1e-4
        
        if board.is_insufficient_material():
            return 1e-4
        
        if board.is_fivefold_repetition():
            return 1e-4
        
        return 0

    
    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        if type(board) == chess.Board:
            return board.mirror() if player == -1 else board
        res = [] 
        for i in board:
            res.append(i.mirror() if player == -1 else i)
        return res 
    
    def getCanonicalFormParallel(self, board, player):
        res = []
        for b in board:
            res.append(b.mirror() if player == -1 else b)
    
    def getCanonicalAction(self, action, player):
        """
        Input:
            action: a string of action in uci formatn  (e.g. 'b1a3') -> b8a6
            player: current player (1 or -1)

        Returns:
            canonicalAction: returns canonical form of action. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            action as is. When the player is black, we can invert
                            the action.
        """
        if player == 1: return action
        
        promotion_piece = action[4:]
        vertical_flip = {'a': 'h', 'b': 'g', 'c': 'f', 'd': 'e', 'e': 'd', 'f': 'c', 'g': 'b', 'h': 'a'}
        horizontal_flip = {'1': '8', '2': '7', '3': '6', '4': '5', '5': '4', '6': '3', '7': '2', '8': '1'}
        
        action = action[0] + horizontal_flip[action[1]] + action[2] + horizontal_flip[action[3]] + promotion_piece
        return action
    
    def getSymmetriesMove(self, move):
        '''
        Input:
            move: a string of move in uci format
        Returns:
            symmForms: a list of moves which are symmetrical to the input move
        b1a3 -> b8a6, g1h3, g8h6
        '''
        promotion_piece = move[4:]
        vertical_flip = {'a': 'h', 'b': 'g', 'c': 'f', 'd': 'e', 'e': 'd', 'f': 'c', 'g': 'b', 'h': 'a'}
        horizontal_flip = {'1': '8', '2': '7', '3': '6', '4': '5', '5': '4', '6': '3', '7': '2', '8': '1'}
        
        # res = ['' for i in range(4)] 
        res = ['' for i in range(2)]
        res[0] = move 
        # res[1] = move[0] + horizontal_flip[move[1]] + move[2] + horizontal_flip[move[3]] + promotion_piece
        res[1] = vertical_flip[move[0]] + move[1] + vertical_flip[move[2]] + move[3] + promotion_piece
        # res[3] = vertical_flip[move[0]] + horizontal_flip[move[1]] + vertical_flip[move[2]] + horizontal_flip[move[3]] + promotion_piece
        
        return res

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        # board b1a3
        # board2 = board.copy().mirror()                  # b8a6
        board2 = board.transform(chess.flip_horizontal)     # g1h3
        # board4 = board3.copy().mirror()                 # g8h6  
        
        # pi2 = [0] * len(pi)
        pi2 = [0] * len(pi)
        # pi4 = [0] * len(pi)
        
        for idx in range(self.getActionSize()):
            action = self.policy_idx_to_action(idx, board, pi)
            if action is None: continue
            
            # _, action2, action3, action4 = self.getSymmetriesMove(action)
            _, action2 = self.getSymmetriesMove(action)
            idx2 = self.action_to_policy_idx(board2, action2)
            # idx3 = self.action_to_policy_idx(board3, action3)
            # idx4 = self.action_to_policy_idx(board4, action4)
            
            pi2[idx2] = pi[idx]
            # pi3[idx3] = pi[idx]
            # pi4[idx4] = pi[idx]
        
        return [(board, pi), (board2, pi2)] #, (board3, pi3), (board4, pi4)]
        
        

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        return board.fen()
    
    def create_rep_layer(self, board, type):
        ''' 
        board: chess.Board
        type: 'p' or 'r' or 'n' or 'b' or 'q' or 'k
        '''
        s = str(board) 
        s = re.sub(f'[^{type}{type.upper()} \n]', '.', s)
        s = re.sub(f'{type}', '-1', s)
        s = re.sub(f'{type.upper()}', '1', s)
        s = re.sub(f'\.', '0', s)
        
        board_mat = []
        for row in s.split('\n'):
            row = row.split(' ')
            row = [int(x) for x in row]
            board_mat.append(row)
        return np.array(board_mat)

    def get_encoded_single_state(self, state):
        pieces = ['p','r', 'n', 'b', 'q', 'k']
        layers = []
        for piece in pieces:
            layers.append(self.create_rep_layer(state, piece))
        board_rep = np.stack (layers)
        return board_rep
    
    def get_encoded_states(self, states):
        res = []
        if type(states) == chess.Board:
            res.append(self.get_encoded_single_state(states))
            return np.array(res).astype(np.float32)
        for i in states:
            res.append(self.get_encoded_single_state(i))
        return np.array(res).astype(np.float32)
    
    def get_bonus_reward(self, canonicalBoard: chess.Board, action: str):
        res = 0
        from_square = self.string_to_position(action[:2])
        to_square = self.string_to_position(action[2:4])
        promtion = action[4:]
        if self.get_piece_at(canonicalBoard, to_square) is not None:
            res += reward_dict[self.get_piece_at(canonicalBoard, to_square).symbol()]
        
        if promtion != '':
            res += reward_dict[promtion]
        
        return res
    
def main():
    ## test 1
    game = Game()
    board = game.getInitBoard()
    # print(board)
    # print(game.getBoardSize())
    # print(game.getActionSize())
    
    ## test 2 get piece at position
    # pos = (1, 0)
    # print(game.get_piece_at(board, pos))
    
    # test 3: index to position and position to string
    # idx = 10
    # pos = game.index_to_position(idx)
    # print(pos)
    # print(game.positon_to_string(pos))
    
    ##test 4: policy to action
    
    # policy = np.array([0] * game.getActionSize())
    # # n = random.randint(0, game.getActionSize()) 
    # n = 494
    # policy[n] = 1
    # print(n)
    # # print(game.policy_to_action(board, policy))
    # print(game.policy_idx_to_action(n, board))
    
    ##test 4: action to policy idx and policy idx to action of promotion
    board = chess.Board('n2k4/1P6/2K5/8/8/8/8/8 w - - 0 1')
    print(board)
    
    print(game.get_bonus_reward(board, 'b7a8q'))
    # action = 'b7a8r'
    # policy_idx = game.action_to_policy_idx(board, action)
    # print(policy_idx)
    # print(game.policy_idx_to_action(policy_idx, board))
    
    
    
    
    
    
    ##test 5 action to policy idx
    # action = 'h8i10'
    # print(game.action_to_policy_idx(board, action))
    
    ##test 5: string to position
    # string = 'h2'
    # print(game.string_to_position(string))
    
    ##test 6: action to policy
    # action = 'b1a3'
    # print(game.action_to_policy(board, action))
    
    ## test 7: get next state
    # player = 1
    # action = 'b1a3'
    # board, player = game.getNextState(board, player, action)
    # print(board)
    
    ## test 8: get valid moves
    # print(game.getValidMoves(board, player))
    
    ##test 9: get game ended
    # print(game.getGameEnded(board, player))
    
    ##test 10: get canonical form
    # print(game.getCanonicalForm(board, player))
    
    ##test 11: get symmetries move 
    # move = 'a7a8q'
    # print(game.getSymmetriesMove(move))
    
    ##test 11: get symmetries
    # player = 1
    # action = 'b1a3'
    # board, player = game.getNextState(board, player, action)
    # print(board)
    # move = 'b2b3'
    # policy = np.array([0] * game.getActionSize())
    # n = game.action_to_policy_idx(board, move)
    # policy[n] = 1
    
    # print(game.getSymmetries(board, policy))
    
    ##test 12: get string representation
    # print(game.stringRepresentation(board))
    
    ##test 13: check end game
    # fen = '8/7k/4p3/8/2P5/8/5PPP/r5K1 w - - 0 1'
    # board = chess.Board(fen)
    # print(board)
    # turn = board.turn
    # res = game.getGameEnded(board, 1)
    # print(turn)
    # print(res)
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    main()
