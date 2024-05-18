import logging
# from Coach import Coach
# from CoachParallel import CoachParallel
from alphazero.Game import  Game
from alphazero.NeuralNet import NeuralNet as nn
from alphazero.utils import *
from alphazero.MCTS import MCTS
import numpy as np
import time
import chess 

log = logging.getLogger(__name__)

args = dotdict({
    'numIters': 20,
    # nums of playing multiple (parallel) games times
    'numEps': 2,  # 20      # number of complete self-play prallel games to simulate during a new iteration.  
    'num_parallel_games': 4,  #nums of parallel games at each episode       => self play numeps * num_parallel_games games
    'tempThreshold': 15,        #
    'updateThreshold': 0.51,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 20000,  # Number of game examples to train the neural networks.
    'numMCTSSims': 800,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 4,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,
    'checkpoint': './model/',
    'load_model': False,
    'load_data': False,
    'load_folder_file': ('model/','checkpoint_12.pth.tar'),
    'load_data_file': ('model/', 'checkpoint_0.pth.tar'),
    'numItersForTrainExamplesHistory': 10,
})

class AlphaZeroAI:
    def __init__(self):
        self.game = Game()
        self.nnet: nn = nn(self.game)
        if args.load_model:
            self.nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
        self.mcts = MCTS(self.game, self.nnet, args)
        
        
    def get_best_move(self, board):
        current_player = 1 if board.turn else -1
        self.mcts = MCTS(self.game, self.nnet, args)
        
        canonicalBoard = self.game.getCanonicalForm(board, current_player)
        actionprobs = self.mcts.getActionProb(canonicalBoard, temp=0) 
        action_idx = np.argmax(actionprobs)
        action = self.game.policy_idx_to_action(action_idx, board=canonicalBoard)
        try:
            action = self.game.getCanonicalAction(action, current_player)
        except:
            return None
        
        return action 
    
    def get_best_move_no_search(self, board):
        current_player = 1 if board.turn else -1
        self.mcts = MCTS(self.game, self.nnet, args)
        canonicalBoard = self.game.getCanonicalForm(board, current_player)
        policy, v = self.nnet.predict(canonicalBoard)
        valids = self.game.getValidMoves(canonicalBoard, 1)
        policy = policy * valids  # masking invalid moves
        action_idx = np.argmax(policy)
        action = self.game.policy_idx_to_action(action_idx, board=canonicalBoard)
        action = self.game.getCanonicalAction(action, current_player)
        
        return action 

def main():
    ai = AlphaZeroAI()
    board = chess.Board('1k6/6R1/3K4/8/8/8/8/8 w - - 0 1')
    print(board)
    while True:
        move = ai.get_best_move(board)
        board.push(chess.Move.from_uci(move))
        print(board)
        if board.is_game_over():
            break
    
if __name__ == '__main__':
    main()