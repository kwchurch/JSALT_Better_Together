#!/bin/bash

#sbatch --mem=10G --time=00:15:00 -p gpu --gres=gpu:v100-pcie:1 rodolfo_run.py
sbatch --mem=10G --time=00:15:00 -p gpu --gres=gpu:v100-pcie:1 rodolfo_run.py --case='two'
