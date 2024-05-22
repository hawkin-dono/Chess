import torch.nn as nn
import torch.nn.functional as F
import torch

import os
import sys
import time

import numpy as np
from tqdm import tqdm

sys.path.append('../../')
from alphazero.utils import *
# from NeuralNet import NeuralNet

import torch
import torch.optim as optim
import random
from alphazero.Game import Game

args = dotdict({
    'lr': 0.001,
    # 'weight_decay': 0.1,
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 16, # 32,
    # 'cuda': torch.cuda.is_available(),
    'device': 'cuda' if torch.cuda.is_available() else 'cpu',
    # 'device': 'cuda:1',
    'num_channels': 128,
    'num_resBlocks': 2,
})

class OthelloNNet(nn.Module):
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        super(OthelloNNet, self).__init__()
        self.conv1 = nn.Conv2d(1, args.num_channels, 3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1)
        self.conv4 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1)

        self.bn1 = nn.BatchNorm2d(args.num_channels)
        self.bn2 = nn.BatchNorm2d(args.num_channels)
        self.bn3 = nn.BatchNorm2d(args.num_channels)
        self.bn4 = nn.BatchNorm2d(args.num_channels)

        self.fc1 = nn.Linear(args.num_channels*(self.board_x-4)*(self.board_y-4), 1024)
        self.fc_bn1 = nn.BatchNorm1d(1024)

        self.fc2 = nn.Linear(1024, 512)
        self.fc_bn2 = nn.BatchNorm1d(512)

        self.fc3 = nn.Linear(512, self.action_size)

        self.fc4 = nn.Linear(512, 1)

    def forward(self, s):
        #                                                           s: batch_size x board_x x board_y
        s = s.view(-1, 1, self.board_x, self.board_y)                # batch_size x 1 x board_x x board_y
        s = F.relu(self.bn1(self.conv1(s)))                          # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn2(self.conv2(s)))                          # batch_size x num_channels x board_x x board_y
        s = F.relu(self.bn3(self.conv3(s)))                          # batch_size x num_channels x (board_x-2) x (board_y-2)
        s = F.relu(self.bn4(self.conv4(s)))                          # batch_size x num_channels x (board_x-4) x (board_y-4)
        s = s.view(-1, self.args.num_channels*(self.board_x-4)*(self.board_y-4))

        s = F.dropout(F.relu(self.fc_bn1(self.fc1(s))), p=self.args.dropout, training=self.training)  # batch_size x 1024
        s = F.dropout(F.relu(self.fc_bn2(self.fc2(s))), p=self.args.dropout, training=self.training)  # batch_size x 512

        pi = self.fc3(s)                                                                         # batch_size x action_size
        v = self.fc4(s)                                                                          # batch_size x 1

        return F.log_softmax(pi, dim=1), torch.tanh(v)

class ResNet(nn.Module):
    def __init__(self, game, args):
        super().__init__()
        self.startBlock = nn.Sequential(
            nn.Conv2d(in_channels=6, out_channels= args.num_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d( args.num_channels),
            nn.ReLU(),
        )
        self.backBone = nn.ModuleList(
            [ResBlock( args.num_channels) for i in range(args.num_resBlocks)]
        )
        
        self.policyHead = nn.Sequential(
            nn.Conv2d(in_channels= args.num_channels, out_channels=4, kernel_size=3, padding=1),
            nn.BatchNorm2d(4),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(4 * 8 * 8, game.getActionSize())
            
        )
        self.valueHead = nn.Sequential(
            nn.Conv2d(in_channels= args.num_channels, out_channels=4, kernel_size=3, padding=1),
            nn.BatchNorm2d(4),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(4 * 8 * 8, 1),
        )

    def forward(self, x):     #batch_size x 6 x 8 x 8
        x = self.startBlock(x)           # batch_size x num_hidden x 8 x 8
        x = F.dropout(x, p= args.dropout)             # batch_size x num_hidden x 8 x 8
        
        for resBlock in self.backBone:
            x = resBlock(x)                 # batch_size x num_hidden x 8 x 8
            x = F.dropout(x, p= args.dropout)         # batch_size x num_hidden x 8 x 8
        policy = self.policyHead(x)             # batch_size x action_size
        value = self.valueHead(x)            # batch_size x 1
        return F.log_softmax(policy, dim=1), torch.tanh(value)

    
class ResBlock(nn.Module):
    def __init__(self, num_hidden):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=num_hidden, out_channels=num_hidden, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(num_features=num_hidden)
        self.conv2 = nn.Conv2d(in_channels=num_hidden, out_channels=num_hidden, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(num_features=num_hidden)

    def forward(self, x):
        residual = x 
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        x += residual
        x = F.relu(x)
        return x




class NeuralNet():
    """
    This class specifies the base NeuralNet class. To define your own neural
    network, subclass this class and implement the functions below. The neural
    network does not consider the current player, and instead only deals with
    the canonical form of the board.

    See othello/NNet.py for an example implementation.
    """

    def __init__(self, game):
        self.game = game
        self.nnet = ResNet(game, args)
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()

        # if args.cuda:
        #     self.nnet.cuda()
        self.nnet.to(args.device)

    def train(self, examples):
        """
        This function trains the neural network with examples obtained from
        self-play.

        Input:
            examples: a list of training examples, where each example is of form
                      (board, pi, v). pi is the MCTS informed policy vector for
                      the given board, and v is its value. The examples has
                      board in its canonical form.
        """
        optimizer = optim.Adam(self.nnet.parameters(), lr=args.lr, weight_decay=1e-4)
        random.shuffle(examples)
        
        for epoch in range(args.epochs):
            print('EPOCH ::: ' + str(epoch+1))
            self.nnet.train()
            pi_losses = AverageMeter()
            v_losses = AverageMeter()
            
            batch_count = int(len(examples) / args.batch_size)
            t = tqdm(range(batch_count), desc='Training Net')
            
            for batch_index in t:
                sample_ids = [i for i in range(batch_index * args.batch_size, min(len(examples) - 1, (batch_index + 1) * args.batch_size))]
                boards, pis, vs = list(zip(*[examples[i] for i in sample_ids]))      #chess.board, pi, v
           
                boards = self.game.get_encoded_states(boards)
                boards = torch.FloatTensor(np.array(boards).astype(np.float64))
                targert_pis = torch.FloatTensor(np.array(pis))
                target_vs = torch.FloatTensor(np.array(vs).astype(np.float64))
                
                #predict
                
                boards, targert_pis, target_vs = boards.contiguous().to(args.device), targert_pis.contiguous().to(args.device), target_vs.contiguous().to(args.device)
                    
                #compute output
                out_pi, out_v = self.nnet(boards)
                l_pi = self.loss_pi(targert_pis, out_pi)
                l_v = self.loss_v(target_vs, out_v)
                total_loss = l_pi + l_v
                
                #record loss
                pi_losses.update(l_pi.item(), boards.size(0))
                v_losses.update(l_v.item(), boards.size(0))
                t.set_postfix(Loss_pi=pi_losses, Loss_v=v_losses)
                
                #compute gradient and do optimizer step
                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()

    def predict(self, board):
        """
        Input:
            board: current board in its canonical form. chess.board

        Returns:
            pi: a policy vector for the current board- a numpy array of length
                game.getActionSize
            v: a float in [-1,1] that gives the value of the current board
        """
        # timing
        # start = time.time()
        board = self.game.get_encoded_states(board)
        
        # preparing input
        board = torch.FloatTensor(board.astype(np.float64))
        board = board.contiguous().to(args.device)
        # board = board.view(6, self.board_x, self.board_y)
        
        self.nnet.eval()
        with torch.no_grad():
            pi, v = self.nnet(board)
        
        #timing
        # end = time.time()
        # print('PREDICTION TIME TAKEN : {0:03f}'.format(end - start))
        
        return torch.exp(pi).data.cpu().numpy()[0], v.data.cpu().numpy()[0]
    
    def loss_pi(self, targets, outputs):
        return -torch.sum(targets * outputs) / targets.size()[0]

    def loss_v(self, targets, outputs):
        return torch.sum((targets - outputs.view(-1)) ** 2) / targets.size()[0]

    def save_checkpoint(self, folder='checkpoint', filename= 'checkpoint.pth.tar'):
        """
        Saves the current neural network (with its parameters) in
        folder/filename
        """
        # date = time.strftime("%H-%d-%m-%Y")
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        torch.save({
            'state_dict': self.nnet.state_dict(),
        }, filepath)

    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join('alphazero/',folder, filename)
        if not os.path.exists(filepath):
            raise ("No model in path {}".format(filepath))
        map_location = 'cuda' if (args.device != 'cpu') else 'cpu'
        checkpoint = torch.load(filepath, map_location=map_location)
        self.nnet.load_state_dict(checkpoint['state_dict'])
def count_parameters(model):
        return sum(p.numel() for p in model.parameters() if p.requires_grad)
 
def main():
    ##test base model
    print(args.device)
    game = Game()
    # model = ResNet(game, args)
    # print(model)
    
    
    # model = NeuralNet(game)
    # model = OthelloNNet(game, args)
    # board = game.getInitBoard()
    # board = game.get_encoded_states(board)
    # # print(board)
    # pi, v = model.predict(board)
    # # print(pi)
    # # print(v)

    # examples = [('board', pi, v)]
    # model.train(examples)

    ##test 3: nums of model parameters
    model = ResNet(game, args)
    # model = OthelloNNet(game, args)
    
    print(model)
    print(f'The model has {count_parameters(model):,} trainable parameters')
    
    
    

if __name__ == '__main__':
    main()
