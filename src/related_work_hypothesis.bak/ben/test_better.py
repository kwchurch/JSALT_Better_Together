
import torch
from tqdm import tqdm
import sys


# compare the fruits of your labor
case_one = torch.load('cosines_one.pt')
case_two = torch.load('cosines_two.pt')

greater_than = 0

for x in tqdm(range(len(case_one))):
    if case_one[x] > case_two[x]:
        greater_than +=1

# calculates the percentage of the time the merged df is better than the unmerged df
case_one_percentage = greater_than / len(case_one)

print('Related papers are more effective than all papers %2f percent of the time' % (1 - case_one_percentage))
