from matplotlib import pyplot as plt
import numpy as np
import joblib

s = joblib.load('1_hop_sims')

def c(l):
   return [x for x in l if x>=-1 and x<=1]

data = [c(s[i]) for i in range(90, 9, -10)]

print(data)
plt.title('1-Hop Cosine Similarities on Full Graph ProNE')
plt.boxplot(data)
plt.xlabel('Bin of Earlier Paper')
plt.ylabel('Cosine Similarity')
plt.xticks(list(range(1,10)), list(range(90, 9, -10)))
plt.savefig('1_hop_sim_plot.jpg')
plt.figure().close()

s = joblib.load('2_to_4_hop_sims')

def c(l):
   return [x for x in l if x>=-1 and x<=1]

data = [c(s[i]) for i in range(90, 9, -10)]

print(data)
plt.title('2 to 4-Hop Cosine Similarities on Full Graph ProNE')
plt.boxplot(data)
plt.xlabel('Bin of Earlier Paper')
plt.ylabel('Cosine Similarity')
plt.xticks(list(range(1,10)), list(range(90, 9, -10)))
plt.savefig('2_to_4_hop_sim_plot.jpg')
