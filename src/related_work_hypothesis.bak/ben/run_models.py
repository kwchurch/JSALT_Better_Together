#!/usr/bin/env python

import csv
import pandas as pd
import ast
import torch
from torch import nn, tensor
import os, sys, argparse, time, gc, socket
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import math
import torch._dynamo as dynamo
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
import torch.nn.functional as F
import string


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# to combat memory problems
torch.cuda.empty_cache()

class Net(nn.Module):
    def __init__(self, dim, input_dim, output_dim, num_layers, dropout):
        super(Net, self).__init__()
        
        layers = [nn.Linear(input_dim, dim), nn.LayerNorm(dim), nn.GELU(), nn.Dropout(dropout)]
        for _ in range(num_layers - 1):
            layers.extend([nn.Linear(dim, dim), nn.LayerNorm(dim), nn.GELU(), nn.Dropout(dropout)])
        layers.append(nn.Linear(dim, output_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, input):
        return self.net(input)

class CustomTrainer():
    def __init__(self, params):
        """
        args:
            params
                epochs: Number of times we train the model on the entire training set
                model: Model that we are training.
                optimizer: Optimizer that we use to modifiy learning rates, and backpropogate through model.
                train_batch_size: Batch size for training runs.
                train_eval_batch_size: Batch size for eval runs.
                debug_overflow: Flag is active if we want to see reasons behind Nans, in underflow and overflow.
                X_train: X values for training data (In this case, embeddings for related work or all references).
                X_test: X values for test data. (Same as above)
                y_train: y values for training data (Embeddings produced by ProNE, which we treat as a baseline).
                y_test: y values for test data. (Same as above)
                case: Using the related work references, or all of the references (case one and case two respectively).
                dimension: Dimension of the hidden layers of the model.
                num_layers: Number of layers in the model.
                dropout: Dropout of the model.
                pretrained_model: If we want to use object for evaluation only, we need to load a pretrained model in.
                eval: If we want to use the object for evaluation only, this flag is set to true.
        """
        self.epochs = params['epochs']
        self.model = params['model']
        self.optimizer = params['optimizer']
        self.train_batch_size = params['train_batch_size']
        self.eval_batch_size = params['eval_batch_size']
        self.debug_overflow = params['debug']
        self.X_train = params['X_train']
        self.X_test = params['X_test']
        self.y_train = params['y_train']
        self.y_test = params['y_test']
        self.case = params['case']
        self.dimension = params['dim']
        self.num_layers = params['num_layers']
        self.dropout = params['dropout']
        self.pretrained_model = params['pretrained_model']
        self.eval = params['eval']

    def plot(self, loss, epoch, case, num_layers, dimension, dropout):
        timesteps = np.arange(1, loss.shape[0] + 1)
        # Plot the MSE vs timesteps
        plt.plot(timesteps, loss)
        # Add axis labels and a title
        plt.xlabel('Timestep')
        plt.ylabel('MSE Loss')
        plt.title('Loss')
        plt.savefig('/work/nlp/b.irving/related_work/loss/model_' + str(num_layers) + '_' + str(dimension) + '_' + str(dropout) + '_' + case + '_' + str(epoch) + '.png')
        plt.close()

    def test(self, model,X,Y):
        cosines = []
        for x in range(len(Y)):
            single_example = torch.tensor(X.iloc[x].values).to(device)
            salida = torch.tensor(Y.iloc[x].values).to(device)
            predicted_output = model.forward(single_example)
            predic = predicted_output[0]
            similarity = F.cosine_similarity(salida.reshape(1, -1), predic.reshape(1, -1))
            cosines.append(similarity)
        return cosines

    def train(self):

        if(self.debug_overflow):
            debug_overflow = DebugUnderflowOverflow(self.model)
        self.model = self.model.to(torch.float64)

        # generalize all of these arguments
        cosine = torch.optim.lr_scheduler.CosineAnnealingLR(self.optimizer, self.epochs)

        # we will use a similar loss to rodolfo
        loss_fct = nn.MSELoss()

        counter = 0
        training_loss_over_epochs = []
        if(not self.eval):
            for epoch in range(self.epochs):
                t0 = time.time()
                training_loss = []
                train_accuracies = []
                train_auroc = []
                total_acc = 0

                for train_index in range(0, len(self.X_train.index) - self.train_batch_size, self.train_batch_size):
                    self.model.zero_grad()
                    
                    #start = torch.cuda.Event(enable_timing=True)
                    #end = torch.cuda.Event(enable_timing=True)
                    #start.record()                
                    out = self.model(torch.tensor(X_train.iloc[train_index:train_index+self.train_batch_size].values).to(device))
                    #end.record()
                    #torch.cuda.synchronize()

                    truth = torch.tensor(self.y_train.iloc[train_index:train_index+self.train_batch_size].values).to(device)
                    loss = loss_fct(out.float().to(device), truth.float().to(device))
                    training_loss.append(loss.item())
                    self.optimizer.zero_grad()
                    loss.backward()
                    self.optimizer.step()
                    # Every 10000 steps, we evaluate the loss
                    if(train_index % 10000 == 0):
                        print('loss: ',  loss.item())

                print('Epoch length: ', str(time.time() - t0))
                self.plot(np.array(training_loss), epoch, self.case, self.num_layers, self.dimension, self.dropout)
                print('\n')
                print('epoch: ', counter)
                counter += 1
                print('loss total: ', sum(training_loss))
                print('\n')
                training_loss_over_epochs.append(training_loss)
                #exponential.step()
                cosine.step()
                # save the model after each epoch
                torch.save(self.model, 'related_papers_' + str(self.num_layers) + '_' + str(self.dimension) + '_' + str(self.dropout) + '_' + str(epoch + 1) + '_' + str(self.case) + '.pt')
        elif (self.eval and self.pretrained_model is not None):
            self.model = torch.load(self.pretrained_model).to(torch.float64).to(device)
        else:
            raise ValueError('For model evaluation, please provide a valid pretrained model.')
        self.model.eval()
        #model = torch.load('related_papers_' + str(self.num_layers) + '_' + str(self.dimension) + '_' + str(self.dropout) + '_' + str(self.epochs) + '_' + str(self.case) + '.pt')
        with torch.no_grad():
            cosines = self.test(model, self.X_test, self.y_test)
        return cosines

if __name__=='__main__':
    torch._dynamo.config.verbose = True
    torch._dynamo.config.suppress_errors = True
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--learning_rate', type=float, help='Learning rate for the trainer', default=5e-5)
    parser.add_argument('-p', '--pretrained', type = str, help='Location of a previously trained model')
    parser.add_argument('-e', '--epochs', type = int, help = 'Number of epochs', default = 3)
    parser.add_argument('-o', '--optimizer', type = str, help = 'Optimizer', default = 'AdamW')
    parser.add_argument('-d', '--decay', type = float, help = 'Weight decay for the optimizer', default = 0.0)
    parser.add_argument('-b1','--beta_1', type = float, help='Beta1 for the optimizer', default = 0.9)
    parser.add_argument('-b2', '--beta_2', type = float, help = 'Beta2 for the optimizer', default= 0.999)
    parser.add_argument('-c', '--classes', type= int, help='Number of classes', default = 2)
    parser.add_argument('-tb', '--train_batch_size', type = int, help = 'Batch size for training step', default = 32)
    parser.add_argument('-ev', '--eval_batch_size', type = int, help = 'Batch size for eval step', default = 1)
    parser.add_argument('-db', '--debug', type = bool, help = 'Debug underflow and overflow', default = False)
    parser.add_argument('-t', '--task', type = str, help = 'Task type for training loop', default = 'classification')
    parser.add_argument('-cl', '--cache_location', type = str, help = 'Location for HuggingFace files')
    parser.add_argument('-di', '--dimension', type=int, help = 'internal dimension', default = 128)
    parser.add_argument('-ca', '--case', type=str, help = 'Merged df or not', default='one')
    parser.add_argument('-nl', '--num_layers', type=int, help= 'The number of layers to use in the model', default=3)
    parser.add_argument('-do', '--dropout', type=float, help='Dropout in our model', default=0.0)
    parser.add_argument('-ptm', '--pretrained_model', type=str, help='Path to model', default=None)
    parser.add_argument('-eva', '--eval', type=bool, help='Flag for evaluating a model', default=False)
    parser.add_argument('-m', '--metric', type = str, help = 'Evalutation metric')
    args = parser.parse_args()

    t0 = time.time()
    df_x = pd.read_csv('rw.csv')
    df_y = pd.read_csv('all_citations.csv')
    df_z = pd.read_csv('prone_y.csv')
    print('Data load finished in: ', str(time.time() - t0))

    #Case 1: All references
    if (args.case == 'one'):
        print('Merged')
        model = Net(args.dimension, 560, 280, args.num_layers, dropout=args.dropout)
        merged_df = pd.concat([df_x.iloc[:, 1:], df_y.iloc[:, 1:]], axis=1)
        print(merged_df.shape)
        X_train, X_test, Y_train, Y_test = train_test_split(merged_df, df_z.iloc[:, 1:], test_size=0.2, random_state=42)
    #Case 2: Only related work references
    elif (args.case == 'two'):
        print('Just related work')
        model = Net(args.dimension, 280, 280, args.num_layers, dropout=args.dropout)
        X_train, X_test, Y_train, Y_test = train_test_split(df_x.iloc[:, 1:], df_z.iloc[:, 1:], test_size=0.2, random_state=42)
    else:
        raise ValueError('Case number not supported')
    
    if(optimizer == 'AdamW'):
        optimizer = torch.optim.AdamW(params = model.parameters(), lr=args.learning_rate, weight_decay=args.decay, betas=(args.beta_1, args.beta_2))
    elif(optimizer == 'Adam'):
        optimizer = torch.optim.Adam(params = model.parameters(), lr=args.learning_rate, weight_decay=args.decay)
    else: 
        raise ValueError("This type of optimizer is not supported.")

    params = {
            'lr': lr,
            'pretrained_model': args.pretrained_model,
            'epochs': args.epochs,
            'optimizer': optimizer,
            'train_batch_size': args.train_batch_size,
            'eval_batch_size': args.eval_batch_size,
            'model':model.to(device),
            'X_train':X_train,
            'X_test':X_test,
            'y_train':Y_train,
            'y_test':Y_test,
            'debug':args.debug,
            'dim':args.dimension,
            'dropout':args.dropout,
            'case':args.case, 
            'num_layers':args.num_layers,
            'eval':args.eval,
            'pretrained_model':args.pretrained_model
    }

    train = CustomTrainer(params)
    cosines = train.train()
    torch.save(cosines, '/work/nlp/b.irving/related_work/cosine_outputs/cosines_' + str(args.num_layers) + '_' + str(args.dimension) + '_' + str(args.dropout) + '_' + str(args.epochs) + '_' + args.case + '.pt')
    print('Done in ' +  str(time.time() - t0) + ' seconds.')
