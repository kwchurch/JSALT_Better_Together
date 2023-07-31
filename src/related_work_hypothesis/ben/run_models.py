#!/usr/bin/env python

import csv
import pandas as pd
import os
import csv
import ast
import torch
from torch import nn, tensor
import os, sys, argparse, time, gc, socket
from torchvision.io import read_image
import numpy as np
import torch
from torch import nn, tensor
import os
import matplotlib.pyplot as plt
from PIL import Image
import requests
from tqdm import tqdm
import math
import torch._dynamo as dynamo
import time
from sklearn.model_selection import train_test_split
import argparse
from sklearn.metrics.pairwise import cosine_similarity
import torch.nn.functional as F


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# to combat memory problems
torch.cuda.empty_cache()

# can easily change this into any structure
# can produce prone embeddings in live time?
class net(nn.Module):
    # simple vector to vector regression
    # transformer?
    def __init__(self, dim, input_dim, output_dim, dropout=0.0):
        super(net, self).__init__()

        self.net = nn.ModuleList([nn.Linear(input_dim, dim), 
        nn.LayerNorm(dim), nn.GELU(), 
        nn.Dropout(dropout), 
        nn.Linear(dim, dim), 
        nn.LayerNorm(dim), nn.GELU(),
        nn.Dropout(dropout),
        nn.Linear(dim, dim), 
        nn.LayerNorm(dim), nn.GELU(), 
        nn.Dropout(dropout),
        # output layer
        nn.Linear(dim, output_dim)])

    def forward(self, input):
        inter = input
        for layer in self.net:
            inter = layer(inter)
        return inter

class CustomTrainer():
    def __init__(self, params):
        """
        A trainer class, that is easy for me to use. Probably less efficient, and most
        certainly less generalizable than the HuggingFace Trainer class. But at least
        I understand how to use it, and perhaps others will as well.

        I think the trick is in the manner in which data is fed into the training loop.

        args:
            params
                epochs
                model
                tokenizer
                optimizer
                train_batch_size
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

    def plot(self, loss, epoch, case):
        timesteps = np.arange(1, loss.shape[0] + 1)
        # Plot the MSE vs timesteps
        plt.plot(timesteps, loss)
        # Add axis labels and a title
        plt.xlabel('Timestep')
        plt.ylabel('MSE Loss')
        plt.title('Loss')
        plt.savefig('/work/nlp/b.irving/related_work/model_' + str(epoch) + '_' + case + '.png')
        plt.close()

    # just run on all of the y_values
    def test(self, model,X,Y):
        cosines = []
        for x in range(len(Y)):
            single_example = torch.tensor(X.iloc[x].values).to(device)
            salida = torch.tensor(Y.iloc[x].values).to(device)
            #df_single_example = pd.DataFrame([single_example])
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
        for epoch in range(self.epochs):
            training_loss = []
            train_accuracies = []
            train_auroc = []
            total_acc = 0
            #num_train_steps = len(train_x) - 1

            # optimize for speed?
            for train_index in range(0, len(self.X_train.index) - self.train_batch_size, self.train_batch_size):
                self.model.zero_grad()
                # pad to the max length, because the longest length would exceed the input size 
                
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

                #if(train_index % 100 == 0):
                #    print('loss: ',  loss.item())

            # we want to save the loss curve for both cases
            self.plot(np.array(training_loss), epoch, self.case)
            print('\n')
            print('epoch: ', counter)
            counter += 1
            print('loss total: ', sum(training_loss))
            print('\n')
            training_loss_over_epochs.append(training_loss)
            #exponential.step()
            cosine.step()
            self.model.eval()
        
        # save the model before the evaluation stage
        torch.save(self.model, 'related_papers_' + self.case + '.pt')
        
        #model = torch.load('related_papers_' + self.case + '.pt')
        #model = torch.load('related_papers_.pt')
        with torch.no_grad():
            cosines = self.test(model, self.X_test, self.y_test)
        return cosines

if __name__=='__main__':
    torch._dynamo.config.verbose = True
    torch._dynamo.config.suppress_errors = True
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--learning_rate', type=float, help='Learning rate for the trainer', default=5e-5)
    parser.add_argument('-p', '--pretrained', type = str, help='Location of a previously trained model')
    parser.add_argument('-e', '--epochs', type = int, help = 'Number of epochs', default = 1)
    parser.add_argument('-o', '--optimizer', type = str, help = 'Optimizer', default = 'AdamW')
    parser.add_argument('-d', '--decay', type = float, help = 'Weight decay for the optimizer', default = 0.0)
    parser.add_argument('-b1','--beta_1', type = float, help='Beta1 for the optimizer', default = 0.9)
    parser.add_argument('-b2', '--beta_2', type = float, help = 'Beta2 for the optimizer', default= 0.999)
    parser.add_argument('-c', '--classes', type= int, help='Number of classes', default = 2)
    parser.add_argument('-tb', '--train_batch_size', type = int, help = 'Batch size for training step', default = 8)
    parser.add_argument('-ev', '--eval_batch_size', type = int, help = 'Batch size for eval step', default = 1)
    parser.add_argument('-db', '--debug', type = bool, help = 'Debug underflow and overflow', default = False)
    parser.add_argument('-t', '--task', type = str, help = 'Task type for training loop', default = 'classification')
    parser.add_argument('-cl', '--cache_location', type = str, help = 'Location for HuggingFace files')
    parser.add_argument('-di', '--dimension', type=int, help = 'internal dimension', default = 128)
    parser.add_argument('-ca', '--case', type=str, help = 'Merged df or not', default='one')

    # what are the best metrics?
    parser.add_argument('-m', '--metric', type = str, help = 'Evalutation metric')
    args = parser.parse_args()

    # Why explicitly state these
    lr = args.learning_rate
    pretrained_model = args.pretrained
    epochs = args.epochs
    optimizer = args.optimizer
    decay = args.decay
    beta_1 = args.beta_1
    beta_2 = args.beta_2
    num_classes = args.classes
    train_batch_size = args.train_batch_size
    eval_batch_size = args.eval_batch_size
    task = args.task
    debug = args.debug
    cache_location = args.cache_location

    # add training args
    t0 = time.time()
    """
    FILEPATH = '/work/nlp/b.irving/related_work/predicting_vectors'
    raw_dirs = set([d for d in os.listdir(FILEPATH)])
    x,z,y = [],[],[]
    for archivo in raw_dirs:
        if (archivo == 'predicting_vectors'):
            pass
        else:
            with open(FILEPATH+"/"+archivo, "r") as file:
                for line in file:
                    if line.find("V") == -1:
                        line = line.replace("\n","")
                        line = line.replace("'","")
                        z.append(ast.literal_eval(line.split("\t")[1]))
                        x.append(ast.literal_eval(line.split("\t")[2]))
                        y.append(ast.literal_eval(line.split("\t")[3]))

    df_x = pd.DataFrame(x)
    df_y = pd.DataFrame(y)
    df_z = pd.DataFrame(z)
    df_x.to_csv('rw.csv')
    df_y.to_csv('all_citations.csv')
    df_z.to_csv('prone_y.csv')
    
    """
    df_x = pd.read_csv('rw.csv')
    df_y = pd.read_csv('all_citations.csv')
    df_z = pd.read_csv('prone_y.csv')
    print('Data prep finished in: ', str(time.time() - t0))

    #Case 1: all references
    if (args.case == 'one'):
        print('Merged')
        model = net(args.dimension, 560, 280, dropout=0.0)
        merged_df = pd.concat([df_x.iloc[:, 1:], df_y.iloc[:, 1:]], axis=1)
        print(merged_df.shape)
        X_train, X_test, Y_train, Y_test = train_test_split(merged_df, df_z.iloc[:, 1:], test_size=0.2, random_state=42)
    elif (args.case == 'two'):
        print('Just related work')
        model = net(args.dimension, 280, 280)
        X_train, X_test, Y_train, Y_test = train_test_split(df_x.iloc[:, 1:], df_z.iloc[:, 1:], test_size=0.2, random_state=42)
    else:
        raise ValueError('Case number not supported')
    
    if(optimizer == 'AdamW'):
        optimizer = torch.optim.AdamW(params = model.parameters(), lr=lr, weight_decay=decay, betas=(beta_1, beta_2))
    elif(optimizer == 'Adam'):
        optimizer = torch.optim.Adam(params = model.parameters(), lr=lr, weight_decay=decay)
    else: 
        raise ValueError("This type of optimizer is not supported.")

    params = {
            'lr': lr,
            'pretrained_model': pretrained_model,
            'epochs': epochs,
            'optimizer': optimizer,
            'train_batch_size': train_batch_size,
            'eval_batch_size': eval_batch_size,
            'model':model.to(device),
            'X_train':X_train,
            'X_test':X_test,
            'y_train':Y_train,
            'y_test':Y_test,
            'debug':debug,
            'case':args.case
    }

    train = CustomTrainer(params)
    cosines = train.train()
    torch.save(cosines, 'cosines_' + args.case + '.pt')
    print('Done in ' +  str(time.time() - t0) + ' seconds.')
