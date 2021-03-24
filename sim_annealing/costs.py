import logging
import random
import numpy as np
import copy

def isling_cost(S, I, A=1):
  '''
  summary:
    cost function for the simulated annealing

  Params:
    S 
      des: given set of N positive numbers to be partitioned e.g {n1,n2,...nN}
      type: np.array
    I
      des: list of isling spin variables
      type: list or np.array
    A
      des: a postive constance, A>0
      type: int

    let n[i] (i=1,...,N=|S|) , S
    let s[i] (i=1,...,N=|S|), I
    H = A * (np.sum([n[x]*s[i] for x in range(N)]))**2

  Returns:
    isling cost
  '''
  s_len = len(S)
  I = np.array(I)
  
  return A * (S.dot(I.reshape(s_len,1))[0]**2)