import sys
import numpy as np

def doit(n):
    try:
        np.zeros(n)
        return True
    except:
        return False

n=10
step=1.1

while True:
   if not doit(n):
       print(str(n) + '\tFalse')
       sys.exit()
   else:
       print(str(n) + '\tTrue')
       n = int(n*step)

